# UAE Legal GraphRAG Demo

A production-ready **GraphRAG demo** using **Neo4j 5.x**, **Python 3.11+**, and **Streamlit** for UAE legal research. Features three retrieval modes: **Local**, **Global**, and **DRIFT** RAG with bi-temporal legal data modeling.

**Proprietary software developed for the EY AI & Data Team.**

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   Azure OpenAI   │    │     Neo4j 5.x   │
│                 │    │   Embeddings     │    │                 │
│ • Local RAG     │◄──►│                  │◄──►│ • Bi-temporal   │
│ • Global RAG    │    │ • text-embedding │    │ • GDS Louvain   │
│ • DRIFT RAG     │    │   -3-large       │    │ • Vector Index  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites

- **Neo4j 5.x** (Desktop or AuraDB)
- **Python 3.11+**
- **Azure OpenAI** account with embeddings deployment
- **GDS plugin** (for Neo4j Desktop) or Aura tier that supports GDS

### 2. Setup

```bash
# Clone and setup
git clone <your-repo>
cd uae-legal-graphrag-neo4j-streamlit

# Install dependencies
make setup

# Configure environment
cp .env.example .env
# Edit .env with your Neo4j and Azure OpenAI credentials
```

### 3. Configure `.env`

```bash
NEO4J_URI=bolt+s://YOUR-DBID.databases.neo4j.io  # or bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
EMBEDDING_DIM=3072  # or 1536 for smaller model
APP_DEFAULT_ASOF=2024-10-01
```

### 4. Seed and Run

```bash
# One-command setup
make full-setup

# OR step by step:
make seed        # Create schema and load sample data
make embeddings  # Generate Azure OpenAI embeddings
make gds         # Run community detection
make run         # Launch Streamlit app
```

## 📋 Features

### 🎯 Local RAG
- **Vector similarity search** on legal provision text
- **As-of temporal filtering** for amendments and changes
- **Relationship traversal** (CITES, INTERPRETED_BY, AMENDED_BY, etc.)
- **Citation tracking** with Official Gazette references

### 🌐 Global RAG  
- **GDS Louvain community detection** on legal citation networks
- **Community-based topic discovery**
- **Cross-jurisdictional pattern analysis**
- **Interactive community exploration**

### 🎪 DRIFT RAG
- **Hybrid approach** combining Global community signals with Local search
- **Query-driven community selection** 
- **Multi-hop traversal** from community centers
- **Evidence fusion** across legal domains with grounding validation

## 🗂️ Data Model

### Bi-temporal UAE Legal Schema

```cypher
(:Instrument)-[:HAS_PROVISION]->(:Provision)
(:Instrument)-[:PUBLISHED_IN]->(:GazetteIssue)
(:Provision)-[:CITES]->(:Provision)
(:Provision)-[:INTERPRETED_BY]->(:Judgment)
(:Event)-[:AFFECTS]->(:Provision)  # with valid_from/valid_to
(:Court)-[:ISSUED]->(:Judgment)
```

### Sample Entities
- **Instruments**: UAE Constitution, Civil Code, Commercial Law
- **Provisions**: Articles with full text and metadata
- **Events**: Amendments with bi-temporal validity periods
- **Judgments**: DIFC Courts decisions with interpretations

## 🛠️ Development

### Commands

```bash
make help          # Show all available commands
make test          # Run test suite
make lint          # Code linting
make format        # Code formatting
make health        # Quick health check
make db-stats      # Database statistics
```

### Project Structure

```
.
├── app/                      # Streamlit application
│   ├── Home.py              # Landing page with health checks
│   ├── pages/               # Multi-page navigation
│   │   ├── 1_Local.py       # Local RAG interface
│   │   ├── 2_Global.py      # Global RAG communities
│   │   └── 3_DRIFT.py       # DRIFT RAG hybrid
│   └── components/          # Reusable UI components
├── src/                     # Core application logic
│   ├── config.py           # Pydantic settings
│   ├── db.py               # Neo4j connection management
│   ├── embeddings/         # Azure OpenAI integration
│   ├── graph/              # Graph queries and tools
│   ├── safety/             # Grounding validation
│   └── utils/              # Formatting utilities
├── scripts/                # Setup and maintenance
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

## 🔍 Usage Examples

### Local RAG Query
```
Query: "civil liability compensation damage"
→ Vector search finds relevant provisions
→ Temporal traversal shows amendments as-of date
→ Citations include Gazette references
```

### Global RAG Analysis
```
Communities discovered:
• Community 1: Civil liability provisions + court interpretations
• Community 2: Commercial law articles + regulatory amendments  
• Community 3: Constitutional principles + jurisdictional rules
```

### DRIFT RAG Query
```
Query: "How are commercial companies liable for damages?"
→ Finds provisions in multiple communities
→ Traces relationships across legal domains
→ Fuses evidence with citation grounding
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test categories
make test-db          # Database connectivity
make test-vector      # Vector search functionality  
make test-temporal    # As-of temporal queries
make test-communities # Community detection
```

## 🔧 Troubleshooting

### Common Issues

1. **Vector index missing**
   ```bash
   # Recreate vector index
   make seed
   ```

2. **No embeddings found**
   ```bash
   # Generate embeddings
   make embeddings
   ```

3. **Communities not found**
   ```bash
   # Run community detection
   make gds
   ```

4. **Azure OpenAI errors**
   - Check endpoint URL format
   - Verify API key and deployment name
   - Ensure quota limits not exceeded

### For Neo4j Desktop
- Install GDS plugin from Graph Apps
- Ensure database is started
- Use `bolt://localhost:7687` as URI

### For Neo4j Aura
- Use `bolt+s://` URI with SSL
- Check Aura tier supports GDS
- Verify firewall allows connections

## � Proprietary Notice

This software is proprietary to **EY AI & Data Team**. All rights reserved. Unauthorized copying, distribution, or modification is strictly prohibited.

## 🤝 Internal Development

For EY AI & Data Team members:

1. Create feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open internal Pull Request for review

## 📚 References

- [Neo4j Vector Index Documentation](https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/)
- [Azure OpenAI Embeddings API](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- [Neo4j GDS Louvain](https://neo4j.com/docs/graph-data-science/current/algorithms/louvain/)
- [Streamlit Multi-page Apps](https://docs.streamlit.io/library/get-started/multipage-apps)

---

**Built with ❤️ by the EY AI & Data Team for UAE Legal Research**
