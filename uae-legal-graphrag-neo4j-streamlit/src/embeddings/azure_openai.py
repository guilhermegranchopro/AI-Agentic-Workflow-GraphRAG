"""Azure OpenAI embeddings integration."""
import httpx
import logging
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import AzureOpenAI
from src.config import settings

logger = logging.getLogger(__name__)


class AzureOpenAIEmbeddings:
    """Azure OpenAI embeddings client."""
    
    def __init__(self):
        self.endpoint = settings.azure_openai_endpoint
        self.api_key = settings.azure_openai_api_key
        self.deployment = settings.azure_openai_embedding_deployment
        self.api_version = "2024-02-01"
        
        self.base_url = f"{self.endpoint}/openai/deployments/{self.deployment}/embeddings"
        
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
    
    def _truncate_text(self, text: str, max_tokens: int = 8000) -> str:
        """Truncate text to approximate token limit."""
        # Rough approximation: 1 token ≈ 4 characters for English
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rsplit(' ', 1)[0]  # Truncate at word boundary
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def get_embeddings(self, text: str) -> List[float]:
        """
        Call Azure OpenAI embeddings endpoint for the configured deployment.
        Return a list[float] of length EMBEDDING_DIM.
        """
        try:
            # Truncate text if too long
            truncated_text = self._truncate_text(text)
            
            payload = {
                "input": truncated_text,
                "encoding_format": "float"
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}?api-version={self.api_version}",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                
                data = response.json()
                embedding = data["data"][0]["embedding"]
                
                # Validate embedding dimension
                if len(embedding) != settings.embedding_dim:
                    raise ValueError(
                        f"Expected embedding dimension {settings.embedding_dim}, "
                        f"got {len(embedding)}"
                    )
                
                logger.debug(f"Generated embedding for text of length {len(text)}")
                return embedding
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling Azure OpenAI: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        embeddings = []
        for i, text in enumerate(texts):
            try:
                embedding = self.get_embeddings(text)
                embeddings.append(embedding)
                logger.info(f"Generated embedding {i+1}/{len(texts)}")
            except Exception as e:
                logger.error(f"Failed to generate embedding for text {i+1}: {e}")
                # Return zero vector as fallback
                embeddings.append([0.0] * settings.embedding_dim)
        return embeddings


# Global embeddings instance
embeddings_client = AzureOpenAIEmbeddings()


def get_azure_openai_client() -> AzureOpenAI:
    """
    Get an Azure OpenAI client for chat completions.
    
    Returns:
        AzureOpenAI client instance configured for chat completions
    """
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version="2024-02-01",
        azure_endpoint=settings.azure_openai_endpoint
    )
