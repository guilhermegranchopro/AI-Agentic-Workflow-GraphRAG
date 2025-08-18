"""Local RAG page - entity-centric search with temporal filtering."""
import streamlit as st
import sys
import os
from typing import List, Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.graph.tools import semantic_search_provisions, local_rag_query, combine_text_and_vector_search
from src.safety.grounding import validate_answer_grounding, get_fallback_sources_only
from components.path_viewer import render_paths, render_temporal_timeline, render_path_statistics
from components.citations_panel import render_citations_panel, render_source_quality_indicators


def main():
    """Main Local RAG page."""
    st.title("🎯 Local RAG - Entity-Centric Search")
    st.markdown("Query → Embed → KNN → As-of Traversal → Paths")
    
    # Get global settings from session state
    as_of_date = st.session_state.get('as_of_date')
    max_results = st.session_state.get('max_results', 5)
    
    if not as_of_date:
        st.warning("Please set the as-of date in the sidebar on the Home page.")
        return
    
    # Search interface
    st.subheader("🔍 Search Legal Provisions")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query_text = st.text_input(
            "Enter your legal query:",
            placeholder="e.g., civil liability compensation damage",
            help="Enter natural language query to find relevant legal provisions"
        )
    
    with col2:
        search_mode = st.selectbox(
            "Search Mode",
            ["Vector Only", "Text Only", "Combined"],
            help="Choose search method"
        )
    
    # Advanced options
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            k_results = st.slider("Initial Results", 1, 10, max_results)
            relationship_types = st.multiselect(
                "Relationship Types",
                ["CITES", "INTERPRETED_BY", "AMENDED_BY", "AFFECTS", "IMPLEMENTS"],
                default=["CITES", "INTERPRETED_BY", "AMENDED_BY"],
                help="Types of relationships to traverse"
            )
        
        with col2:
            include_amendments = st.checkbox("Include Amendments", value=True)
            show_statistics = st.checkbox("Show Path Statistics", value=True)
    
    # Search execution
    if query_text:
        search_and_display_results(
            query_text, search_mode, k_results, relationship_types,
            include_amendments, show_statistics, as_of_date
        )


def search_and_display_results(
    query_text: str,
    search_mode: str,
    k_results: int,
    relationship_types: List[str],
    include_amendments: bool,
    show_statistics: bool,
    as_of_date
):
    """Execute search and display results."""
    
    with st.spinner("Searching legal provisions..."):
        # Execute search based on mode
        if search_mode == "Vector Only":
            search_results = semantic_search_provisions(query_text, k_results)
        elif search_mode == "Text Only":
            from src.graph.queries import search_provisions_by_text
            text_results = search_provisions_by_text(query_text, k_results)
            search_results = []
            for result in text_results:
                search_results.append({
                    "provision": result["provision"],
                    "score": result["score"],
                    "search_type": "fulltext"
                })
        else:  # Combined
            search_results = combine_text_and_vector_search(query_text, k_results)
    
    if not search_results:
        st.warning("No relevant provisions found for your query.")
        return
    
    # Display search results
    st.subheader(f"📋 Search Results ({len(search_results)} found)")
    
    # Show source quality indicators
    render_source_quality_indicators(search_results)
    
    # Top results selection
    st.subheader("🎯 Top Provisions")
    
    selected_provisions = []
    
    for i, result in enumerate(search_results[:3]):  # Show top 3
        provision = result["provision"]
        score = result.get("score", 0)
        
        with st.expander(f"Result {i+1}: Article {provision.get('number', 'Unknown')} (Score: {score:.3f})", expanded=True):
            # Display provision details
            st.markdown(f"**Text:** {provision.get('text', 'No text available')}")
            st.markdown(f"**Title:** {provision.get('article_title', 'No title')}")
            st.markdown(f"**ID:** `{provision.get('id', 'Unknown')}`")
            
            # Selection checkbox
            if st.checkbox(f"Explore relationships for this provision", key=f"select_{i}"):
                selected_provisions.append(provision)
    
    # Local RAG exploration for selected provisions
    if selected_provisions:
        st.subheader("🔗 Relationship Exploration")
        
        for provision in selected_provisions:
            explore_provision_relationships(
                provision, relationship_types, include_amendments, 
                show_statistics, as_of_date
            )
    
    # Citations panel
    render_citations_panel(search_results, "📚 All Sources & Citations")


