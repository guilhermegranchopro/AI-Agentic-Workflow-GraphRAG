"""Legal Assistant - AI Chatbot powered by Azure OpenAI and AI Agents Workflow for UAE Legal System."""
import streamlit as st
import sys
import os
import asyncio
from datetime import datetime
from pathlib import Path
import json

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    # Import the new AI Agents Workflow system
    from src.agents.manager import get_agent_system, initialize_agents_for_streamlit
    from src.config import settings
    from src.db import db
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.stop()


def main():
    """Main Legal Assistant chatbot page."""
    st.set_page_config(
        page_title="Legal Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 UAE Legal Assistant")
    st.markdown("**AI-powered legal chatbot using AI Agents Workflow and Azure OpenAI**")
    
    # Initialize the agent system
    if 'agent_system_initialized' not in st.session_state:
        st.session_state.agent_system_initialized = False
    
    # System status display
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.agent_system_initialized:
                st.success("🤖 AI Agents: Active")
            else:
                st.warning("🤖 AI Agents: Initializing...")
        
        with col2:
            # Test database connection
            try:
                db_health = db.health_check()
                if db_health:
                    st.success("📊 Database: Connected")
                else:
                    st.error("📊 Database: Disconnected")
            except:
                st.error("📊 Database: Error")
        
        with col3:
            st.info("🧠 Mode: AI Agents Workflow")
    
    # Initialize agents in background
    if not st.session_state.agent_system_initialized:
        with st.spinner("Initializing AI Agents Workflow..."):
            try:
                # Run async initialization
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(initialize_agents_for_streamlit())
                loop.close()
                
                if success:
                    st.session_state.agent_system_initialized = True
                    st.success("✅ AI Agents Workflow initialized successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to initialize AI Agents Workflow")
                    st.stop()
            except Exception as e:
                st.error(f"❌ Agent initialization error: {e}")
                st.stop()
    
    # Sidebar for chatbot settings
    with st.sidebar:
        st.header("⚙️ Assistant Settings")
        
        # RAG Strategy Selection (now shows AI Agents)
        rag_strategy = st.selectbox(
            "AI Agent Strategy",
            ["Smart Auto (Orchestrator)", "Multi-Agent Synthesis", "Local RAG Agent", "Global RAG Agent", "DRIFT RAG Agent"],
            help="Choose which AI agents to use for your query"
        )
        
        st.info("🤖 **AI Agents Workflow Active**")
        st.markdown("**Available Agents:**")
        st.markdown("""
        - 🧠 **Orchestrator**: Intelligent coordination
        - 🔍 **Local RAG**: Specific provisions
        - 🌐 **Global RAG**: Broad concepts  
        - ⏱️ **DRIFT RAG**: Temporal analysis
        """)
        
        # Agent Performance Metrics
        if st.button("📊 View Agent Performance"):
            if st.session_state.agent_system_initialized:
                with st.spinner("Fetching agent performance..."):
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        system = loop.run_until_complete(get_agent_system())
                        status = system.get_system_status()
                        loop.close()
                        
                        st.json(status)
                    except Exception as e:
                        st.error(f"Error fetching performance: {e}")
            else:
                st.warning("Agent system not initialized")
        
        # Response style
        response_style = st.selectbox(
            "Response Style",
            ["Professional Legal", "Educational", "Conversational"],
            help="Choose the tone and style of responses"
        )
        
        # Citation style
        citation_style = st.selectbox(
            "Citation Format",
            ["Detailed", "Brief", "Academic"],
            help="How to format legal citations"
        )
        
        # Maximum sources
        max_sources = st.slider(
            "Max Sources",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of sources to cite"
        )
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            if "chat_messages" in st.session_state:
                del st.session_state.chat_messages
            st.rerun()
        
        # Export chat button
        if st.button("📥 Export Chat", type="secondary"):
            export_chat_history()
        
        # Show additional info
        st.info("💡 **Quick Start Examples:**")
        st.markdown("""
        - "What is Article 25 of the UAE Constitution?"
        - "Explain the process for civil liability claims"
        - "What are the recent changes in commercial law?"
        - "Compare penalties for contract breach vs tort"
        - "What rights do employees have under UAE law?"
        """)
        
        # Legal areas  
        st.markdown("**🏛️ Coverage Areas:**")
        st.markdown("""
        - Constitutional Law
        - Civil Code
        - Commercial Law
        - Criminal Law
        - Labor Law
        - Administrative Law
        """)
    
    # Initialize chat history
    if "chat_messages" in st.session_state:
        chat_messages = st.session_state.chat_messages
    else:
        chat_messages = []
        st.session_state.chat_messages = chat_messages
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(chat_messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander(f"📚 Sources ({len(message['sources'])})", expanded=False):
                        display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about UAE legal matters..."):
        # Add user message to chat
        chat_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI Agents processing your query..."):
                try:
                    # Use the new AI Agents Workflow
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    system = loop.run_until_complete(get_agent_system())
                    
                    # Map strategy selection to agent preferences
                    preferences = {
                        'rag_strategy': _map_strategy_selection(rag_strategy),
                        'response_style': response_style,
                        'citation_style': citation_style,
                        'max_sources': max_sources
                    }
                    
                    # Process query through agent system
                    if rag_strategy == "Multi-Agent Synthesis":
                        result = loop.run_until_complete(
                            system.process_multi_agent_query(prompt, f"session_{len(chat_messages)}")
                        )
                    else:
                        result = loop.run_until_complete(
                            system.process_user_query(prompt, f"session_{len(chat_messages)}", preferences)
                        )
                    
                    loop.close()
                    
                    if result.get('error'):
                        st.error(f"❌ Agent Error: {result['response']}")
                        chat_messages.append({"role": "assistant", "content": result['response']})
                    else:
                        response = result['response']
                        sources = result.get('sources', [])
                        
                        st.markdown(response)
                        
                        # Display sources with agent information
                        if sources:
                            with st.expander(f"📚 Sources ({len(sources)}) - Agent: {result.get('agent_id', 'Multi-Agent')}", expanded=True):
                                display_sources_with_agents(sources, result)
                        
                        # Show agent performance info
                        if result.get('strategy_used'):
                            st.info(f"🧠 Strategy: **{result['strategy_used'].upper()}** | Confidence: {result.get('confidence', 0):.1%} | Response Time: {result.get('response_time', 0):.2f}s")
                        
                        # Add assistant response to chat
                        chat_messages.append({
                            "role": "assistant", 
                            "content": response,
                            "sources": sources,
                            "agent_info": {
                                "strategy": result.get('strategy_used', 'unknown'),
                                "confidence": result.get('confidence', 0),
                                "response_time": result.get('response_time', 0),
                                "agent_id": result.get('agent_id', 'unknown')
                            }
                        })
                    
                except Exception as e:
                    error_msg = f"❌ AI Agents Error: {str(e)}"
                    st.error(error_msg)
                    chat_messages.append({"role": "assistant", "content": error_msg})
        
        # Update session state
        st.session_state.chat_messages = chat_messages


def _map_strategy_selection(rag_strategy: str) -> str:
    """Map Streamlit strategy selection to agent system preferences."""
    strategy_mapping = {
        "Smart Auto (Orchestrator)": "smart_auto",
        "Multi-Agent Synthesis": "multi_agent", 
        "Local RAG Agent": "local",
        "Global RAG Agent": "global",
        "DRIFT RAG Agent": "drift"
    }
    return strategy_mapping.get(rag_strategy, "smart_auto")


def display_sources_with_agents(sources: list, result: dict):
    """Display sources with agent information."""
    for i, source in enumerate(sources):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{i+1}. {source.get('title', 'Legal Source')}**")
                st.markdown(source.get('content', 'No content available')[:300] + "...")
            
            with col2:
                st.markdown(f"**Agent:** {source.get('source_agent', 'Unknown')}")
                st.markdown(f"**Confidence:** {source.get('confidence', 0):.1%}")
                if source.get('type'):
                    st.markdown(f"**Type:** {source.get('type', 'Unknown')}")
            
            st.divider()


def export_chat_history():
    """Export chat history to JSON."""
    if "chat_messages" in st.session_state and st.session_state.chat_messages:
        try:
            # Prepare export data
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "system": "UAE Legal Assistant - AI Agents Workflow",
                "total_messages": len(st.session_state.chat_messages),
                "chat_history": []
            }
            
            for msg in st.session_state.chat_messages:
                export_msg = {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": datetime.now().isoformat()
                }
                
                # Add agent information if available
                if "agent_info" in msg:
                    export_msg["agent_info"] = msg["agent_info"]
                
                # Add sources if available
                if "sources" in msg:
                    export_msg["sources_count"] = len(msg["sources"])
                
                export_data["chat_history"].append(export_msg)
            
            # Create download
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download Chat History",
                data=json_str,
                file_name=f"uae_legal_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Export failed: {e}")
    else:
        st.warning("No chat history to export")


