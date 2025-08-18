"""Configuration management using Pydantic settings."""

import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Neo4j Database Configuration
    neo4j_uri: str = Field(..., env="NEO4J_URI")
    neo4j_user: str = Field(..., env="NEO4J_USER") 
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")
    neo4j_database: str = Field("neo4j", env="NEO4J_DATABASE")
    
    # Azure OpenAI Configuration
    azure_openai_endpoint: str = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(..., env="AZURE_OPENAI_API_KEY")
    azure_openai_embedding_deployment: str = Field(..., env="AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    embedding_dim: int = Field(3072, env="EMBEDDING_DIM")
    
    # Application Settings
    app_default_asof: str = Field("2024-10-01", env="APP_DEFAULT_ASOF")
    
    # Optional extra fields that might be in .env
    aura_instanceid: Optional[str] = Field(None, env="AURA_INSTANCEID")
    aura_instancename: Optional[str] = Field(None, env="AURA_INSTANCENAME")
    log_level: Optional[str] = Field("INFO", env="LOG_LEVEL")
    debug: Optional[str] = Field("false", env="DEBUG")
    environment: Optional[str] = Field("development", env="ENVIRONMENT")
    
    model_config = {
        "env_file": [".env", "../.env", "../../.env"],  # Look for .env in multiple locations
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }
    
    @field_validator('embedding_dim')
    @classmethod
    def validate_embedding_dim(cls, v):
        """Validate embedding dimension is supported."""
        if v not in [1536, 3072]:
            raise ValueError("embedding_dim must be 1536 or 3072")
        return v
    
    @field_validator('azure_openai_endpoint')
    @classmethod
    def validate_azure_endpoint(cls, v):
        """Validate Azure OpenAI endpoint format."""
        if not v.startswith('https://') or not v.endswith('.openai.azure.com/'):
            if not v.endswith('.openai.azure.com'):
                raise ValueError("azure_openai_endpoint must be https://<resource>.openai.azure.com or https://<resource>.openai.azure.com/")
        return v


# Global settings instance
settings = Settings()
