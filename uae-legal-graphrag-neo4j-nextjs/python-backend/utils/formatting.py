"""Utility functions for formatting and display."""
from typing import Dict, Any, List
from datetime import date, datetime


def format_provision_display(provision: Dict[str, Any], context: Dict[str, Any] = None) -> str:
    """Format provision for display with context information."""
    display_parts = []
    
    # Article header
    if provision.get("number"):
        header = f"Article {provision['number']}"
        if provision.get("article_title"):
            header += f": {provision['article_title']}"
        display_parts.append(f"**{header}**")
    
    # Source instrument
    if context and context.get("instrument"):
        instrument = context["instrument"]
        source = instrument.get("title", "Unknown Instrument")
        if instrument.get("year"):
            source += f" ({instrument['year']})"
        display_parts.append(f"*Source: {source}*")
    
    # Article text
    if provision.get("text"):
        display_parts.append(provision["text"])
    
    # Provision ID (for technical reference)
    if provision.get("id"):
        display_parts.append(f"*ID: {provision['id']}*")
    
    return "\n\n".join(display_parts)


def format_path_display(path_data: Dict[str, Any]) -> str:
    """Format relationship path for display as chips."""
    rel_type = path_data.get("relationship_type", "RELATED")
    neighbor = path_data.get("neighbor", {})
    
    # Format neighbor based on type
    if neighbor.get("case_number"):  # Judgment
        neighbor_display = f"Judgment {neighbor['case_number']}"
        if neighbor.get("date"):
            neighbor_display += f" ({neighbor['date']})"
    elif neighbor.get("number"):  # Provision
        neighbor_display = f"Article {neighbor['number']}"
    else:
        neighbor_display = neighbor.get("id", "Unknown")
    
    # Format relationship
    rel_display = rel_type.replace("_", " ").title()
    
    return f"**{rel_display}** → {neighbor_display}"


def format_citation_panel(context: Dict[str, Any]) -> str:
    """Format citation information panel."""
    citation_parts = []
    
    # Gazette information
    if context.get("gazette"):
        gazette = context["gazette"]
        gazette_info = f"**Official Gazette:** No. {gazette.get('number', 'Unknown')}"
        if gazette.get("date"):
            gazette_info += f", {gazette['date']}"
        citation_parts.append(gazette_info)
    
    # Instrument details
    if context.get("instrument"):
        instrument = context["instrument"]
        inst_info = f"**Instrument:** {instrument.get('title', 'Unknown')}"
        if instrument.get("type"):
            inst_info += f" ({instrument['type']})"
        if instrument.get("number") and instrument.get("year"):
            inst_info += f" No. {instrument['number']}/{instrument['year']}"
        citation_parts.append(inst_info)
    
    # Provision details
    if context.get("provision"):
        provision = context["provision"]
        prov_info = f"**Provision ID:** {provision.get('id', 'Unknown')}"
        citation_parts.append(prov_info)
    
    return "\n".join(citation_parts)


def format_community_summary(community_data: Dict[str, Any]) -> str:
    """Format community information for display."""
    summary_parts = []
    
    # Community header
    comm_id = community_data.get("id", "Unknown")
    size = community_data.get("size", 0)
    summary_parts.append(f"**Community {comm_id}** ({size} nodes)")
    
    # Node types
    node_types = community_data.get("node_types", [])
    if node_types:
        summary_parts.append(f"*Types:* {', '.join(node_types)}")
    
    # Summary description
    summary = community_data.get("summary", "")
    if summary:
        summary_parts.append(f"*Summary:* {summary}")
    
    # Sample nodes
    sample_nodes = community_data.get("sample_nodes", [])
    if sample_nodes:
        summary_parts.append("*Sample nodes:*")
        for node_data in sample_nodes[:3]:
            node = node_data.get("node", {})
            node_type = node_data.get("node_type", "")
            
            if node_type == "Provision" and node.get("number"):
                node_desc = f"- Article {node['number']}"
                if node.get("article_title"):
                    node_desc += f": {node['article_title']}"
            elif node_type == "Judgment" and node.get("case_number"):
                node_desc = f"- {node['case_number']}"
            else:
                node_desc = f"- {node.get('id', 'Unknown')}"
            
            summary_parts.append(node_desc)
    
    return "\n".join(summary_parts)


def format_score_display(score: float, score_type: str = "similarity") -> str:
    """Format similarity or relevance scores for display."""
    if score_type == "similarity":
        percentage = score * 100
        return f"{percentage:.1f}% similar"
    else:
        return f"Score: {score:.3f}"


def format_date_range(start_date: Any, end_date: Any = None) -> str:
    """Format date or date range for display."""
    def format_single_date(d):
        if isinstance(d, str):
            return d
        elif isinstance(d, (date, datetime)):
            return d.strftime("%Y-%m-%d")
        else:
            return str(d)
    
    start_str = format_single_date(start_date)
    
    if end_date:
        end_str = format_single_date(end_date)
        return f"{start_str} to {end_str}"
    else:
        return f"from {start_str}"


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix."""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # If word boundary is reasonable
        return truncated[:last_space] + suffix
    else:
        return truncated + suffix


def format_search_results_summary(results: List[Dict[str, Any]], 
                                query: str = "") -> str:
    """Format summary of search results."""
    if not results:
        return f"No results found for query: '{query}'"
    
    result_count = len(results)
    search_types = set()
    
    for result in results:
        if "search_type" in result:
            search_types.add(result["search_type"])
    
    summary = f"Found {result_count} result(s)"
    if query:
        summary += f" for '{query}'"
    
    if search_types:
        summary += f" using {', '.join(search_types)} search"
    
    return summary