if __name__ == "__main__":
    main()
    """
    Generate a legal response using the specified RAG strategy and Azure OpenAI.
    
    Args:
        query: User's legal question
        rag_strategy: RAG strategy to use
        response_style: Style of response
        citation_style: Citation format
        max_sources: Maximum sources to include
        chat_history: Previous chat messages for context
        
    Returns:
        Tuple of (response_text, sources_list)
    """
    # Analyze the query for better processing
    query_analysis = analyze_legal_query(query)
    
    # Get relevant information using GraphRAG
    if rag_strategy == "Smart Auto":
        # Use the suggested strategy from analysis
        suggested_strategy = query_analysis['suggested_strategy']
        
        if suggested_strategy == 'drift':
            rag_results = drift_rag_query(query, datetime.now().date())
        elif suggested_strategy == 'global':
            rag_results = global_rag_query(query)
        else:  # local
            rag_results = local_rag_query(query)
            
        # Show which strategy was used
        strategy_info = f"🧠 Auto-selected: **{suggested_strategy.upper()} RAG** (Confidence: {query_analysis['confidence']:.1%})"
        
    elif rag_strategy == "Local RAG":
        rag_results = local_rag_query(query)
        strategy_info = "🔍 Using: **LOCAL RAG**"
    elif rag_strategy == "Global RAG":
        rag_results = global_rag_query(query)
        strategy_info = "🌐 Using: **GLOBAL RAG**"
    elif rag_strategy == "DRIFT RAG":
        rag_results = drift_rag_query(query, datetime.now().date())
        strategy_info = "⏱️ Using: **DRIFT RAG**"
    else:
        rag_results = "No results found."
        strategy_info = ""
    
    # Enhanced source extraction using query analysis
    sources = enhanced_source_extraction(rag_results, query_analysis, max_sources)
    
    # Build context for Azure OpenAI
    context = build_enhanced_chat_context(
        query, rag_results, response_style, citation_style, 
        chat_history, query_analysis, strategy_info
    )
    
    # Generate response using Azure OpenAI
    try:
        client = get_azure_openai_client()
        
        response = client.chat.completions.create(
            model=settings.azure_openai_chat_deployment,  # Use the configured deployment name
            messages=context,
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=1500,
            top_p=0.9
        )
        
        assistant_response = response.choices[0].message.content
        
        # Format response with enhanced citations
        formatted_response = format_legal_response(assistant_response, sources, citation_style)
        
        # Add strategy info at the beginning
        if strategy_info:
            formatted_response = f"{strategy_info}\n\n{formatted_response}"
        
        return formatted_response, sources
        
    except Exception as e:
        return f"Error generating response: {str(e)}", []


