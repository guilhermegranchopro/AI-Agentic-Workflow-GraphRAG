import asyncio
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from ..schemas.config import settings


class AzureLLM:
    """Azure OpenAI client wrapper with retry logic."""
    
    def __init__(self):
        """Initialize Azure OpenAI client."""
        if not settings.azure_openai_api_key or not settings.azure_openai_endpoint:
            logger.warning("Azure OpenAI credentials not configured - using mock mode")
            logger.warning(f"API Key present: {bool(settings.azure_openai_api_key)}")
            logger.warning(f"Endpoint present: {bool(settings.azure_openai_endpoint)}")
            self.client = None
            self.deployment = "mock-deployment"
            self.mock_mode = True
            return
            
        try:
            # Use AzureOpenAI client with correct parameters (matching test_azure configuration)
            self.client = AzureOpenAI(
                api_key=settings.azure_openai_api_key,
                azure_endpoint=settings.azure_openai_endpoint,
                api_version=settings.azure_openai_api_version
            )
            self.deployment = settings.azure_openai_deployment
            self.mock_mode = False
            logger.info(f"Azure OpenAI client initialized successfully with endpoint: {settings.azure_openai_endpoint}")
            logger.info(f"Using deployment: {self.deployment}")
        except Exception as e:
            logger.warning(f"Failed to initialize Azure OpenAI client: {e} - using mock mode")
            self.client = None
            self.deployment = "mock-deployment"
            self.mock_mode = True
        
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
        if not self.client or self.mock_mode:
            # Return mock response when Azure OpenAI is not configured
            logger.info("Azure OpenAI not configured - returning mock response")
            return self._generate_mock_response(messages)
            
        try:
            # Use synchronous client in async context
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Azure OpenAI chat error: {e}")
            logger.error(f"Deployment: {self.deployment}")
            logger.error(f"Endpoint: {settings.azure_openai_endpoint}")
            # Fallback to mock response on error
            logger.info("Falling back to mock response due to Azure OpenAI error")
            # Set mock mode to avoid repeated failed attempts
            self.mock_mode = True
            return self._generate_mock_response(messages)
            
    def _generate_mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a mock response when Azure OpenAI is not available."""
        last_message = messages[-1]["content"].lower() if messages else ""
        
        # Generate context-aware mock responses
        if "legal" in last_message or "law" in last_message:
            return "Based on UAE legal framework, I can provide guidance on legal matters. For specific legal advice, please consult with a qualified legal professional."
        elif "vat" in last_message or "tax" in last_message:
            return "UAE VAT regulations require businesses to register if their taxable supplies exceed AED 375,000 annually. The standard VAT rate is 5%."
        elif "employment" in last_message or "labor" in last_message:
            return "UAE Labor Law provides comprehensive protection for employees, including notice periods, end-of-service benefits, and working conditions."
        elif "free zone" in last_message:
            return "UAE Free Zones offer 100% foreign ownership, tax benefits, and simplified business setup procedures for international companies."
        else:
            return "I'm here to help with UAE legal and business matters. Please ask me specific questions about laws, regulations, or business procedures."
            
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
        if not self.client or self.mock_mode:
            # Return mock embeddings when Azure OpenAI is not configured
            logger.info("Azure OpenAI not configured - returning mock embeddings")
            return [[0.1] * 1536 for _ in texts]  # Mock embedding vector
            
        try:
            # Use synchronous client in async context
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.embeddings.create(
                    model=self.deployment,
                    input=texts
                )
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Azure OpenAI embed error: {e}")
            # Fallback to mock embeddings
            logger.info("Falling back to mock embeddings due to Azure OpenAI error")
            return [[0.1] * 1536 for _ in texts]
            
    async def health_check(self) -> Dict[str, Any]:
        """Check Azure OpenAI service health."""
        if not self.client or self.mock_mode:
            return {"status": "mock_mode", "message": "Using mock responses - Azure OpenAI deployment not available"}
            
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
            
    def is_configured(self) -> bool:
        """Check if Azure OpenAI is properly configured."""
        return self.client is not None and not self.mock_mode
