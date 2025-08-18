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
                
                # Show sources with agent info if available
                if message["role"] == "assistant" and "sources" in message:
                    agent_info = message.get("agent_info", {})
                    agent_strategy = agent_info.get("strategy", "unknown")
                    with st.expander(f"📚 Sources ({len(message['sources'])}) - Strategy: {agent_strategy.upper()}", expanded=False):
                        display_sources_with_agents(message["sources"], message.get("agent_info", {}))
    
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
                            strategy_used = result.get('strategy_used', 'unknown')
                            with st.expander(f"📚 Sources ({len(sources)}) - Strategy: {strategy_used.upper()}", expanded=True):
                                display_sources_with_agents(sources, result)
                        
                        # Show agent performance info
                        if result.get('strategy_used'):
                            confidence = result.get('confidence', 0)
                            response_time = result.get('response_time', 0)
                            st.info(f"🧠 Strategy: **{result['strategy_used'].upper()}** | Confidence: {confidence:.1%} | Response Time: {response_time:.2f}s")
                        
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
                content = source.get('content', 'No content available')
                if len(content) > 300:
                    content = content[:300] + "..."
                st.markdown(content)
            
            with col2:
                st.markdown(f"**Agent:** {source.get('source_agent', 'Unknown')}")
                confidence = source.get('confidence', 0)
                st.markdown(f"**Confidence:** {confidence:.1%}")
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