def smart_rag_selection(query: str, max_sources: int) -> tuple:
    """
    Automatically select the best RAG strategy based on query characteristics.
    
    Args:
        query: User's question
        max_sources: Maximum sources to return
        
    Returns:
        Tuple of (rag_results, sources)
    """
    query_lower = query.lower()
    
    # Keywords that suggest different RAG strategies
    temporal_keywords = ['recent', 'current', 'latest', 'new', 'updated', 'change', 'amendment']
    specific_keywords = ['article', 'section', 'provision', 'law number', 'decree']
    general_keywords = ['overview', 'explain', 'what is', 'how does', 'definition']
    
    # Check for temporal queries (use DRIFT RAG)
    if any(keyword in query_lower for keyword in temporal_keywords):
        rag_results = drift_rag_query(query, datetime.now().date())
        strategy_used = "DRIFT RAG (Temporal)"
    
    # Check for specific provision queries (use Local RAG)
    elif any(keyword in query_lower for keyword in specific_keywords):
        rag_results = local_rag_query(query)
        strategy_used = "Local RAG (Specific)"
    
    # Check for general concept queries (use Global RAG)
    elif any(keyword in query_lower for keyword in general_keywords):
        rag_results = global_rag_query(query)
        strategy_used = "Global RAG (General)"
    
    # Default to Local RAG
    else:
        rag_results = local_rag_query(query)
        strategy_used = "Local RAG (Default)"
    
    sources = extract_sources_from_rag_result(rag_results, max_sources)
    
    # Add strategy info to sources
    if sources:
        sources[0]["strategy_used"] = strategy_used
    
    return rag_results, sources


