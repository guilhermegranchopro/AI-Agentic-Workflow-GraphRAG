#!/bin/bash

# Seeding script for Neo4j database
# Usage: ./seed_local.sh [NEO4J_URI] [NEO4J_USER] [NEO4J_PASSWORD] [NEO4J_DATABASE]

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

echo "🌱 Seeding Neo4j database..."
echo "URI: $NEO4J_URI"
echo "User: $NEO4J_USER"
echo "Database: $NEO4J_DATABASE"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SEED_DIR="$PROJECT_ROOT/src/graph/seed"

# Check if cypher-shell is available
if ! command -v cypher-shell &> /dev/null; then
    echo "Error: cypher-shell not found. Please install Neo4j and ensure cypher-shell is in PATH."
    exit 1
fi

# Check if seed files exist
SEED_FILES=(
    "01_schema.cypher"
    "02_seed.cypher"
    "03_indexes_vector.cypher"
)

for file in "${SEED_FILES[@]}"; do
    if [ ! -f "$SEED_DIR/$file" ]; then
        echo "Error: Seed file not found: $SEED_DIR/$file"
        exit 1
    fi
done

echo "📋 Found all required seed files"

# Function to run cypher file
run_cypher_file() {
    local file="$1"
    local description="$2"
    
    echo "🔧 $description..."
    
    if [ "$file" = "03_indexes_vector.cypher" ]; then
        # Vector index creation needs the dimension parameter
        # Read dimension from environment
        EMBEDDING_DIM="${EMBEDDING_DIM:-3072}"
        echo "Creating vector index with dimension: $EMBEDDING_DIM"
        
        # Create temporary file with parameter
        temp_file=$(mktemp)
        echo ":param dim => $EMBEDDING_DIM;" > "$temp_file"
        cat "$SEED_DIR/$file" >> "$temp_file"
        
        cypher-shell \
            -a "$NEO4J_URI" \
            -u "$NEO4J_USER" \
            -p "$NEO4J_PASSWORD" \
            --database "$NEO4J_DATABASE" \
            -f "$temp_file"
        
        rm "$temp_file"
    else
        cypher-shell \
            -a "$NEO4J_URI" \
            -u "$NEO4J_USER" \
            -p "$NEO4J_PASSWORD" \
            --database "$NEO4J_DATABASE" \
            -f "$SEED_DIR/$file"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ $description completed successfully"
    else
        echo "❌ $description failed"
        exit 1
    fi
}

# Run seed files in order
run_cypher_file "01_schema.cypher" "Creating schema constraints and indexes"
run_cypher_file "02_seed.cypher" "Loading sample data"
run_cypher_file "03_indexes_vector.cypher" "Creating vector indexes"

echo ""
echo "🎉 Database seeding completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run embeddings: python scripts/load_embeddings.py"
echo "2. Run GDS: ./scripts/run_gds.sh"
echo "3. Start app: streamlit run app/Home.py"
