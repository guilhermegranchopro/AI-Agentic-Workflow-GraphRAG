"""Path viewer component for rendering relationship paths."""
import streamlit as st
from typing import List, Dict, Any
from src.utils.formatting import format_path_display, format_date_range


def render_paths(paths: List[Dict[str, Any]], as_of: str) -> None:
    """
    Render path chips showing relationships between legal entities.
    
    Args:
        paths: List of path data from graph queries
        as_of: As-of date for temporal context
    """
    if not paths:
        st.info("No relationship paths found for the selected provision.")
        return
    
    st.subheader(f"🔗 Relationship Paths (as of {as_of})")
    
    # Group paths by relationship type for better organization
    paths_by_type = {}
    for path in paths:
        rel_type = path.get("relationship_type", "UNKNOWN")
        if rel_type not in paths_by_type:
            paths_by_type[rel_type] = []
        paths_by_type[rel_type].append(path)
    
    # Render each relationship type
    for rel_type, type_paths in paths_by_type.items():
        with st.expander(f"{rel_type.replace('_', ' ').title()} ({len(type_paths)} connections)", 
                        expanded=True):
            
            for i, path in enumerate(type_paths):
                render_single_path(path, i)


def render_single_path(path_data: Dict[str, Any], index: int) -> None:
    """Render a single relationship path as a visual chip."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Main path display
        path_display = format_path_display(path_data)
        st.markdown(path_display)
        
        # Additional relationship properties
        rel_props = path_data.get("relationship_props", {})
        if rel_props:
            prop_display = []
            for key, value in rel_props.items():
                if key.startswith('valid_'):
                    prop_display.append(f"{key}: {value}")
            
            if prop_display:
                st.caption(", ".join(prop_display))
    
    with col2:
        # Show details button
        if st.button("Details", key=f"path_details_{index}"):
            show_path_details(path_data)


def show_path_details(path_data: Dict[str, Any]) -> None:
    """Show detailed information about a path in a modal-style display."""
    neighbor = path_data.get("neighbor", {})
    rel_props = path_data.get("relationship_props", {})
    
    st.markdown("---")
    st.markdown("**Path Details:**")
    
    # Neighbor information
    if neighbor.get("text"):
        st.markdown(f"**Text:** {neighbor['text'][:300]}...")
    
    if neighbor.get("case_number"):
        st.markdown(f"**Case Number:** {neighbor['case_number']}")
    
    if neighbor.get("date"):
        st.markdown(f"**Date:** {neighbor['date']}")
    
    # Relationship properties
    if rel_props:
        st.markdown("**Relationship Properties:**")
        for key, value in rel_props.items():
            st.markdown(f"- {key}: {value}")


def render_path_network_view(paths: List[Dict[str, Any]]) -> None:
    """
    Render a simple network visualization of paths.
    Note: This is a simplified text-based network view.
    For a full graph visualization, you'd integrate with libraries like pyvis or networkx.
    """
    if not paths:
        return
    
    st.subheader("🕸️ Network View")
    
    # Create a simple adjacency representation
    nodes = set()
    edges = []
    
    for path in paths:
        neighbor = path.get("neighbor", {})
        rel_type = path.get("relationship_type", "RELATED")
        
        # Add nodes (simplified - in practice you'd get from the full path)
        nodes.add("Central Provision")
        if neighbor.get("case_number"):
            node_name = f"Judgment {neighbor['case_number']}"
        elif neighbor.get("number"):
            node_name = f"Article {neighbor['number']}"
        else:
            node_name = neighbor.get("id", "Unknown")
        
        nodes.add(node_name)
        edges.append((rel_type, node_name))
    
    # Display as text network
    st.markdown("**Central Provision** connects to:")
    for rel_type, target in edges:
        st.markdown(f"- **{rel_type}** → {target}")


def render_temporal_timeline(amendments: List[Dict[str, Any]]) -> None:
    """
    Render a timeline of amendments and changes.
    
    Args:
        amendments: List of amendment events with temporal data
    """
    if not amendments:
        return
    
    st.subheader("📅 Temporal Timeline")
    
    # Sort amendments by date
    sorted_amendments = sorted(
        amendments,
        key=lambda x: x.get("valid_from", "1900-01-01")
    )
    
    for amendment in sorted_amendments:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Date display
                valid_from = amendment.get("valid_from")
                valid_to = amendment.get("valid_to")
                date_range = format_date_range(valid_from, valid_to)
                st.markdown(f"**{date_range}**")
            
            with col2:
                # Amendment details
                st.markdown(f"**{amendment.get('kind', 'CHANGE')}**: {amendment.get('description', 'No description')}")
                
                if amendment.get("gazette_ref"):
                    st.caption(f"📰 Gazette: {amendment['gazette_ref']}")
            
            st.markdown("---")


def render_path_statistics(paths: List[Dict[str, Any]]) -> None:
    """Render statistics about the relationship paths."""
    if not paths:
        return
    
    st.subheader("📊 Path Statistics")
    
    # Count by relationship type
    rel_counts = {}
    for path in paths:
        rel_type = path.get("relationship_type", "UNKNOWN")
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    # Display as metrics
    cols = st.columns(len(rel_counts))
    for i, (rel_type, count) in enumerate(rel_counts.items()):
        with cols[i]:
            st.metric(
                label=rel_type.replace("_", " ").title(),
                value=count
            )
    
    # Total connections
    st.metric("Total Connections", len(paths))