def extract_sources_from_rag_result(rag_result: str, max_sources: int) -> list:
    """
    Extract source information from RAG query results.
    
    Args:
        rag_result: RAG query result
        max_sources: Maximum sources to extract
        
    Returns:
        List of source dictionaries
    """
    sources = []
    
    try:
        # Try to extract sources from the result text
        # This is a simplified extraction - you might need to adjust based on your RAG result format
        lines = rag_result.split('\n')
        
        for line in lines:
            if any(indicator in line.lower() for indicator in ['source:', 'article', 'law', 'decree']):
                # Extract source information
                source_info = {
                    "text": line.strip(),
                    "type": "Legal Document",
                    "timestamp": datetime.now().isoformat(),
                    "relevance_score": 0.8  # Default score
                }
                sources.append(source_info)
                
                if len(sources) >= max_sources:
                    break
        
        # If no sources found in text, try to get from knowledge graph
        if not sources:
            # Search for related provisions
            kg_results = search_provisions_by_text(rag_result[:100])  # Use first 100 chars
            
            for result in kg_results[:max_sources]:
                source_info = {
                    "text": result.get("text", "No text available"),
                    "type": "Knowledge Graph",
                    "id": result.get("id", "Unknown"),
                    "instrument": result.get("instrument", "Unknown"),
                    "relevance_score": 0.7
                }
                sources.append(source_info)
    
    except Exception as e:
        st.warning(f"Could not extract sources: {str(e)}")
    
    return sources


def build_enhanced_chat_context(query: str, rag_results: str, response_style: str, 
                              citation_style: str, chat_history: list, 
                              query_analysis: dict, strategy_info: str) -> list:
    """
    Build enhanced context for Azure OpenAI chat completion with query analysis.
    """
    # Enhanced system prompt based on query analysis
    style_prompts = {
        "Professional Legal": "You are a professional legal assistant specializing in UAE law. Provide precise, formal responses using proper legal terminology.",
        "Educational": "You are an educational legal assistant. Explain UAE legal concepts clearly and comprehensively, suitable for students and professionals learning the law.",
        "Conversational": "You are a friendly legal assistant. Explain UAE legal matters in an accessible, conversational way while maintaining accuracy."
    }
    
    citation_prompts = {
        "Detailed": "Always provide detailed citations with full legal references, article numbers, and relevant context.",
        "Brief": "Provide brief, concise citations with essential reference information only.",
        "Academic": "Use formal academic citation style with complete legal references and proper formatting."
    }
    
    # Query-specific guidance
    query_type = query_analysis.get('query_type', 'general')
    entities = query_analysis.get('entities', {})
    
    query_guidance = {
        'definition': "Focus on providing clear, accurate definitions with legal context and implications.",
        'procedural': "Provide step-by-step procedures with relevant legal requirements and deadlines.",
        'specific_provision': "Quote the exact provision text and explain its meaning and application.",
        'comparative': "Provide detailed comparisons highlighting key similarities and differences.",
        'penalty': "Clearly state penalties, fines, and consequences with relevant legal authority.",
        'rights_obligations': "Comprehensively explain rights and corresponding obligations.",
        'general': "Provide comprehensive overview covering key aspects and implications."
    }
    
    system_prompt = f"""
    {style_prompts.get(response_style, style_prompts['Professional Legal'])}
    
    You are an expert in UAE legal system with access to the comprehensive legal knowledge graph.
    
    Query Analysis:
    - Query Type: {query_type}
    - Complexity: {"High" if query_analysis.get('is_complex') else "Standard"}
    - Temporal Aspect: {"Yes" if query_analysis.get('is_temporal') else "No"}
    - Confidence: {query_analysis.get('confidence', 0.7):.1%}
    
    Specific Guidance for this query type:
    {query_guidance.get(query_type, query_guidance['general'])}
    
    Citation Requirements:
    {citation_prompts.get(citation_style, citation_prompts['Detailed'])}
    
    Legal Framework Guidelines:
    - Always ground responses in the provided legal information from the knowledge graph
    - Distinguish between federal and local UAE laws when relevant
    - Consider the hierarchy: Constitution > Federal Laws > Local Laws > Regulations
    - Reference specific articles, sections, or provisions when available
    - If information is incomplete, clearly state limitations
    - Provide practical implications and real-world applications when appropriate
    - Consider cross-references to related legal provisions
    
    UAE Legal Knowledge Base:
    {rag_results}
    
    Strategy Used: {strategy_info}
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add relevant chat history (last 8 messages for better context)
    recent_history = chat_history[-8:] if len(chat_history) > 8 else chat_history
    messages.extend(recent_history)
    
    # Enhanced user query with extracted entities
    enhanced_query = query
    if entities.get('articles') or entities.get('laws') or entities.get('decrees'):
        entity_info = []
        if entities.get('articles'):
            entity_info.append(f"Articles: {', '.join(entities['articles'])}")
        if entities.get('laws'):
            entity_info.append(f"Laws: {', '.join([f'No. {law[0]}' + (f' of {law[1]}' if law[1] else '') for law in entities['laws']])}")
        if entities.get('decrees'):
            entity_info.append(f"Decrees: {', '.join([f'No. {decree[0]}' + (f' of {decree[1]}' if decree[1] else '') for decree in entities['decrees']])}")
        
        enhanced_query += f"\n\n[Extracted Legal Entities: {'; '.join(entity_info)}]"
    
    messages.append({"role": "user", "content": enhanced_query})
    
    return messages


def build_chat_context(query: str, rag_results: str, response_style: str, 
                      citation_style: str, chat_history: list) -> list:
    """
    Build the context for Azure OpenAI chat completion.
    
    Args:
        query: User's question
        rag_results: Results from GraphRAG
        response_style: Response style
        citation_style: Citation format
        chat_history: Previous chat messages
        
    Returns:
        List of messages for OpenAI chat completion
    """
    # System prompt based on response style
    style_prompts = {
        "Professional Legal": "You are a professional legal assistant specializing in UAE law. Provide precise, formal responses using proper legal terminology.",
        "Educational": "You are an educational legal assistant. Explain UAE legal concepts clearly and comprehensively, suitable for students and professionals learning the law.",
        "Conversational": "You are a friendly legal assistant. Explain UAE legal matters in an accessible, conversational way while maintaining accuracy."
    }
    
    citation_prompts = {
        "Detailed": "Always provide detailed citations with full legal references, article numbers, and relevant context.",
        "Brief": "Provide brief, concise citations with essential reference information only.",
        "Academic": "Use formal academic citation style with complete legal references and proper formatting."
    }
    
    system_prompt = f"""
    {style_prompts.get(response_style, style_prompts['Professional Legal'])}
    
    You have access to the UAE legal knowledge graph and must base your responses on the provided information.
    
    Guidelines:
    - Always ground your responses in the provided legal information
    - {citation_prompts.get(citation_style, citation_prompts['Detailed'])}
    - If information is not available in the provided context, clearly state this
    - Distinguish between federal and local UAE laws when relevant
    - Consider the hierarchy of UAE legal sources (Constitution, Federal Laws, Local Laws, etc.)
    - Provide practical implications when appropriate
    
    UAE Legal Context:
    {rag_results}
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent chat history for context (last 6 messages)
    recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
    messages.extend(recent_history)
    
    # Add current user query
    messages.append({"role": "user", "content": query})
    
    return messages


