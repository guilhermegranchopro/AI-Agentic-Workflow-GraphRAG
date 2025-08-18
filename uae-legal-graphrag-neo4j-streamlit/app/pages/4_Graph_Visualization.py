"""Graph Visualization page - Interactive Neo4j Knowledge Graph Explorer."""
import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components.graph_visualizer import (
    create_legal_graph_visualization, 
    create_agraph_visualization,
    render_graph_controls,
    fetch_graph_data,
    render_graph_statistics,
    render_legend
)


def main():
    """Main graph visualization page."""
    st.set_page_config(
        page_title="Graph Visualization",
        page_icon="🕸️",
        layout="wide"
    )
    
    st.title("🕸️ Legal Knowledge Graph Visualization")
    st.markdown("**Interactive exploration of the UAE Legal GraphRAG knowledge graph**")
    
    # Information about the visualization
    st.info("""
    🎯 **What you can explore:**
    - Legal instruments (Constitution, Civil Code, etc.)
    - Legal provisions and their relationships
    - Court decisions and interpretations
    - Citation networks and amendments
    - Community structures from graph analysis
    """)
    
    # Graph visualization tabs
    tab1, tab2, tab3 = st.tabs(["🌐 Interactive Graph", "📊 Graph Analytics", "🎨 Legend & Help"])
    
    # Global controls for all tabs
    st.markdown("### ⚙️ Visualization Controls")
    max_nodes, relationships, layout = render_graph_controls()
    
    with tab1:
        render_interactive_graph(max_nodes, relationships, layout)
    
    with tab2:
        render_graph_analytics(max_nodes, relationships, layout)
    
    with tab3:
        render_legend_and_help()


def render_interactive_graph(max_nodes, relationships, layout):
    """Render the interactive graph visualization."""
    st.subheader("🌐 Interactive Knowledge Graph")
    
    if not relationships:
        st.warning("Please select at least one relationship type to display the graph.")
        return
    
    # Visualization type selection
    viz_type = st.radio(
        "Visualization Engine",
        ["PyVis (Full Featured)", "Agraph (Lightweight)"],
        help="PyVis provides more features but may be slower for large graphs",
        key="graph_viz_engine_type"
    )
    
    # Generate graph button
    if st.button("🚀 Generate Graph Visualization", type="primary", key="generate_graph_viz"):
        with st.spinner("🕸️ Building knowledge graph visualization..."):
            try:
                if viz_type == "PyVis (Full Featured)":
                    # Create PyVis visualization
                    html_file = create_legal_graph_visualization(
                        max_nodes=max_nodes,
                        include_relationships=relationships,
                        layout=layout
                    )
                    
                    # Display the graph
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    st.components.v1.html(html_content, height=650)
                    
                    # Cleanup
                    os.unlink(html_file)
                    
                else:
                    # Create Agraph visualization
                    st.markdown("### Interactive Graph (Click and drag nodes)")
                    selected_node = create_agraph_visualization(max_nodes, relationships)
                    
                    if selected_node:
                        st.markdown(f"**Selected Node:** {selected_node}")
                        # Could add more details about the selected node here
                
                st.success("✅ Graph visualization generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating graph: {str(e)}")
                st.markdown("**Troubleshooting:**")
                st.markdown("- Check that Neo4j is running and accessible")
                st.markdown("- Verify that there is data in the database")
                st.markdown("- Try reducing the number of nodes or relationships")


def render_graph_analytics(max_nodes, relationships, layout):
    """Render graph analytics and statistics."""
    st.subheader("📊 Graph Analytics & Statistics")
    
    # Fetch current graph statistics
    try:
        if st.button("🔍 Analyze Current Graph", key="analyze_graph_button"):
            with st.spinner("📈 Analyzing graph structure..."):
                graph_data = fetch_graph_data(max_nodes, relationships)
                
                # Basic statistics
                st.markdown("### 📈 Basic Statistics")
                render_graph_statistics(graph_data)
                
                # Community analysis
                st.markdown("### 🏘️ Community Analysis")
                from src.graph.queries import communities_top
                
                try:
                    communities = communities_top(10)
                    if not communities.empty:
                        st.dataframe(
                            communities,
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No communities detected. Run community detection first.")
                except Exception as e:
                    st.warning(f"Community analysis not available: {str(e)}")
                
                # Node degree analysis
                st.markdown("### 🔗 Connectivity Analysis")
                
                # Calculate node degrees
                node_degrees = {}
                for edge in graph_data["edges"]:
                    source = edge["source"]
                    target = edge["target"]
                    node_degrees[source] = node_degrees.get(source, 0) + 1
                    node_degrees[target] = node_degrees.get(target, 0) + 1
                
                if node_degrees:
                    import pandas as pd
                    
                    # Find node details
                    node_lookup = {node["id"]: node for node in graph_data["nodes"]}
                    
                    degree_data = []
                    for node_id, degree in sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:10]:
                        if node_id in node_lookup:
                            node = node_lookup[node_id]
                            node_type = node["labels"][0] if node["labels"] else "Unknown"
                            node_label = node["properties"].get("id", str(node_id))
                            degree_data.append({
                                "Node": node_label,
                                "Type": node_type,
                                "Connections": degree
                            })
                    
                    if degree_data:
                        df = pd.DataFrame(degree_data)
                        st.markdown("**Top 10 Most Connected Nodes:**")
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Degree distribution
                    degrees = list(node_degrees.values())
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Avg Connections", f"{sum(degrees)/len(degrees):.1f}")
                    with col2:
                        st.metric("Max Connections", max(degrees))
                    with col3:
                        st.metric("Min Connections", min(degrees))
                
    except Exception as e:
        st.error(f"❌ Error analyzing graph: {str(e)}")


def render_legend_and_help():
    """Render legend and help information."""
    col1, col2 = st.columns(2)
    
    with col1:
        render_legend()
    
    with col2:
        st.markdown("### 🆘 Help & Tips")
        
        st.markdown("**🎮 Interaction Tips:**")
        st.markdown("- **PyVis**: Click and drag nodes to rearrange")
        st.markdown("- **PyVis**: Hover over nodes/edges for details")
        st.markdown("- **PyVis**: Use mouse wheel to zoom")
        st.markdown("- **Agraph**: Click nodes to select and view details")
        
        st.markdown("**⚙️ Configuration Tips:**")
        st.markdown("- Start with fewer nodes (20-30) for better performance")
        st.markdown("- **Hierarchical** layout works best for citation networks")
        st.markdown("- **Physics** layout good for exploring communities")
        st.markdown("- Include **HAS_PROVISION** + **CITES** for core structure")
        
        st.markdown("**🐛 Troubleshooting:**")
        st.markdown("- If graph doesn't load, check Neo4j connection")
        st.markdown("- Large graphs may take time to render")
        st.markdown("- Try reducing nodes/relationships if slow")
        st.markdown("- Use 'Lightweight' mode for quick exploration")
        
        st.markdown("**📚 About the Data:**")
        st.markdown("- Nodes represent legal entities")
        st.markdown("- Edges show relationships between entities")
        st.markdown("- Colors indicate different entity types")
        st.markdown("- Communities show related legal concepts")


if __name__ == "__main__":
    main()
