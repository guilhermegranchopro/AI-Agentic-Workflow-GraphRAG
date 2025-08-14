"""Home page for UAE Legal GraphRAG demo."""
import streamlit as st
import sys
import os
from datetime import date

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db


def main():
    """Main home page function."""
    st.set_page_config(
        page_title="UAE Legal GraphRAG",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("⚖️ UAE Legal GraphRAG Demo")
    st.markdown("**Neo4j + Streamlit + Azure OpenAI Embeddings**")
    
    st.markdown("""
    This demo showcases three different GraphRAG retrieval modes for UAE legal research:
    
    - **🎯 Local RAG**: Entity-centric traversal with temporal filtering
    - **🌐 Global RAG**: Community-based analysis using GDS Louvain
    - **🎪 DRIFT RAG**: Community-guided local search for comprehensive coverage
    """)
    
    # Sidebar controls
    render_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Overview", "🔧 Health Check", "📊 Database Stats"])
    
    with tab1:
        render_overview()
    
    with tab2:
        render_health_check()
    
    with tab3:
        render_database_stats()


def render_sidebar():
    """Render sidebar with global controls."""
    st.sidebar.title("⚙️ Global Settings")
    
    # As-of date control
    default_date = date.fromisoformat(settings.app_default_asof)
    as_of_date = st.sidebar.date_input(
        "As-of Date",
        value=default_date,
        help="Date for temporal filtering of legal changes"
    )
    
    # Store in session state for other pages
    st.session_state.as_of_date = as_of_date
    
    # Jurisdiction filter
    jurisdiction = st.sidebar.selectbox(
        "Jurisdiction",
        ["All", "UAE", "DIFC", "ADGM"],
        help="Filter by legal jurisdiction"
    )
    st.session_state.jurisdiction = jurisdiction
    
    # Search parameters
    st.sidebar.subheader("🔍 Search Settings")
    
    max_results = st.sidebar.slider(
        "Max Results",
        min_value=1,
        max_value=20,
        value=5,
        help="Maximum number of search results"
    )
    st.session_state.max_results = max_results
    
    similarity_threshold = st.sidebar.slider(
        "Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Minimum similarity score for results"
    )
    st.session_state.similarity_threshold = similarity_threshold


def render_overview():
    """Render the overview section."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Local RAG")
        st.markdown("""
        **Entity-centric retrieval** starting from specific legal provisions:
        - Vector similarity search on provision text
        - As-of temporal filtering for amendments
        - Relationship traversal (CITES, INTERPRETED_BY, etc.)
        - Citation tracking with Gazette references
        """)
        
        if st.button("Try Local RAG", key="nav_local"):
            st.switch_page("pages/1_Local.py")
    
    with col2:
        st.subheader("🌐 Global RAG")
        st.markdown("""
        **Community-based analysis** using graph structure:
        - GDS Louvain community detection
        - Community summary generation
        - Cluster-based legal topic discovery
        - Cross-jurisdictional pattern analysis
        """)
        
        if st.button("Try Global RAG", key="nav_global"):
            st.switch_page("pages/2_Global.py")
    
    st.subheader("🎪 DRIFT RAG")
    st.markdown("""
    **Hybrid approach** combining Global community signals with Local search:
    - Query-driven community selection
    - Multi-hop traversal from community centers
    - Evidence fusion across legal domains
    - Comprehensive coverage with citation grounding
    """)
    
    if st.button("Try DRIFT RAG", key="nav_drift"):
        st.switch_page("pages/3_DRIFT.py")


def render_health_check():
    """Render system health check."""
    st.subheader("🏥 System Health Check")
    
    with st.spinner("Checking system health..."):
        health_data = db.health_check()
    
    if health_data.get("status") == "healthy":
        st.success("✅ System is healthy!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Database Status", "Connected" if health_data.get("connected") else "Disconnected")
        
        with col2:
            st.metric("Total Nodes", health_data.get("node_count", 0))
        
        with col3:
            vector_status = "✅ Ready" if health_data.get("vector_index_exists") else "❌ Missing"
            st.metric("Vector Index", vector_status)
        
        with col4:
            community_nodes = health_data.get("community_nodes", 0)
            st.metric("Community Nodes", community_nodes)
        
        # Configuration check
        st.subheader("📋 Configuration Status")
        
        config_checks = [
            ("Neo4j Connection", settings.neo4j_uri, "🔗"),
            ("Azure OpenAI Endpoint", settings.azure_openai_endpoint, "🤖"),
            ("Embedding Deployment", settings.azure_openai_embedding_deployment, "📝"),
            ("Embedding Dimension", str(settings.embedding_dim), "📏"),
        ]
        
        for name, value, icon in config_checks:
            st.write(f"{icon} **{name}**: `{value[:50]}...`" if len(value) > 50 else f"{icon} **{name}**: `{value}`")
    
    else:
        st.error("❌ System health check failed!")
        st.error(f"Error: {health_data.get('error', 'Unknown error')}")
        
        st.subheader("🔧 Troubleshooting")
        st.markdown("""
        **Common issues:**
        1. Check Neo4j connection settings in `.env`
        2. Verify Azure OpenAI credentials
        3. Ensure database is seeded with `make seed`
        4. Run embedding generation with `python scripts/load_embeddings.py`
        """)


def render_database_stats():
    """Render database statistics."""
    st.subheader("📊 Database Statistics")
    
    try:
        with db.session() as session:
            # Node counts by label
            st.subheader("📦 Node Counts")
            
            node_queries = [
                ("Instruments", "MATCH (n:Instrument) RETURN count(n) as count"),
                ("Provisions", "MATCH (n:Provision) RETURN count(n) as count"),
                ("Judgments", "MATCH (n:Judgment) RETURN count(n) as count"),
                ("Events", "MATCH (n:Event) RETURN count(n) as count"),
                ("Gazette Issues", "MATCH (n:GazetteIssue) RETURN count(n) as count"),
            ]
            
            cols = st.columns(len(node_queries))
            for i, (label, query) in enumerate(node_queries):
                with cols[i]:
                    result = session.run(query)
                    count = result.single()["count"]
                    st.metric(label, count)
            
            # Relationship counts
            st.subheader("🔗 Relationship Counts")
            
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            rel_data = [(record["rel_type"], record["count"]) for record in rel_result]
            
            if rel_data:
                rel_cols = st.columns(min(len(rel_data), 4))
                for i, (rel_type, count) in enumerate(rel_data[:4]):
                    with rel_cols[i % 4]:
                        st.metric(rel_type.replace("_", " "), count)
            
            # Vector index status
            st.subheader("🎯 Vector Index Status")
            
            vector_result = session.run("""
                SHOW INDEXES 
                YIELD name, type, entityType, labelsOrTypes, properties, state
                WHERE type = 'VECTOR'
            """)
            
            vector_indexes = list(vector_result)
            if vector_indexes:
                for index in vector_indexes:
                    st.write(f"✅ **{index['name']}**: {index['state']} ({index['entityType']})")
            else:
                st.warning("No vector indexes found. Run `python scripts/load_embeddings.py`")
            
            # Embeddings status
            embedding_result = session.run("""
                MATCH (p:Provision)
                WITH count(p) as total, 
                     count(CASE WHEN p.embedding IS NOT NULL THEN 1 END) as with_embeddings
                RETURN total, with_embeddings, 
                       round(100.0 * with_embeddings / total, 1) as percentage
            """)
            
            embedding_stats = embedding_result.single()
            if embedding_stats:
                st.metric(
                    "Provisions with Embeddings",
                    f"{embedding_stats['with_embeddings']}/{embedding_stats['total']} ({embedding_stats['percentage']}%)"
                )
    
    except Exception as e:
        st.error(f"Error retrieving database statistics: {e}")


if __name__ == "__main__":
    main()