def display_sources(sources: list):
    """
    Display source information in a formatted way.
    
    Args:
        sources: List of source dictionaries
    """
    if not sources:
        st.info("No sources available")
        return
    
    for i, source in enumerate(sources, 1):
        with st.container():
            # Source header
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**Source {i}**: {source.get('type', 'Unknown')}")
            with col2:
                if 'relevance_score' in source:
                    score = source['relevance_score']
                    st.markdown(f"📊 {score:.1%}")
            with col3:
                if 'strategy_used' in source:
                    st.markdown(f"🔧 {source['strategy_used']}")
            
            # Source content
            if 'instrument' in source:
                st.markdown(f"**Document**: {source['instrument']}")
            if 'id' in source:
                st.markdown(f"**ID**: {source['id']}")
            
            # Source text
            text = source.get('text', 'No text available')
            if len(text) > 200:
                with st.expander("📄 Full Text"):
                    st.markdown(text)
                st.markdown(f"📄 {text[:200]}...")
            else:
                st.markdown(f"📄 {text}")
            
            if i < len(sources):
                st.divider()


def export_chat_history():
    """Export chat history to JSON file."""
    if "chat_messages" not in st.session_state or not st.session_state.chat_messages:
        st.warning("No chat history to export")
        return
    
    # Prepare export data
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "chat_session": st.session_state.chat_messages,
        "total_messages": len(st.session_state.chat_messages)
    }
    
    # Convert to JSON
    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    # Offer download
    st.download_button(
        label="📥 Download Chat History",
        data=json_data,
        file_name=f"uae_legal_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )


# Add some helper functions for additional features
def search_provisions_by_text(search_text: str, limit: int = 5) -> list:
    """
    Search provisions in the knowledge graph by text content.
    
    Args:
        search_text: Text to search for
        limit: Maximum results to return
        
    Returns:
        List of matching provisions
    """
    try:
        with db.session() as session:
            query = """
            MATCH (p:Provision)
            WHERE p.text CONTAINS $search_text
            OPTIONAL MATCH (p)<-[:HAS_PROVISION]-(i:Instrument)
            RETURN p.id as id, p.text as text, i.id as instrument
            LIMIT $limit
            """
            
            result = session.run(query, search_text=search_text, limit=limit)
            return [dict(record) for record in result]
    except Exception as e:
        st.warning(f"Search error: {str(e)}")
        return []


if __name__ == "__main__":
    main()
