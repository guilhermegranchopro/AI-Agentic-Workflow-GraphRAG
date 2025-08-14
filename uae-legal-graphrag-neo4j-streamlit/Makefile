# UAE Legal GraphRAG - Neo4j + Streamlit + Azure OpenAI
# Makefile for setup, seeding, and running the application

.PHONY: help setup seed embeddings gds run test clean

# Default target
help:
	@echo "UAE Legal GraphRAG - Available Commands:"
	@echo ""
	@echo "  make setup      - Create virtual environment and install dependencies"
	@echo "  make seed       - Seed Neo4j database with schema and sample data"
	@echo "  make embeddings - Generate and load embeddings for provisions"
	@echo "  make gds        - Run GDS Louvain community detection"
	@echo "  make run        - Start the Streamlit application"
	@echo "  make test       - Run the test suite"
	@echo "  make clean      - Clean up temporary files"
	@echo ""
	@echo "Quick start (after setting up .env):"
	@echo "  make setup && make seed && make embeddings && make gds && make run"

# Setup virtual environment and install dependencies
setup:
	@echo "🔧 Setting up Python environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Setup complete! Activate with: source venv/bin/activate"

# Seed the database
seed:
	@echo "🌱 Seeding Neo4j database..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	. .env && ./scripts/seed_local.sh
	@echo "✅ Database seeding complete!"

# Generate and load embeddings
embeddings:
	@echo "📝 Generating embeddings..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	python scripts/load_embeddings.py
	@echo "✅ Embeddings loading complete!"

# Run GDS Louvain community detection
gds:
	@echo "🧠 Running GDS Louvain community detection..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	. .env && ./scripts/run_gds.sh
	@echo "✅ GDS community detection complete!"

# Run the Streamlit application
run:
	@echo "🚀 Starting Streamlit application..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	streamlit run app/Home.py

# Run tests
test:
	@echo "🧪 Running test suite..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	pytest tests/ -v

# Run specific test files
test-db:
	pytest tests/test_db_connect.py -v

test-vector:
	pytest tests/test_vector_knn.py -v

test-temporal:
	pytest tests/test_asof_traversal.py -v

test-communities:
	pytest tests/test_louvain_labels.py -v

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ Cleanup complete!"

# Development helpers
dev-install:
	pip install -e .
	pip install pytest black flake8 mypy

lint:
	@echo "🔍 Running linters..."
	black --check .
	flake8 .
	mypy src/

format:
	@echo "🎨 Formatting code..."
	black .

# Check environment
check-env:
	@echo "🔍 Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found"; \
		exit 1; \
	fi
	@echo "✅ .env file found"
	@python -c "from src.config import settings; print('✅ Configuration loaded successfully')"

# Quick health check
health:
	@echo "🏥 Performing health check..."
	python -c "from src.db import db; health = db.health_check(); print('✅ Database health:', health['status'])"

# Full setup from scratch
full-setup: setup check-env seed embeddings gds
	@echo "🎉 Full setup complete! Run 'make run' to start the application."

# Docker helpers (if you want to add Docker support later)
docker-build:
	docker build -t uae-legal-graphrag .

docker-run:
	docker-compose up -d

# Database utilities
db-reset:
	@echo "⚠️  This will delete all data in the database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	. .env && echo "MATCH (n) DETACH DELETE n" | cypher-shell -a $$NEO4J_URI -u $$NEO4J_USER -p $$NEO4J_PASSWORD --database $$NEO4J_DATABASE

db-stats:
	@echo "📊 Database statistics..."
	. .env && echo "MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY count DESC" | cypher-shell -a $$NEO4J_URI -u $$NEO4J_USER -p $$NEO4J_PASSWORD --database $$NEO4J_DATABASE
