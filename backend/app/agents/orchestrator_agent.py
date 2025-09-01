"""
Orchestrator Agent
=================

Coordinates the workflow between the 3 GraphRAG agents (Local, Global, DRIFT)
for both AI Assistant and AI Analysis tools.
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import BaseAgent
from ..schemas.a2a import A2AEnvelope, MessageType
from ..adapters.a2a import A2AAdapter


class OrchestratorAgent(BaseAgent):
    """Agent responsible for orchestrating the workflow between GraphRAG agents."""
    
    def __init__(self, neo4j_conn, azure_llm, a2a_adapter: A2AAdapter):
        super().__init__("orchestrator_agent", neo4j_conn, azure_llm)
        self.a2a_adapter = a2a_adapter
        
    async def handle_message(self, envelope: A2AEnvelope) -> Optional[A2AEnvelope]:
        """Handle orchestration requests."""
        try:
            task_type = envelope.payload.get("task_type")
            data = envelope.payload.get("data", {})
            
            if task_type == "assistant_workflow":
                return await self._execute_assistant_workflow(data, envelope)
            elif task_type == "analysis_workflow":
                return await self._execute_analysis_workflow(data, envelope)
            else:
                return await self.send_error_response(envelope, f"Unknown task type: {task_type}")
                
        except Exception as e:
            self.logger.error(f"Orchestrator agent error: {e}")
            return await self.send_error_response(envelope, str(e))
    
    async def _execute_assistant_workflow(self, data: Dict[str, Any], envelope: A2AEnvelope) -> A2AEnvelope:
        """Execute the AI Assistant workflow using all 3 GraphRAG agents."""
        query = data.get("query", "")
        strategy = data.get("strategy", "hybrid")
        max_results = data.get("max_results", 10)
        conversation_id = envelope.conversation_id
        
        self.logger.info(f"Executing assistant workflow for query: {query} with strategy: {strategy}")
        
        try:
            # Step 1: Execute GraphRAG retrieval based on strategy
            rag_results = await self._execute_graphrag_retrieval(
                conversation_id, query, strategy, max_results
            )
            
            if not rag_results["success"]:
                return await self.send_error_response(envelope, rag_results["error"])
            
            # Step 2: Generate AI response using the retrieved data
            ai_response = await self._generate_ai_response(query, rag_results["data"])
            
            # Step 3: Prepare final response
            final_response = {
                "response": ai_response,
                "conversation_id": conversation_id,
                "citations": rag_results["data"]["citations"],
                "nodes": rag_results["data"]["nodes"],
                "edges": rag_results["data"]["edges"],
                "metadata": {
                    "strategy": strategy,
                    "coverage": rag_results["data"]["coverage"],
                    "confidence": rag_results["data"]["confidence"],
                    "workflow": "multi_agent_assistant",
                    "agents_used": rag_results["data"]["agents_used"]
                }
            }
            
            return await self.send_response(envelope, final_response, True)
            
        except Exception as e:
            self.logger.error(f"Assistant workflow error: {e}")
            return await self.send_error_response(envelope, str(e))
    
    async def _execute_analysis_workflow(self, data: Dict[str, Any], envelope: A2AEnvelope) -> A2AEnvelope:
        """Execute the AI Analysis workflow using all 3 GraphRAG agents."""
        query = data.get("query", "")
        analysis_type = data.get("analysis_type", "comprehensive")
        max_depth = data.get("max_depth", 3)
        conversation_id = envelope.conversation_id
        
        self.logger.info(f"Executing analysis workflow for query: {query}")
        
        try:
            # Step 1: Execute comprehensive GraphRAG retrieval using all agents
            rag_results = await self._execute_graphrag_retrieval(
                conversation_id, query, "comprehensive", 15
            )
            
            if not rag_results["success"]:
                return await self.send_error_response(envelope, rag_results["error"])
            
            # Step 2: Perform legal analysis
            analysis_results = await self._perform_legal_analysis(
                query, rag_results["data"], max_depth
            )
            
            # Step 3: Generate AI summary and recommendations
            ai_summary = await self._generate_analysis_summary(query, analysis_results)
            
            # Step 4: Prepare final response
            final_response = {
                "query": query,
                "contradictions": analysis_results["contradictions"],
                "recommendations": analysis_results["recommendations"],
                "summary": ai_summary,
                "confidence": 0.85,
                "stats": analysis_results["stats"],
                "harmonizations": analysis_results["harmonizations"],
                "citations": rag_results["data"]["citations"],
                "metadata": {
                    "workflow": "multi_agent_analysis",
                    "analysis_type": analysis_type,
                    "max_depth": max_depth,
                    "agents_used": rag_results["data"]["agents_used"]
                }
            }
            
            return await self.send_response(envelope, final_response, True)
            
        except Exception as e:
            self.logger.error(f"Analysis workflow error: {e}")
            return await self.send_error_response(envelope, str(e))
    
    async def _execute_graphrag_retrieval(self, conversation_id: str, query: str, strategy: str, max_results: int) -> Dict[str, Any]:
        """Execute GraphRAG retrieval using the appropriate agents."""
        try:
            agents_to_use = []
            
            if strategy == "local":
                agents_to_use = ["local_graphrag_agent"]
            elif strategy == "global":
                agents_to_use = ["global_graphrag_agent"]
            elif strategy == "drift":
                agents_to_use = ["drift_graphrag_agent"]
            else:  # hybrid or comprehensive
                agents_to_use = ["local_graphrag_agent", "global_graphrag_agent", "drift_graphrag_agent"]
            
            # Execute retrieval with each agent
            agent_results = []
            for agent_id in agents_to_use:
                try:
                    result = await self.a2a_adapter.send_task(
                        conversation_id=conversation_id,
                        sender=self.agent_id,
                        recipient=agent_id,
                        task_type="retrieve",
                        payload={
                            "query": query,
                            "max_results": max_results // len(agents_to_use) if len(agents_to_use) > 1 else max_results
                        }
                    )
                    
                    if result and result.payload.get("success", False):
                        agent_results.append(result.payload.get("result", {}))
                    else:
                        self.logger.warning(f"Agent {agent_id} failed to retrieve data")
                        
                except Exception as e:
                    self.logger.error(f"Error with agent {agent_id}: {e}")
            
            if not agent_results:
                return {"success": False, "error": "All GraphRAG agents failed"}
            
            # Merge results from all agents
            merged_data = self._merge_agent_results(agent_results)
            
            return {
                "success": True,
                "data": merged_data
            }
            
        except Exception as e:
            self.logger.error(f"GraphRAG retrieval error: {e}")
            return {"success": False, "error": str(e)}
    
    def _merge_agent_results(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge results from multiple GraphRAG agents."""
        all_nodes = {}
        all_edges = {}
        all_citations = {}
        agents_used = []
        
        for result in agent_results:
            # Merge nodes
            for node in result.get("nodes", []):
                all_nodes[node["id"]] = node
            
            # Merge edges
            for edge in result.get("edges", []):
                edge_key = f"{edge['source']}_{edge['target']}_{edge['type']}"
                all_edges[edge_key] = edge
            
            # Merge citations
            for citation in result.get("citations", []):
                all_citations[citation["node_id"]] = citation
            
            # Track agents used
            if result.get("agent_id"):
                agents_used.append(result["agent_id"])
        
        # Calculate overall metrics
        total_coverage = sum(result.get("coverage", 0) for result in agent_results) / len(agent_results)
        total_confidence = sum(result.get("confidence", 0) for result in agent_results) / len(agent_results)
        
        return {
            "nodes": list(all_nodes.values()),
            "edges": list(all_edges.values()),
            "citations": list(all_citations.values()),
            "coverage": total_coverage,
            "confidence": total_confidence,
            "agents_used": agents_used
        }
    
    async def _generate_ai_response(self, query: str, rag_data: Dict[str, Any]) -> str:
        """Generate AI response using the retrieved GraphRAG data."""
        try:
            # Check if we have GraphRAG data
            has_graphrag_data = len(rag_data.get("citations", [])) > 0
            
            if has_graphrag_data:
                # Create context from citations
                citations = rag_data.get("citations", [])
                context_text = "\n\n".join([
                    f"Source {i+1}: {citation['content']}"
                    for i, citation in enumerate(citations[:5])  # Top 5 citations
                ])
                
                system_prompt = """You are a legal research assistant for UAE law. Use the provided GraphRAG sources to answer questions accurately and cite your sources. 

IMPORTANT: Always mention that you used GraphRAG techniques and cite the specific nodes/edges from the knowledge graph that were relevant to your answer.

Format your response as follows:
1. Answer the question based on the GraphRAG sources
2. Mention which GraphRAG strategies were used (Local, Global, DRIFT)
3. Cite specific nodes from the knowledge graph that were relevant
4. If you used relationships between nodes, mention those as well"""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {query}\n\nGraphRAG Sources:\n{context_text}\n\nPlease provide a comprehensive answer based on the GraphRAG sources provided."}
                ]
            else:
                # No GraphRAG data available
                system_prompt = """You are a legal research assistant for UAE law. Since no specific GraphRAG sources were found in the knowledge graph, you should use your general knowledge about UAE law and legal principles to provide a helpful response.

IMPORTANT: 
1. Clearly state that you are providing information based on general knowledge since no specific GraphRAG sources were found
2. Mention that you did not use GraphRAG techniques for this response
3. Provide accurate and helpful information about UAE law
4. If the question is very specific and requires current legal information, suggest consulting with a legal professional

For complex or time-sensitive legal matters, always recommend consulting with qualified legal professionals."""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {query}\n\nPlease provide a helpful response about UAE law based on your general knowledge. Clearly state that no GraphRAG sources were found and you are using general knowledge."}
                ]
            
            # Generate response
            response = await self.azure_llm.chat(messages, temperature=0.7, max_tokens=1500)
            return response
            
        except Exception as e:
            self.logger.error(f"AI response generation error: {e}")
            return f"I apologize, but I encountered an error while generating the response: {str(e)}. Please try again or contact support."
    
    async def _perform_legal_analysis(self, query: str, rag_data: Dict[str, Any], max_depth: int) -> Dict[str, Any]:
        """Perform legal analysis using the retrieved data."""
        try:
            # Find contradictions in the retrieved nodes
            node_ids = [node["id"] for node in rag_data.get("nodes", [])]
            
            if not node_ids:
                return {
                    "contradictions": [],
                    "harmonizations": [],
                    "recommendations": [],
                    "stats": {"total_contradictions": 0}
                }
            
            # Query for contradictions
            contradictions_query = """
            MATCH (a:LegalNode)-[r:RELATES_TO]->(b:LegalNode)
            WHERE a.id IN $node_ids AND b.id IN $node_ids AND r.type = 'CONTRADICTS'
            RETURN a, b, properties(r) as r_props
            """
            
            contradictions_result = await self.neo4j_conn.run_cypher(contradictions_query, {"node_ids": node_ids})
            
            # Process contradictions
            contradictions = []
            for record in contradictions_result:
                if "a" in record and "b" in record and "r_props" in record:
                    node_a = record["a"]
                    node_b = record["b"]
                    relationship_props = record["r_props"]
                    
                    priority = relationship_props.get("priority", "medium")
                    severity = relationship_props.get("severity", "medium")
                    category = relationship_props.get("category", "Legal Compliance")
                    description = relationship_props.get("description", f"Contradiction between {node_a.get('title', '')} and {node_b.get('title', '')}")
                    
                    contradiction = {
                        "id": f"cont_{node_a.get('id', '')}_{node_b.get('id', '')}",
                        "title": f"Legal Contradiction: {node_a.get('title', '')} vs {node_b.get('title', '')}",
                        "description": description,
                        "severity": severity,
                        "priority": priority,
                        "category": category,
                        "sources": [node_a.get("title", ""), node_b.get("title", "")],
                        "impact": f"High impact on {category.lower()} compliance and regulatory alignment",
                        "recommendation": f"Review and harmonize the conflicting provisions between {node_a.get('title', '')} and {node_b.get('title', '')} to ensure {category.lower()} compliance"
                    }
                    contradictions.append(contradiction)
            
            # Generate harmonizations
            harmonizations = []
            for contradiction in contradictions:
                harmonization = {
                    "id": f"harm_{len(harmonizations) + 1}",
                    "title": f"Harmonization for {contradiction['title']}",
                    "description": f"Legal harmonization required to resolve contradiction: {contradiction['description']}",
                    "approach": "Legal harmonization and regulatory alignment",
                    "related_contradiction": contradiction["id"],
                    "priority": contradiction.get("priority", "medium")
                }
                harmonizations.append(harmonization)
            
            # Generate recommendations
            recommendations = []
            for contradiction in contradictions:
                severity = contradiction.get("severity", "medium")
                
                if severity == "critical":
                    priority = "high"
                    timeline = "Immediate (7 days)"
                    cost_impact = "Critical - Immediate compliance costs"
                elif severity == "high":
                    priority = "high"
                    timeline = "Short-term (30 days)"
                    cost_impact = "High - Compliance and harmonization costs"
                elif severity == "medium":
                    priority = "medium"
                    timeline = "Medium-term (90 days)"
                    cost_impact = "Medium - Review and alignment costs"
                else:
                    priority = "low"
                    timeline = "Long-term (180 days)"
                    cost_impact = "Low - Monitoring and review costs"
                
                recommendations.append({
                    "id": f"rec_{contradiction['id']}",
                    "title": f"Address {contradiction.get('category', 'Legal')} Contradiction",
                    "description": f"Implement measures to resolve the contradiction: {contradiction['title']}",
                    "action": contradiction.get("recommendation", "Review and harmonize conflicting provisions"),
                    "priority": priority,
                    "timeline": timeline,
                    "cost_impact": cost_impact
                })
            
            # Calculate stats
            stats = {
                "total_contradictions": len(contradictions),
                "critical_priority": len([c for c in contradictions if c.get("severity") == "critical"]),
                "high_priority": len([c for c in contradictions if c.get("severity") == "high"]),
                "medium_priority": len([c for c in contradictions if c.get("severity") == "medium"]),
                "low_priority": len([c for c in contradictions if c.get("severity") == "low"])
            }
            
            return {
                "contradictions": contradictions,
                "harmonizations": harmonizations,
                "recommendations": recommendations,
                "stats": stats
            }
            
        except Exception as e:
            self.logger.error(f"Legal analysis error: {e}")
            return {
                "contradictions": [],
                "harmonizations": [],
                "recommendations": [],
                "stats": {"total_contradictions": 0}
            }
    
    async def _generate_analysis_summary(self, query: str, analysis_results: Dict[str, Any]) -> str:
        """Generate AI summary of the analysis results."""
        try:
            contradictions = analysis_results.get("contradictions", [])
            
            if contradictions:
                severity_counts = {
                    "critical": len([c for c in contradictions if c.get("severity") == "critical"]),
                    "high": len([c for c in contradictions if c.get("severity") == "high"]),
                    "medium": len([c for c in contradictions if c.get("severity") == "medium"]),
                    "low": len([c for c in contradictions if c.get("severity") == "low"])
                }
                
                severity_text = []
                if severity_counts["critical"] > 0:
                    severity_text.append(f"{severity_counts['critical']} critical")
                if severity_counts["high"] > 0:
                    severity_text.append(f"{severity_counts['high']} high priority")
                if severity_counts["medium"] > 0:
                    severity_text.append(f"{severity_counts['medium']} medium priority")
                if severity_counts["low"] > 0:
                    severity_text.append(f"{severity_counts['low']} low priority")
                
                severity_summary = ", ".join(severity_text)
                summary = f"Analysis of '{query}' identified {len(contradictions)} legal contradictions ({severity_summary}) requiring immediate attention. Found {len(analysis_results.get('harmonizations', []))} harmonization opportunities."
            else:
                summary = f"Analysis of '{query}' found no explicit contradictions in the current knowledge base. Consider expanding the legal data or refining the search criteria."
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Analysis summary generation error: {e}")
            return f"Analysis completed for '{query}' with {len(analysis_results.get('contradictions', []))} contradictions found."
