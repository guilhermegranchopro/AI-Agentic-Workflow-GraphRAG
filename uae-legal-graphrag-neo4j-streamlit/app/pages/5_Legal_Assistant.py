"""Legal Assistant - AI Chatbot powered by Azure OpenAI and GraphRAG for UAE Legal System."""
import streamlit as st
import sys
import os
from datetime import datetime
from pathlib import Path
import json

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    # Import wrapper functions that match the expected signatures
    from utils.rag_wrapper import local_rag_query, global_rag_query, drift_rag_query
    from src.embeddings.azure_openai import get_azure_openai_client
    from src.graph.queries import search_provisions_by_text, get_node_details
    from src.db import db
    from utils.chatbot_utils import (
        analyze_legal_query, enhanced_source_extraction, 
        format_legal_response, get_related_provisions
    )
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
    st.markdown("**AI-powered legal chatbot using GraphRAG and Azure OpenAI**")
    
    # Sidebar for chatbot settings
    with st.sidebar:
        st.header("⚙️ Assistant Settings")
        
        # RAG Strategy Selection
        rag_strategy = st.selectbox(
            "RAG Strategy",
            ["Smart Auto", "Local RAG", "Global RAG", "DRIFT RAG"],
            help="Choose how the assistant retrieves information"
        )
        
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
            with st.spinner("🔍 Searching legal knowledge base..."):
                try:
                    response, sources = generate_legal_response(
                        prompt, 
                        rag_strategy, 
                        response_style, 
                        citation_style,
                        max_sources,
                        chat_messages[:-1]  # Previous messages for context
                    )
                    
                    st.markdown(response)
                    
                    # Display sources
                    if sources:
                        with st.expander(f"📚 Sources ({len(sources)})", expanded=True):
                            display_sources(sources)
                    
                    # Add assistant response to chat
                    chat_messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    chat_messages.append({"role": "assistant", "content": error_msg})
        
        # Update session state
        st.session_state.chat_messages = chat_messages


def generate_legal_response(query: str, rag_strategy: str, response_style: str, 
                          citation_style: str, max_sources: int, chat_history: list) -> tuple:
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
            model="gpt-4",  # or your deployed model name
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
