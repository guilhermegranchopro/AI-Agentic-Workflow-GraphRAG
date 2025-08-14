"""Citations panel component for showing source information."""
import streamlit as st
from typing import Dict, Any, List
from src.utils.formatting import format_citation_panel, format_provision_display


def render_citations_panel(results: List[Dict[str, Any]], title: str = "📚 Citations & Sources") -> None:
    """
    Render a citations panel showing Gazette numbers, dates, node IDs, and links.
    
    Args:
        results: Query results containing provision and context data
        title: Panel title
    """
    if not results:
        st.info("No citations available.")
        return
    
    with st.expander(title, expanded=False):
        for i, result in enumerate(results):
            render_single_citation(result, i)
            if i < len(results) - 1:
                st.markdown("---")


def render_single_citation(result: Dict[str, Any], index: int) -> None:
    """Render citation information for a single result."""
    provision = result.get("provision", {})
    context = result.get("context", {})
    score = result.get("score")
    
    # Citation header
    provision_id = provision.get("id", f"result-{index}")
    st.markdown(f"**Citation {index + 1}: {provision_id}**")
    
    # Format and display citation panel
    citation_info = format_citation_panel(context)
    if citation_info:
        st.markdown(citation_info)
    
    # Relevance score if available
    if score is not None:
        st.markdown(f"**Relevance Score:** {score:.3f}")
    
    # Preview of provision text
    if provision.get("text"):
        preview_text = provision["text"][:200]
        if len(provision["text"]) > 200:
            preview_text += "..."
        st.markdown(f"**Preview:** {preview_text}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Full Text", key=f"view_full_{index}"):
            show_full_provision(provision, context)
    
    with col2:
        if st.button("Copy Citation", key=f"copy_cite_{index}"):
            copy_citation_text(provision, context)
    
    with col3:
        if context.get("gazette"):
            gazette = context["gazette"]
            gazette_info = f"Gazette No. {gazette.get('number', 'Unknown')}, {gazette.get('date', 'Unknown date')}"
            st.caption(f"📰 {gazette_info}")


def show_full_provision(provision: Dict[str, Any], context: Dict[str, Any]) -> None:
    """Display the full provision text in an expanded view."""
    st.markdown("---")
    st.markdown("### Full Provision Text")
    
    # Format and display the complete provision
    full_display = format_provision_display(provision, context)
    st.markdown(full_display)
    
    # Additional metadata
    if provision.get("id"):
        st.code(f"Provision ID: {provision['id']}", language="text")


def copy_citation_text(provision: Dict[str, Any], context: Dict[str, Any]) -> None:
    """Generate and display citation text for copying."""
    citation_parts = []
    
    # Article reference
    if provision.get("number"):
        citation_parts.append(f"Article {provision['number']}")
    
    # Instrument title
    if context.get("instrument"):
        instrument = context["instrument"]
        title = instrument.get("title", "Unknown Instrument")
        if instrument.get("year"):
            title += f" ({instrument['year']})"
        citation_parts.append(title)
    
    # Gazette reference
    if context.get("gazette"):
        gazette = context["gazette"]
        gazette_ref = f"Official Gazette No. {gazette.get('number', 'Unknown')}"
        if gazette.get("date"):
            gazette_ref += f", {gazette['date']}"
        citation_parts.append(gazette_ref)
    
    citation_text = ", ".join(citation_parts)
    
    st.code(citation_text, language="text")
    st.success("Citation text displayed above - you can copy it manually.")


def render_source_quality_indicators(results: List[Dict[str, Any]]) -> None:
    """Display quality indicators for the sources."""
    if not results:
        return
    
    st.subheader("🎯 Source Quality")
    
    # Calculate quality metrics
    scores = [r.get("score", 0) for r in results if r.get("score") is not None]
    search_types = [r.get("search_type", "unknown") for r in results]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if scores:
            avg_score = sum(scores) / len(scores)
            st.metric("Average Relevance", f"{avg_score:.3f}")
        else:
            st.metric("Average Relevance", "N/A")
    
    with col2:
        vector_count = search_types.count("vector")
        st.metric("Vector Search Results", vector_count)
    
    with col3:
        text_count = search_types.count("fulltext")
        st.metric("Text Search Results", text_count)


def render_export_options(results: List[Dict[str, Any]]) -> None:
    """Render export options for citations and sources."""
    if not results:
        return
    
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as Bibliography"):
            bibliography = generate_bibliography(results)
            st.text_area("Bibliography (copy text below):", bibliography, height=200)
    
    with col2:
        if st.button("Export as JSON"):
            import json
            json_data = json.dumps(results, indent=2, default=str)
            st.code(json_data, language="json")


def generate_bibliography(results: List[Dict[str, Any]]) -> str:
    """Generate a formatted bibliography from results."""
    bibliography_entries = []
    
    for i, result in enumerate(results):
        provision = result.get("provision", {})
        context = result.get("context", {})
        
        entry_parts = []
        
        # Author/Source (instrument)
        if context.get("instrument"):
            instrument = context["instrument"]
            entry_parts.append(f"United Arab Emirates. {instrument.get('title', 'Unknown Instrument')}")
            
            if instrument.get("number") and instrument.get("year"):
                entry_parts.append(f"No. {instrument['number']}/{instrument['year']}")
        
        # Article reference
        if provision.get("number"):
            entry_parts.append(f"Art. {provision['number']}")
        
        # Publication info (gazette)
        if context.get("gazette"):
            gazette = context["gazette"]
            pub_info = f"Official Gazette No. {gazette.get('number', 'Unknown')}"
            if gazette.get("date"):
                pub_info += f", {gazette['date']}"
            entry_parts.append(pub_info)
        
        # Combine entry
        if entry_parts:
            bibliography_entries.append(f"{i+1}. {'. '.join(entry_parts)}.")
    
    return "\n\n".join(bibliography_entries)


def render_related_documents(provision_id: str) -> None:
    """Render related documents and cross-references."""
    st.subheader("🔗 Related Documents")
    
    # This would typically query for related documents
    # For now, show placeholder
    st.info(f"Related documents for {provision_id} would be shown here.")
    
    # In a full implementation, you might show:
    # - Other provisions in the same instrument
    # - Provisions that cite this one
    # - Court cases that reference this provision
    # - Commentary or analysis documents
