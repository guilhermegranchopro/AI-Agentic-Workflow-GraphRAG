from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings with grouped environment loading."""
    
    # Application settings
    app_env: str = Field(default="development", description="Application environment")
    port: int = Field(default=8000, description="Application port")
    
    # Azure OpenAI settings
    azure_openai_api_key: Optional[str] = Field(default=None, description="Azure OpenAI API key")
    azure_openai_endpoint: Optional[str] = Field(default=None, description="Azure OpenAI endpoint")
    azure_openai_deployment: Optional[str] = Field(default=None, description="Azure OpenAI deployment name")
    azure_openai_api_version: str = Field(default="2024-02-15-preview", description="Azure OpenAI API version")
    
    # Neo4j settings
    neo4j_uri: Optional[str] = Field(default=None, description="Neo4j connection URI")
    neo4j_username: Optional[str] = Field(default=None, description="Neo4j username")
    neo4j_password: Optional[str] = Field(default=None, description="Neo4j password")
    
    # FAISS settings
    faiss_index_path: str = Field(default="./data/faiss_index", description="FAISS index storage path")
    
    # Orchestration settings
    max_retrieval_results: int = Field(default=10, description="Maximum retrieval results")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold for RAG")
    max_conversation_turns: int = Field(default=10, description="Maximum conversation turns")
    
    # A2A protocol settings
    a2a_timeout: int = Field(default=30, description="A2A protocol timeout in seconds")
    a2a_max_retries: int = Field(default=3, description="A2A protocol max retries")
    
    # Rate limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per window")
    rate_limit_window: int = Field(default=3600, description="Rate limit window in seconds")
    
    class Config:
        env_file = "../.env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