def explore_provision_relationships(
    provision: Dict[str, Any],
    relationship_types: List[str],
    include_amendments: bool,
    show_statistics: bool,
    as_of_date
):
    """Explore relationships for a selected provision."""
    
    provision_id = provision.get("id")
    provision_number = provision.get("number", "Unknown")
    
    st.subheader(f"🔍 Exploring Article {provision_number}")
    
    with st.spinner(f"Finding relationships for Article {provision_number}..."):
        # Execute local RAG query
        local_result = local_rag_query(provision_id, as_of_date, relationship_types)
    
    if "error" in local_result:
        st.error(f"Error exploring provision: {local_result['error']}")
        return
    
    # Display provision context
    provision_context = local_result.get("provision", {})
    if provision_context:
        display_provision_context(provision_context)
    
    # Display relationship paths
    neighbors = local_result.get("neighbors", [])
    if neighbors:
        render_paths(neighbors, str(as_of_date), "local_rag")
        
        if show_statistics:
            render_path_statistics(neighbors)
    else:
        st.info(f"No relationships found for Article {provision_number} as of {as_of_date}")
    
    # Display amendments if requested
    if include_amendments:
        amendments = local_result.get("amendments", [])
        if amendments:
            render_temporal_timeline(amendments)
        else:
            st.info("No amendments found for this provision.")
    
    # Grounding validation
    validate_and_display_grounding(local_result, neighbors + local_result.get("amendments", []))


def display_provision_context(provision_context: Dict[str, Any]):
    """Display full context for a provision."""
    provision = provision_context.get("provision", {})
    instrument = provision_context.get("instrument", {})
    gazette = provision_context.get("gazette", {})
    
    with st.expander("📋 Full Provision Context", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Provision Details:**")
            st.markdown(f"- **Article:** {provision.get('number', 'Unknown')}")
            st.markdown(f"- **Title:** {provision.get('article_title', 'No title')}")
            st.markdown(f"- **ID:** `{provision.get('id', 'Unknown')}`")
        
        with col2:
            if instrument:
                st.markdown("**Source Instrument:**")
                st.markdown(f"- **Title:** {instrument.get('title', 'Unknown')}")
                st.markdown(f"- **Type:** {instrument.get('type', 'Unknown')}")
                st.markdown(f"- **Year:** {instrument.get('year', 'Unknown')}")
            
            if gazette:
                st.markdown("**Gazette Publication:**")
                st.markdown(f"- **Number:** {gazette.get('number', 'Unknown')}")
                st.markdown(f"- **Date:** {gazette.get('date', 'Unknown')}")


def validate_and_display_grounding(local_result: Dict[str, Any], sources: List[Dict[str, Any]]):
    """Validate grounding and display appropriate content."""
    
    # Create a simple summary for grounding validation
    provision = local_result.get("provision", {}).get("provision", {})
    neighbors = local_result.get("neighbors", [])
    
    if not neighbors:
        return
    
    # Generate a basic summary
    summary = f"Article {provision.get('number', 'Unknown')} has {len(neighbors)} relationships"
    
    # Validate grounding
    is_grounded = validate_answer_grounding(summary, sources, strict=False)
    
    with st.expander("🛡️ Grounding Validation", expanded=False):
        if is_grounded:
            st.success("✅ Content is properly grounded in sources")
            st.markdown(summary)
        else:
            st.warning("⚠️ Grounding validation failed - showing sources only")
            fallback_content = get_fallback_sources_only(sources)
            st.markdown(fallback_content)


if __name__ == "__main__":
    main()
