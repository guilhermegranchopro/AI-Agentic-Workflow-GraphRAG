"""
Configuration management for Python backend
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Neo4j Configuration
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    # Advanced Processing Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    legal_embedding_model: str = "nlpaueb/legal-bert-base-uncased"
    max_embedding_batch_size: int = 32
    
    # Graph Processing
    max_graph_depth: int = 3
    community_detection_resolution: float = 1.0
    semantic_similarity_threshold: float = 0.7
    
    # API Settings
    max_query_length: int = 1000
    default_results_limit: int = 20
    request_timeout: int = 300
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()
