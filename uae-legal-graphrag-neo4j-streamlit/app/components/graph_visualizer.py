"""Graph visualization component for the UAE Legal GraphRAG application."""
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from typing import List, Dict, Any, Tuple
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from src.db import db


def create_legal_graph_visualization(
    max_nodes: int = 50,
    include_relationships: List[str] = None,
    layout: str = "hierarchical"
) -> str:
    """
    Create an interactive graph visualization of the legal knowledge graph.
    
    Args:
        max_nodes: Maximum number of nodes to display
        include_relationships: List of relationship types to include
        layout: Layout algorithm ('hierarchical', 'physics', 'clustered')
        
    Returns:
        HTML file path for the generated graph
    """
    if include_relationships is None:
        include_relationships = ["HAS_PROVISION", "CITES", "INTERPRETED_BY", "AMENDED_BY"]
    
    # Query the graph data
    graph_data = fetch_graph_data(max_nodes, include_relationships)
    
    # Create PyVis network
    net = Network(
        height="600px", 
        width="100%", 
        bgcolor="#1e1e1e", 
        font_color="white",
        directed=True
    )
    
    # Configure physics
    if layout == "physics":
        net.set_options("""
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100}
          }
        }
        """)
    elif layout == "hierarchical":
        net.set_options("""
        var options = {
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "UD",
              "sortMethod": "directed"
            }
          },
          "physics": {"enabled": false}
        }
        """)
    
    # Add nodes with different colors for different types
    node_colors = {
        "Instrument": "#ff6b6b",  # Red for legal instruments
        "Provision": "#4ecdc4",   # Teal for provisions
        "Court": "#45b7d1",       # Blue for courts
        "Judgment": "#f9ca24",    # Yellow for judgments
        "GazetteIssue": "#6c5ce7", # Purple for gazette issues
        "Event": "#fd79a8"        # Pink for events
    }
    
    for node in graph_data["nodes"]:
        node_type = node["labels"][0] if node["labels"] else "Unknown"
        color = node_colors.get(node_type, "#95a5a6")
        
        # Create node title with details
        title = f"<b>{node_type}</b><br>"
        if "title" in node["properties"]:
            title += f"Title: {node['properties']['title']}<br>"
        if "number" in node["properties"]:
            title += f"Number: {node['properties']['number']}<br>"
        if "text" in node["properties"]:
            text = node["properties"]["text"][:100] + "..." if len(node["properties"]["text"]) > 100 else node["properties"]["text"]
            title += f"Text: {text}<br>"
        
        # Add community info if available
        if "communityId" in node["properties"]:
            title += f"Community: {node['properties']['communityId']}<br>"
        
        net.add_node(
            node["id"],
            label=node["properties"].get("id", str(node["id"])),
            color=color,
            title=title,
            size=20 if node_type == "Provision" else 15
        )
    
    # Add edges with different colors for different relationships
    edge_colors = {
        "HAS_PROVISION": "#3498db",
        "CITES": "#e74c3c",
        "INTERPRETED_BY": "#f39c12",
        "AMENDED_BY": "#9b59b6",
        "PUBLISHED_IN": "#1abc9c",
        "AFFECTS": "#e67e22",
        "ISSUED": "#2ecc71"
    }
    
    for edge in graph_data["edges"]:
        rel_type = edge["type"]
        color = edge_colors.get(rel_type, "#bdc3c7")
        
        # Create edge title with relationship details
        title = f"<b>{rel_type}</b><br>"
        if edge["properties"]:
            for key, value in edge["properties"].items():
                title += f"{key}: {value}<br>"
        
        net.add_edge(
            edge["source"],
            edge["target"],
            label=rel_type,
            color=color,
            title=title,
            arrows="to",
            width=2
        )
    
    # Generate HTML file
    html_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w')
    net.save_graph(html_file.name)
    html_file.close()
    
    return html_file.name


def fetch_graph_data(max_nodes: int, include_relationships: List[str]) -> Dict[str, Any]:
    """
    Fetch graph data from Neo4j for visualization.
    
    Args:
        max_nodes: Maximum number of nodes to fetch
        include_relationships: List of relationship types to include
        
    Returns:
        Dictionary with nodes and edges data
    """
    rel_filter = "'" + "', '".join(include_relationships) + "'"
    
    query = f"""
    MATCH (n)
    WITH n LIMIT {max_nodes}
    OPTIONAL MATCH (n)-[r]->(m)
    WHERE type(r) IN [{rel_filter}]
    RETURN 
        collect(DISTINCT {{
            id: elementId(n),
            labels: labels(n),
            properties: properties(n)
        }}) + collect(DISTINCT {{
            id: elementId(m),
            labels: labels(m),
            properties: properties(m)
        }}) as nodes,
        collect(DISTINCT {{
            source: elementId(n),
            target: elementId(m),
            type: type(r),
            properties: properties(r)
        }}) as edges
    """
    
    with db.session() as session:
        result = session.run(query)
        data = result.single()
        
        # Filter out null nodes and deduplicate by ID
        all_nodes = [node for node in data["nodes"] if node["id"] is not None]
        edges = [edge for edge in data["edges"] if edge["source"] is not None and edge["target"] is not None]
        
        # Deduplicate nodes by ID
        seen_ids = set()
        unique_nodes = []
        for node in all_nodes:
            if node["id"] not in seen_ids:
                seen_ids.add(node["id"])
                unique_nodes.append(node)
        
        return {
            "nodes": unique_nodes,
            "edges": edges
        }


