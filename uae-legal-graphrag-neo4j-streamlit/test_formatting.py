#!/usr/bin/env python3
"""Test the response formatting function."""

def format_agent_response_for_chatbot(response: str) -> str:
    """
    Convert raw agent response with escape characters to chatbot-friendly format.
    """
    if not response:
        return "I apologize, but I couldn't generate a response to your query."
    
    # Replace literal \n with actual newlines
    formatted = response.replace('\\n', '\n')
    
    # Clean up any double newlines
    formatted = formatted.replace('\n\n\n', '\n\n')
    
    # Ensure proper spacing around sections
    sections = [
        '**Temporal Legal Analysis:**',
        '**Historical Legal Context:**',
        '**Legal Framework Overview:**',
        '**Primary Legal Provision:**',
        '**Temporal Evolution Across Legal Domains:**',
        '**Cross-Domain Legal Analysis:**',
        '**Reference Date Analysis:**',
        '**Legal Evolution:**',
        '**Related Legal Context:**',
        '**Relevant Legal Provisions:**'
    ]
    
    for section in sections:
        formatted = formatted.replace(section, f'\n{section}')
    
    # Clean up any leading/trailing whitespace
    formatted = formatted.strip()
    
    # If response is too technical/raw, add a friendly intro
    if any(keyword in formatted for keyword in ['Historical Provision 1:', 'Legal Provision 1:', 'Domain 1:']):
        if 'temporal' in formatted.lower() or 'evolution' in formatted.lower():
            intro = "Based on my temporal analysis of UAE legal documents, here's what I found regarding the changes in this area:\n\n"
        elif 'framework' in formatted.lower() or 'overview' in formatted.lower():
            intro = "Here's a comprehensive overview of the legal framework you asked about:\n\n"
        elif 'provision' in formatted.lower():
            intro = "I found the following specific legal provisions relevant to your question:\n\n"
        else:
            intro = "Based on my analysis of UAE legal documents:\n\n"
        
        formatted = intro + formatted
    
    return formatted

# Test with example from user
test_response = "Temporal Legal Analysis:\\n\\nHistorical Legal Context:\\n1. Historical Provision 1: \\n2. Historical Provision 2: \\n3. Historical Provision 3: \\n\\nTemporal Evolution Across Legal Domains:\\nDomain 1: 1 temporal relationships identified\\nDomain 2: 1 temporal relationships identified\\n\\nReference Date Analysis: 2025-08-18\\nThe above provisions represent the legal framework as it existed or evolved around the specified timeframe.\\n\\nLegal Evolution: The analysis reveals how legal provisions have evolved over time, showing patterns of legislative development."

print("=== BEFORE FORMATTING ===")
print(repr(test_response))
print("\n=== AFTER FORMATTING ===")
formatted_result = format_agent_response_for_chatbot(test_response)
print(repr(formatted_result))
print("\n=== DISPLAY RESULT ===")
print(formatted_result)
