"""Global RAG page - community-based analysis using GDS Louvain."""
import streamlit as st
import sys
import os
import pandas as pd
from typing import Dict, Any, List

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.graph.tools import global_rag_communities
from src.graph.queries import communities_top, nodes_in_community
from src.db import db
from src.utils.formatting import format_community_summary


def main():
    """Main Global RAG page."""
    st.title("🌐 Global RAG - Community Analysis")
    st.markdown("GDS Louvain Community Detection → Summary Cards → Global Patterns")
    
    # Community analysis interface
    st.subheader("🏘️ Legal Community Structure")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Global RAG uses graph community detection to identify clusters of related legal entities.
        Communities are formed by provisions, judgments, and other legal documents that frequently 
        cite or reference each other.
        """)
    
    with col2:
        # Controls
        max_communities = st.slider("Max Communities", 5, 20, 10)
        
        if st.button("🔄 Run Community Detection", type="primary"):
            run_community_detection()
    
    # Display community analysis
    display_community_analysis(max_communities)


def run_community_detection():
    """Execute GDS Louvain community detection."""
    
    with st.spinner("Running GDS Louvain community detection..."):
        try:
            with db.session() as session:
                # Check if communities already exist
                check_result = session.run("""
                    MATCH (n) 
                    WHERE n.communityId IS NOT NULL 
                    RETURN count(n) as community_nodes
                """)
                existing_nodes = check_result.single()["community_nodes"]
                
                if existing_nodes > 0:
                    st.info(f"Found {existing_nodes} nodes with existing community assignments.")
                    
                    if st.button("Re-run Community Detection"):
                        execute_louvain(session)
                else:
                    execute_louvain(session)
                    
        except Exception as e:
            st.error(f"Error running community detection: {e}")


def execute_louvain(session):
    """Execute the Louvain algorithm."""
    try:
        # Project graph
        st.info("Projecting graph...")
        session.run("""
            CALL gds.graph.project(
                'legal-network-temp',
                ['Provision', 'Judgment'],
                {
                    CITES: {orientation: 'UNDIRECTED'},
                    INTERPRETED_BY: {orientation: 'UNDIRECTED'},
                    INTERPRETS: {orientation: 'UNDIRECTED'}
                }
            )
        """)
        
        # Run Louvain
        st.info("Running Louvain community detection...")
        result = session.run("""
            CALL gds.louvain.mutate(
                'legal-network-temp',
                {
                    mutateProperty: 'communityId',
                    includeIntermediateCommunities: false
                }
            )
            YIELD communityCount, modularity
            RETURN communityCount, modularity
        """)
        
        stats = result.single()
        st.success(f"✅ Found {stats['communityCount']} communities (modularity: {stats['modularity']:.3f})")
        
        # Write back to nodes
        st.info("Writing community IDs back to nodes...")
        session.run("""
            CALL gds.graph.nodeProperties.write(
                'legal-network-temp',
                ['communityId']
            )
        """)
        
        # Clean up
        session.run("CALL gds.graph.drop('legal-network-temp')")
        
        st.success("🎉 Community detection completed!")
        
    except Exception as e:
        # Clean up on error
        try:
            session.run("CALL gds.graph.drop('legal-network-temp')")
        except:
            pass
        raise e


def display_community_analysis(max_communities: int):
    """Display the community analysis results."""
    
    try:
        # Get global community data
        with st.spinner("Loading community analysis..."):
            global_data = global_rag_communities(max_communities)
        
        if "error" in global_data:
            st.error(f"Error loading communities: {global_data['error']}")
            return
        
        communities = global_data.get("communities", [])
        total_communities = global_data.get("total_communities", 0)
        
        if not communities:
            st.warning("No communities found. Please run community detection first.")
            return
        
        # Overview metrics
        display_community_overview(communities, total_communities)
        
        # Community details
        display_community_details(communities)
        
        # Community comparison
        display_community_comparison(communities)
        
    except Exception as e:
        st.error(f"Error displaying community analysis: {e}")


def display_community_overview(communities: List[Dict[str, Any]], total_communities: int):
    """Display community overview metrics."""
    
    st.subheader("📊 Community Overview")
    
    # Calculate statistics
    total_nodes = sum(comm["size"] for comm in communities)
    avg_size = total_nodes / len(communities) if communities else 0
    largest_community = max(communities, key=lambda x: x["size"]) if communities else None
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Communities", total_communities)
    
    with col2:
        st.metric("Nodes in Top Communities", total_nodes)
    
    with col3:
        st.metric("Average Community Size", f"{avg_size:.1f}")
    
    with col4:
        if largest_community:
            st.metric("Largest Community", f"{largest_community['size']} nodes")
    
    # Community size distribution
    if communities:
        st.subheader("📈 Community Size Distribution")
        
        sizes = [comm["size"] for comm in communities]
        size_df = pd.DataFrame({
            "Community ID": [comm["id"] for comm in communities],
            "Size": sizes,
            "Types": [", ".join(comm["node_types"]) for comm in communities]
        })
        
        st.bar_chart(size_df.set_index("Community ID")["Size"])


def display_community_details(communities: List[Dict[str, Any]]):
    """Display detailed information for each community."""
    
    st.subheader("🏘️ Community Details")
    
    # Community selection
    selected_community = st.selectbox(
        "Select a community to explore:",
        options=range(len(communities)),
        format_func=lambda i: f"Community {communities[i]['id']} ({communities[i]['size']} nodes)"
    )
    
    if selected_community is not None:
        community = communities[selected_community]
        display_single_community(community)


def display_single_community(community: Dict[str, Any]):
    """Display details for a single community."""
    
    community_id = community["id"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### Community {community_id}")
        
        # Community summary
        summary = format_community_summary(community)
        st.markdown(summary)
        
        # Sample nodes
        sample_nodes = community.get("sample_nodes", [])
        if sample_nodes:
            st.markdown("**Sample Nodes:**")
            
            for node_data in sample_nodes:
                node = node_data.get("node", {})
                node_type = node_data.get("node_type", "")
                
                with st.expander(f"{node_type}: {node.get('id', 'Unknown')}", expanded=False):
                    if node_type == "Provision":
                        if node.get("number"):
                            st.markdown(f"**Article:** {node['number']}")
                        if node.get("article_title"):
                            st.markdown(f"**Title:** {node['article_title']}")
                        if node.get("text"):
                            st.markdown(f"**Text:** {node['text'][:200]}...")
                    
                    elif node_type == "Judgment":
                        if node.get("case_number"):
                            st.markdown(f"**Case:** {node['case_number']}")
                        if node.get("date"):
                            st.markdown(f"**Date:** {node['date']}")
                    
                    st.markdown(f"**ID:** `{node.get('id', 'Unknown')}`")
    
    with col2:
        # Community actions
        st.markdown("**Actions:**")
        
        if st.button("View All Nodes", key=f"view_all_{community_id}"):
            view_all_community_nodes(community_id)
        
        if st.button("Export Community", key=f"export_{community_id}"):
            export_community_data(community)
        
        if st.button("Find Similar Communities", key=f"similar_{community_id}"):
            find_similar_communities(community)


def view_all_community_nodes(community_id: int):
    """Display all nodes in a community."""
    
    st.subheader(f"🔍 All Nodes in Community {community_id}")
    
    try:
        all_nodes = nodes_in_community(community_id, 50)  # Get up to 50 nodes
        
        if not all_nodes:
            st.info("No nodes found in this community.")
            return
        
        # Group by node type
        nodes_by_type = {}
        for node_data in all_nodes:
            node_type = node_data.get("node_type", "Unknown")
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node_data)
        
        # Display by type
        for node_type, nodes in nodes_by_type.items():
            with st.expander(f"{node_type} ({len(nodes)} nodes)", expanded=True):
                for node_data in nodes:
                    node = node_data.get("node", {})
                    
                    if node_type == "Provision":
                        display_text = f"Article {node.get('number', 'Unknown')}"
                        if node.get("article_title"):
                            display_text += f": {node['article_title']}"
                    elif node_type == "Judgment":
                        display_text = node.get("case_number", node.get("id", "Unknown"))
                    else:
                        display_text = node.get("id", "Unknown")
                    
                    st.markdown(f"- {display_text}")
    
    except Exception as e:
        st.error(f"Error loading community nodes: {e}")


def export_community_data(community: Dict[str, Any]):
    """Export community data."""
    
    st.subheader("📤 Export Community Data")
    
    import json
    
    # Create export data
    export_data = {
        "community_id": community["id"],
        "size": community["size"],
        "node_types": community["node_types"],
        "summary": community["summary"],
        "sample_nodes": community["sample_nodes"],
        "export_timestamp": str(pd.Timestamp.now())
    }
    
    # Display as JSON
    json_str = json.dumps(export_data, indent=2, default=str)
    st.code(json_str, language="json")
    
    # Download button would go here in a full implementation
    st.info("Copy the JSON above to save community data.")


def find_similar_communities(community: Dict[str, Any]):
    """Find communities with similar characteristics."""
    
    st.subheader("🔍 Similar Communities")
    
    # This would implement similarity analysis
    # For now, show a placeholder
    st.info(f"Similar communities to Community {community['id']} would be shown here.")
    st.markdown("""
    **Similarity could be based on:**
    - Node type composition
    - Size similarity  
    - Shared connections between communities
    - Topic similarity (if using text analysis)
    """)


def display_community_comparison(communities: List[Dict[str, Any]]):
    """Display comparison between communities."""
    
    st.subheader("⚖️ Community Comparison")
    
    if len(communities) < 2:
        st.info("Need at least 2 communities for comparison.")
        return
    
    # Select communities to compare
    compare_options = [f"Community {comm['id']} ({comm['size']} nodes)" for comm in communities]
    
    col1, col2 = st.columns(2)
    
    with col1:
        comm1_idx = st.selectbox("First Community", range(len(communities)), 
                                format_func=lambda i: compare_options[i])
    
    with col2:
        comm2_idx = st.selectbox("Second Community", range(len(communities)), 
                                format_func=lambda i: compare_options[i],
                                index=1 if len(communities) > 1 else 0)
    
    if comm1_idx != comm2_idx:
        compare_communities(communities[comm1_idx], communities[comm2_idx])


def compare_communities(comm1: Dict[str, Any], comm2: Dict[str, Any]):
    """Compare two communities side by side."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Community {comm1['id']}**")
        st.markdown(f"Size: {comm1['size']} nodes")
        st.markdown(f"Types: {', '.join(comm1['node_types'])}")
        st.markdown(f"Summary: {comm1['summary']}")
    
    with col2:
        st.markdown(f"**Community {comm2['id']}**")
        st.markdown(f"Size: {comm2['size']} nodes")
        st.markdown(f"Types: {', '.join(comm2['node_types'])}")
        st.markdown(f"Summary: {comm2['summary']}")
    
    # Comparison metrics
    st.markdown("**Comparison:**")
    
    size_diff = abs(comm1['size'] - comm2['size'])
    type_overlap = set(comm1['node_types']) & set(comm2['node_types'])
    
    st.markdown(f"- Size difference: {size_diff} nodes")
    st.markdown(f"- Shared node types: {', '.join(type_overlap) if type_overlap else 'None'}")


if __name__ == "__main__":
    main()
