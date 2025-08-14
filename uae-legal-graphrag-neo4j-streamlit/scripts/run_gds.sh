#!/bin/bash

# Run GDS Louvain community detection
# Usage: ./run_gds.sh [NEO4J_URI] [NEO4J_USER] [NEO4J_PASSWORD] [NEO4J_DATABASE]

set -e

# Default values from environment or command line
NEO4J_URI="${1:-${NEO4J_URI:-bolt://localhost:7687}}"
NEO4J_USER="${2:-${NEO4J_USER:-neo4j}}"
NEO4J_PASSWORD="${3:-${NEO4J_PASSWORD}}"
NEO4J_DATABASE="${4:-${NEO4J_DATABASE:-neo4j}}"

if [ -z "$NEO4J_PASSWORD" ]; then
    echo "Error: NEO4J_PASSWORD must be provided"
    echo "Usage: $0 [URI] [USER] [PASSWORD] [DATABASE]"
    exit 1
fi

echo "🧠 Running GDS Louvain community detection..."
echo "URI: $NEO4J_URI"
echo "User: $NEO4J_USER"
echo "Database: $NEO4J_DATABASE"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GDS_FILE="$PROJECT_ROOT/src/graph/seed/04_gds_louvain.cypher"

# Check if cypher-shell is available
if ! command -v cypher-shell &> /dev/null; then
    echo "Error: cypher-shell not found. Please install Neo4j and ensure cypher-shell is in PATH."
    exit 1
fi

# Check if GDS file exists
if [ ! -f "$GDS_FILE" ]; then
    echo "Error: GDS file not found: $GDS_FILE"
    exit 1
fi

echo "📋 Found GDS Louvain script"

# Check if GDS is available (for Aura users)
echo "🔍 Checking GDS availability..."
cypher-shell \
    -a "$NEO4J_URI" \
    -u "$NEO4J_USER" \
    -p "$NEO4J_PASSWORD" \
    --database "$NEO4J_DATABASE" \
    "CALL gds.version() YIELD gdsVersion RETURN gdsVersion"

if [ $? -ne 0 ]; then
    echo "❌ GDS is not available in this Neo4j instance"
    echo "Note: GDS is available in Neo4j Desktop (with plugin) and some Aura tiers"
    exit 1
fi

echo "✅ GDS is available"

# Run GDS Louvain
echo "🔧 Running Louvain community detection..."

cypher-shell \
    -a "$NEO4J_URI" \
    -u "$NEO4J_USER" \
    -p "$NEO4J_PASSWORD" \
    --database "$NEO4J_DATABASE" \
    -f "$GDS_FILE"

if [ $? -eq 0 ]; then
    echo "✅ GDS Louvain completed successfully"
    
    # Show community statistics
    echo "📊 Community statistics:"
    cypher-shell \
        -a "$NEO4J_URI" \
        -u "$NEO4J_USER" \
        -p "$NEO4J_PASSWORD" \
        --database "$NEO4J_DATABASE" \
        "MATCH (n) WHERE n.communityId IS NOT NULL 
         RETURN n.communityId as community, count(n) as size 
         ORDER BY size DESC LIMIT 10"
else
    echo "❌ GDS Louvain failed"
    exit 1
fi

echo ""
echo "🎉 GDS community detection completed!"
echo ""
echo "You can now use Global and DRIFT RAG modes in the Streamlit app."
