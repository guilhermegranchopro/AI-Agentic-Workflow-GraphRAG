"""
Configuration management for Python backend
"""

import os
from pydantic import BaseSettings, Field
from typing import Optional

class Neo4jSettings(BaseSettings):
    """Neo4j database configuration"""
    uri: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    user: str = Field(default="neo4j", env="NEO4J_USERNAME")
    password: str = Field(default="", env="NEO4J_PASSWORD")
    database: str = Field(default="neo4j", env="NEO4J_DATABASE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class AzureOpenAISettings(BaseSettings):
    """Azure OpenAI configuration"""
    api_key: str = Field(default="", env="AZURE_OPENAI_API_KEY")
    endpoint: str = Field(default="", env="AZURE_OPENAI_ENDPOINT")
    deployment: str = Field(default="", env="AZURE_OPENAI_DEPLOYMENT")
    api_version: str = Field(default="2024-02-15-preview", env="AZURE_OPENAI_API_VERSION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Neo4j Configuration
    neo4j: Neo4jSettings = Neo4jSettings()
    
    # Azure OpenAI Configuration
    azure_openai: AzureOpenAISettings = AzureOpenAISettings()
    
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
    
    def validate_neo4j(self) -> bool:
        """Validate Neo4j configuration"""
        return bool(self.neo4j.uri and self.neo4j.user and self.neo4j.password)
    
    def validate_azure_openai(self) -> bool:
        """Validate Azure OpenAI configuration"""
        return bool(self.azure_openai.api_key and self.azure_openai.endpoint and self.azure_openai.deployment)

# Global settings instance
settings = Settings()