def create_agraph_visualization(max_nodes: int = 20, include_relationships: List[str] = None) -> None:
    """
    Create a streamlit-agraph visualization of the legal knowledge graph.
    
    Args:
        max_nodes: Maximum number of nodes to display
        include_relationships: List of relationship types to include
    """
    if include_relationships is None:
        include_relationships = ["HAS_PROVISION", "CITES", "INTERPRETED_BY"]
    
    # Fetch graph data with the specified parameters
    graph_data = fetch_graph_data(max_nodes, include_relationships)
    
    if not graph_data["nodes"]:
        st.warning("No nodes found with the current settings. Try adjusting the parameters.")
        return None
    
    # Debug: Show node count
    st.info(f"📊 Displaying {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
    
    # Create nodes and edges for agraph
    nodes = []
    edges = []
    
    # Color mapping for node types
    node_colors = {
        "Instrument": "#FF6B6B",
        "Provision": "#4ECDC4",
        "Court": "#45B7D1",
        "Judgment": "#F9CA24",
        "GazetteIssue": "#6C5CE7"
    }
    
    # Add nodes
    node_ids = set()
    for node in graph_data["nodes"]:
        node_type = node["labels"][0] if node["labels"] else "Unknown"
        color = node_colors.get(node_type, "#95A5A6")
        
        label = node["properties"].get("id", str(node["id"]))
        if len(label) > 15:
            label = label[:12] + "..."
        
        node_id = str(node["id"])
        if node_id not in node_ids:
            node_ids.add(node_id)
            nodes.append(Node(
                id=node_id,
                label=label,
                size=25,
                color=color
            ))
    
    # Add edges (deduplicate by source-target-type combination)
    edge_signatures = set()
    for edge in graph_data["edges"]:
        source = str(edge["source"])
        target = str(edge["target"])
        edge_type = edge["type"]
        
        # Only add edge if both nodes exist and edge is unique
        edge_sig = f"{source}-{target}-{edge_type}"
        if source in node_ids and target in node_ids and edge_sig not in edge_signatures:
            edge_signatures.add(edge_sig)
            edges.append(Edge(
                source=source,
                target=target,
                label=edge_type,
                color="#BDC3C7"
            ))
    
    # Configure the graph
    config = Config(
        width=800,
        height=600,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7CA18",
        collapsible=False
    )
    
    # Display final stats
    st.success(f"✅ Graph ready: {len(nodes)} nodes, {len(edges)} edges")
    
    # Render the graph
    return agraph(nodes=nodes, edges=edges, config=config)


def render_graph_controls() -> Tuple[int, List[str], str]:
    """
    Render controls for graph visualization parameters.
    
    Returns:
        Tuple of (max_nodes, relationships, layout)
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_nodes = st.slider(
            "Max Nodes",
            min_value=10,
            max_value=100,
            value=30,
            help="Maximum number of nodes to display",
            key="graph_viz_max_nodes"
        )
    
    with col2:
        available_relationships = [
            "HAS_PROVISION",
            "CITES",
            "INTERPRETED_BY",
            "AMENDED_BY",
            "PUBLISHED_IN",
            "AFFECTS",
            "ISSUED"
        ]
        
        relationships = st.multiselect(
            "Relationships",
            available_relationships,
            default=["HAS_PROVISION", "CITES", "INTERPRETED_BY"],
            help="Select which relationship types to display",
            key="graph_viz_relationships"
        )
    
    with col3:
        layout = st.selectbox(
            "Layout",
            ["hierarchical", "physics", "clustered"],
            help="Graph layout algorithm",
            key="graph_viz_layout"
        )
    
    return max_nodes, relationships, layout


def render_graph_statistics(graph_data: Dict[str, Any]) -> None:
    """
    Render statistics about the graph.
    
    Args:
        graph_data: Dictionary with nodes and edges data
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Nodes", len(graph_data["nodes"]))
    
    with col2:
        st.metric("Total Edges", len(graph_data["edges"]))
    
    with col3:
        # Count node types
        node_types = {}
        for node in graph_data["nodes"]:
            node_type = node["labels"][0] if node["labels"] else "Unknown"
            node_types[node_type] = node_types.get(node_type, 0) + 1
        st.metric("Node Types", len(node_types))
    
    with col4:
        # Count relationship types
        rel_types = set(edge["type"] for edge in graph_data["edges"])
        st.metric("Relationship Types", len(rel_types))
    
    # Show detailed breakdown
    with st.expander("📊 Detailed Statistics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Node Types:**")
            for node_type, count in node_types.items():
                st.markdown(f"- {node_type}: {count}")
        
        with col2:
            st.markdown("**Relationship Types:**")
            rel_counts = {}
            for edge in graph_data["edges"]:
                rel_type = edge["type"]
                rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
            
            for rel_type, count in rel_counts.items():
                st.markdown(f"- {rel_type}: {count}")


def render_legend() -> None:
    """Render a legend for the graph visualization."""
    st.markdown("### 🎨 Graph Legend")
    
    legend_data = [
        ("🔴 Instrument", "Legal instruments (Constitution, Civil Code, etc.)"),
        ("🟢 Provision", "Legal provisions and articles"),
        ("🔵 Court", "Courts and judicial bodies"),
        ("🟡 Judgment", "Court decisions and judgments"),
        ("🟣 Gazette Issue", "Official gazette publications"),
        ("🟠 Event", "Legal events (amendments, changes)")
    ]
    
    for color_label, description in legend_data:
        st.markdown(f"**{color_label}**: {description}")
    
    st.markdown("---")
    st.markdown("**Relationship Types:**")
    st.markdown("- **HAS_PROVISION**: Instrument contains provision")
    st.markdown("- **CITES**: One provision cites another")
    st.markdown("- **INTERPRETED_BY**: Provision interpreted by judgment")
    st.markdown("- **AMENDED_BY**: Provision amended by event")
    st.markdown("- **PUBLISHED_IN**: Published in gazette issue")
