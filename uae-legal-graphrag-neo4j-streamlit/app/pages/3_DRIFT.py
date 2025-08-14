"""DRIFT RAG page - community-guided local search."""
import streamlit as st
import sys
import os
from typing import Dict, Any, List

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.graph.tools import drift_rag_query, semantic_search_provisions
from src.graph.queries import communities_top
from src.safety.grounding import validate_answer_grounding, create_grounded_summary, get_fallback_sources_only
from components.path_viewer import render_paths, render_path_statistics
from components.citations_panel import render_citations_panel, render_source_quality_indicators


def main():
    """Main DRIFT RAG page."""
    st.title("🎪 DRIFT RAG - Community-Guided Search")
    st.markdown("Global Community Signal → Targeted Local Hops → Evidence Fusion")
    
    # Get global settings
    as_of_date = st.session_state.get('as_of_date')
    max_results = st.session_state.get('max_results', 5)
    
    if not as_of_date:
        st.warning("Please set the as-of date in the sidebar on the Home page.")
        return
    
    # DRIFT query interface
    st.subheader("🎯 DRIFT Query Interface")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query_text = st.text_area(
            "Enter your comprehensive legal query:",
            placeholder="e.g., What are the liability rules for commercial companies and how are they interpreted by courts?",
            help="DRIFT works best with broader queries that might span multiple legal domains",
            height=100
        )
    
    with col2:
        st.markdown("**DRIFT Process:**")
        st.markdown("""
        1. 🎯 Find relevant provisions
        2. 🌐 Identify key communities  
        3. 🔍 Target local searches
        4. 🧩 Fuse evidence
        5. ✅ Validate grounding
        """)
    
    # Advanced DRIFT options
    with st.expander("🛠️ DRIFT Configuration"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_communities = st.slider("Top Communities", 1, 5, 3, 
                                       help="Number of communities to explore")
            semantic_seeds = st.slider("Semantic Seeds", 3, 10, 5,
                                     help="Initial semantic search results")
        
        with col2:
            max_paths_per_community = st.slider("Paths per Community", 1, 5, 2,
                                               help="Max relationship paths from each community")
            fusion_strategy = st.selectbox("Fusion Strategy", 
                                         ["Simple Merge", "Weighted by Score", "Community Priority"])
        
        with col3:
            grounding_strictness = st.selectbox("Grounding Level", 
                                              ["Lenient", "Standard", "Strict"])
            include_cross_community = st.checkbox("Cross-Community Links", value=True,
                                                 help="Include relationships between communities")
    
    # Execute DRIFT query
    if query_text:
        execute_drift_query(
            query_text, top_communities, semantic_seeds, max_paths_per_community,
            fusion_strategy, grounding_strictness, include_cross_community, as_of_date
        )


def execute_drift_query(
    query_text: str,
    top_communities: int,
    semantic_seeds: int, 
    max_paths_per_community: int,
    fusion_strategy: str,
    grounding_strictness: str,
    include_cross_community: bool,
    as_of_date
):
    """Execute the complete DRIFT RAG process."""
    
    with st.spinner("🎪 Executing DRIFT RAG query..."):
        # Execute DRIFT query
        drift_result = drift_rag_query(query_text, as_of_date, top_communities)
    
    if "error" in drift_result:
        st.error(f"DRIFT query failed: {drift_result['error']}")
        return
    
    # Display DRIFT process and results
    display_drift_process(drift_result, query_text)
    display_drift_results(drift_result, fusion_strategy, max_paths_per_community)
    validate_drift_grounding(drift_result, grounding_strictness)


def display_drift_process(drift_result: Dict[str, Any], query_text: str):
    """Display the DRIFT process flow."""
    
    st.subheader("🔄 DRIFT Process Flow")
    
    # Process overview
    semantic_seeds = drift_result.get("semantic_seeds", [])
    community_results = drift_result.get("community_results", [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Semantic Seeds", len(semantic_seeds))
        if semantic_seeds:
            with st.expander("View Semantic Seeds"):
                for i, seed in enumerate(semantic_seeds):
                    provision = seed.get("provision", {})
                    score = seed.get("score", 0)
                    st.markdown(f"**{i+1}.** Article {provision.get('number', 'Unknown')} (Score: {score:.3f})")
                    st.caption(provision.get("text", "")[:100] + "...")
    
    with col2:
        st.metric("🌐 Communities Explored", len(community_results))
        if community_results:
            with st.expander("View Communities"):
                for result in community_results:
                    community_id = result.get("community_id")
                    provisions_count = result.get("provisions_explored", 0)
                    paths_count = len(result.get("paths", []))
                    st.markdown(f"**Community {community_id}:** {provisions_count} provisions, {paths_count} paths")
    
    with col3:
        total_paths = sum(len(result.get("paths", [])) for result in community_results)
        st.metric("🔗 Total Paths Found", total_paths)
    
    # Query analysis
    st.subheader("🔍 Query Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Query:**")
        st.info(query_text)
    
    with col2:
        st.markdown("**DRIFT Strategy:**")
        strategy_text = generate_strategy_explanation(drift_result)
        st.markdown(strategy_text)


def generate_strategy_explanation(drift_result: Dict[str, Any]) -> str:
    """Generate explanation of DRIFT strategy."""
    
    semantic_count = len(drift_result.get("semantic_seeds", []))
    community_count = len(drift_result.get("community_results", []))
    
    explanation = f"""
    1. **Semantic Bootstrap:** Found {semantic_count} relevant provisions using vector similarity
    2. **Community Targeting:** Explored {community_count} communities for broader coverage
    3. **Local Exploration:** Performed relationship traversal from community centers
    4. **Evidence Fusion:** Combined paths and citations from multiple communities
    """
    
    return explanation


def display_drift_results(drift_result: Dict[str, Any], fusion_strategy: str, max_paths_per_community: int):
    """Display the fused DRIFT results."""
    
    st.subheader("🧩 Fused DRIFT Results")
    
    community_results = drift_result.get("community_results", [])
    
    if not community_results:
        st.warning("No community results found.")
        return
    
    # Apply fusion strategy
    fused_paths = apply_fusion_strategy(community_results, fusion_strategy, max_paths_per_community)
    
    # Display fused evidence
    if fused_paths:
        st.markdown(f"**Fused Evidence ({len(fused_paths)} total paths):**")
        
        # Group by community for organized display
        paths_by_community = {}
        for path_data in fused_paths:
            community_id = path_data.get("community_id", "Unknown")
            if community_id not in paths_by_community:
                paths_by_community[community_id] = []
            paths_by_community[community_id].append(path_data["path_info"])
        
        # Display each community's contribution
        for community_id, paths in paths_by_community.items():
            with st.expander(f"🏘️ Community {community_id} ({len(paths)} paths)", expanded=True):
                render_paths(paths, str(drift_result.get("as_of_date", "")))
                render_path_statistics(paths)
    
    else:
        st.info("No relationship paths found across communities.")
    
    # Generate comprehensive summary
    generate_drift_summary(drift_result, fused_paths)


def apply_fusion_strategy(community_results: List[Dict[str, Any]], 
                         strategy: str, max_paths: int) -> List[Dict[str, Any]]:
    """Apply the selected fusion strategy to combine results."""
    
    all_paths = []
    
    for community_result in community_results:
        community_id = community_result.get("community_id")
        paths = community_result.get("paths", [])
        
        for path_result in paths:
            neighbors = path_result.get("neighbors", [])
            
            # Take top paths from each community
            for neighbor in neighbors[:max_paths]:
                all_paths.append({
                    "community_id": community_id,
                    "path_info": neighbor,
                    "source_provision": path_result.get("provision", {})
                })
    
    # Apply fusion strategy
    if strategy == "Simple Merge":
        return all_paths
    
    elif strategy == "Weighted by Score":
        # Sort by relationship strength or provision scores
        # For now, just return all (would implement scoring logic)
        return all_paths
    
    elif strategy == "Community Priority":
        # Prioritize by community size or importance
        # For now, just return all (would implement priority logic)
        return all_paths
    
    return all_paths


def generate_drift_summary(drift_result: Dict[str, Any], fused_paths: List[Dict[str, Any]]):
    """Generate a comprehensive summary of DRIFT results."""
    
    st.subheader("📋 Comprehensive Summary")
    
    # Collect all sources for grounding
    all_sources = []
    
    # Add semantic seeds
    for seed in drift_result.get("semantic_seeds", []):
        all_sources.append(seed)
    
    # Add path sources
    for path_data in fused_paths:
        path_info = path_data.get("path_info", {})
        source_provision = path_data.get("source_provision", {})
        
        if source_provision:
            all_sources.append({"provision": source_provision})
    
    # Generate grounded summary
    if all_sources:
        grounded_summary = create_grounded_summary(all_sources, include_ids=True)
        
        with st.expander("📄 Generated Summary", expanded=True):
            st.markdown(grounded_summary)
    
    # Show source breakdown
    display_source_breakdown(drift_result, fused_paths)


def display_source_breakdown(drift_result: Dict[str, Any], fused_paths: List[Dict[str, Any]]):
    """Display breakdown of sources by type and community."""
    
    st.subheader("📊 Source Breakdown")
    
    # Count sources by type
    semantic_count = len(drift_result.get("semantic_seeds", []))
    
    community_counts = {}
    for path_data in fused_paths:
        community_id = path_data.get("community_id", "Unknown")
        community_counts[community_id] = community_counts.get(community_id, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Source Types:**")
        st.markdown(f"- 🎯 Semantic Seeds: {semantic_count}")
        st.markdown(f"- 🔗 Relationship Paths: {len(fused_paths)}")
        st.markdown(f"- 🌐 Communities: {len(community_counts)}")
    
    with col2:
        st.markdown("**By Community:**")
        for community_id, count in community_counts.items():
            st.markdown(f"- Community {community_id}: {count} paths")


def validate_drift_grounding(drift_result: Dict[str, Any], strictness: str):
    """Validate grounding of DRIFT results."""
    
    st.subheader("🛡️ Grounding Validation")
    
    # Collect all sources
    all_sources = []
    
    # Add semantic seeds as sources
    for seed in drift_result.get("semantic_seeds", []):
        all_sources.append(seed)
    
    # Add community path sources
    for community_result in drift_result.get("community_results", []):
        for path_result in community_result.get("paths", []):
            all_sources.append(path_result)
    
    if not all_sources:
        st.warning("No sources available for grounding validation.")
        return
    
    # Create a comprehensive summary for validation
    summary_text = f"""
    This DRIFT analysis found {len(drift_result.get('semantic_seeds', []))} relevant provisions 
    across {len(drift_result.get('community_results', []))} communities, 
    with {sum(len(cr.get('paths', [])) for cr in drift_result.get('community_results', []))} 
    relationship paths providing supporting evidence.
    """
    
    # Validate grounding based on strictness
    strict_mode = strictness == "Strict"
    is_grounded = validate_answer_grounding(summary_text, all_sources, strict=strict_mode)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if is_grounded:
            st.success("✅ DRIFT results are properly grounded")
            st.markdown("**Summary passes grounding validation:**")
            st.markdown(summary_text)
        else:
            st.warning("⚠️ Grounding validation failed")
            st.markdown("**Showing sources only:**")
            fallback = get_fallback_sources_only(all_sources)
            st.markdown(fallback)
    
    with col2:
        st.markdown("**Grounding Metrics:**")
        st.markdown(f"- **Strictness Level:** {strictness}")
        st.markdown(f"- **Total Sources:** {len(all_sources)}")
        st.markdown(f"- **Validation Status:** {'✅ Passed' if is_grounded else '❌ Failed'}")
        
        # Additional metrics could be shown here
        if strictness == "Strict":
            st.caption("Strict mode requires high citation coverage and no invalid references.")


if __name__ == "__main__":
    main()
