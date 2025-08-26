import asyncio
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from ..schemas.config import settings


class AzureLLM:
    """Azure OpenAI client wrapper with retry logic."""
    
    def __init__(self):
        """Initialize Azure OpenAI client."""
        if not settings.azure_openai_api_key or not settings.azure_openai_endpoint:
            logger.warning("Azure OpenAI credentials not configured")
            self.client = None
            return
            
        self.client = AsyncOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            azure_deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version
        )
        self.deployment = settings.azure_openai_deployment
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        timeout: int = 30
    ) -> str:
        """Send chat completion request with retry logic."""
        if not self.client:
            raise ValueError("Azure OpenAI client not configured")
            
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                ),
                timeout=timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Azure OpenAI chat error: {e}")
            raise
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def embed(
        self,
        texts: List[str],
        timeout: int = 30
    ) -> List[List[float]]:
        """Generate embeddings with retry logic."""
        if not self.client:
            raise ValueError("Azure OpenAI client not configured")
            
        try:
            response = await asyncio.wait_for(
                self.client.embeddings.create(
                    model=self.deployment,
                    input=texts
                ),
                timeout=timeout
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Azure OpenAI embed error: {e}")
            raise
            
    async def health_check(self) -> Dict[str, Any]:
        """Check Azure OpenAI service health."""
        if not self.client:
            return {"status": "not_configured", "error": "Credentials missing"}
            
        try:
            # Simple health check with minimal tokens
            await self.chat(
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                timeout=10
            )
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
