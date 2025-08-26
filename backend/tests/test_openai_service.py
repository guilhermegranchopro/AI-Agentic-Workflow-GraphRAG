"""
Tests for OpenAI service functionality.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.openai_service import OpenAIClient
import os


@pytest.fixture
def openai_client():
    """Create OpenAI client instance."""
    return OpenAIClient()


@pytest.fixture
def mock_azure_openai():
    """Mock Azure OpenAI client."""
    with patch("app.services.openai_service.AzureOpenAI") as mock:
        client = Mock()
        mock.return_value = client
        yield client


class TestOpenAIClient:
    """Test OpenAI client functionality."""

    @pytest.mark.asyncio
    async def test_openai_client_initialization(self, mock_azure_openai):
        """Test OpenAI client initialization."""
        client = OpenAIClient()
        assert client is not None
        assert hasattr(client, 'client')

    @pytest.mark.asyncio
    async def test_generate_response(self, openai_client, mock_azure_openai):
        """Test response generation."""
        # Mock the chat completion response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated response"
        mock_response.usage.total_tokens = 100
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100
        )

        assert response == "Generated response"
        mock_azure_openai.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response_with_system_prompt(self, openai_client, mock_azure_openai):
        """Test response generation with system prompt."""
        # Mock the chat completion response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "System-guided response"
        mock_response.usage.total_tokens = 150
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Test message"}
        ]
        
        response = await openai_client.generate_response(
            messages=messages,
            max_tokens=100
        )

        assert response == "System-guided response"
        
        # Verify the call included system message
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert len(call_args[1]['messages']) == 2
        assert call_args[1]['messages'][0]['role'] == 'system'

    @pytest.mark.asyncio
    async def test_generate_response_with_temperature(self, openai_client, mock_azure_openai):
        """Test response generation with temperature parameter."""
        # Mock the chat completion response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Creative response"
        mock_response.usage.total_tokens = 80
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100,
            temperature=0.8
        )

        assert response == "Creative response"
        
        # Verify temperature was passed
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert call_args[1]['temperature'] == 0.8

    @pytest.mark.asyncio
    async def test_generate_response_api_error(self, openai_client, mock_azure_openai):
        """Test handling of API errors."""
        # Mock API error
        mock_azure_openai.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            await openai_client.generate_response(
                messages=[{"role": "user", "content": "Test message"}],
                max_tokens=100
            )

    @pytest.mark.asyncio
    async def test_generate_response_rate_limit_error(self, openai_client, mock_azure_openai):
        """Test handling of rate limit errors."""
        # Mock rate limit error
        from openai import RateLimitError
        mock_azure_openai.chat.completions.create.side_effect = RateLimitError(
            "Rate limit exceeded", response=Mock(), body=None
        )

        with pytest.raises(RateLimitError):
            await openai_client.generate_response(
                messages=[{"role": "user", "content": "Test message"}],
                max_tokens=100
            )

    @pytest.mark.asyncio
    async def test_generate_response_empty_choices(self, openai_client, mock_azure_openai):
        """Test handling of empty choices in response."""
        # Mock response with empty choices
        mock_response = Mock()
        mock_response.choices = []
        mock_response.usage.total_tokens = 0
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        with pytest.raises(ValueError):
            await openai_client.generate_response(
                messages=[{"role": "user", "content": "Test message"}],
                max_tokens=100
            )

    @pytest.mark.asyncio
    async def test_generate_response_none_content(self, openai_client, mock_azure_openai):
        """Test handling of None content in response."""
        # Mock response with None content
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None
        mock_response.usage.total_tokens = 50
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        with pytest.raises(ValueError):
            await openai_client.generate_response(
                messages=[{"role": "user", "content": "Test message"}],
                max_tokens=100
            )

    @pytest.mark.asyncio
    async def test_generate_response_with_streaming(self, openai_client, mock_azure_openai):
        """Test response generation with streaming enabled."""
        # Mock streaming response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Streamed response"
        mock_response.usage.total_tokens = 120
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100,
            stream=True
        )

        assert response == "Streamed response"
        
        # Verify streaming was enabled
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert call_args[1]['stream'] is True

    @pytest.mark.asyncio
    async def test_generate_response_with_functions(self, openai_client, mock_azure_openai):
        """Test response generation with function calling."""
        # Mock response with function call
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Function response"
        mock_response.choices[0].message.function_call = {
            "name": "test_function",
            "arguments": '{"param": "value"}'
        }
        mock_response.usage.total_tokens = 200
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        functions = [
            {
                "name": "test_function",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param": {"type": "string"}
                    }
                }
            }
        ]

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100,
            functions=functions
        )

        assert response == "Function response"
        
        # Verify functions were passed
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert call_args[1]['functions'] == functions

    @pytest.mark.asyncio
    async def test_generate_response_token_limit(self, openai_client, mock_azure_openai):
        """Test response generation with token limit."""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Limited response"
        mock_response.usage.total_tokens = 50
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=50
        )

        assert response == "Limited response"
        
        # Verify max_tokens was passed
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert call_args[1]['max_tokens'] == 50

    @pytest.mark.asyncio
    async def test_generate_response_with_model_override(self, openai_client, mock_azure_openai):
        """Test response generation with custom model."""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Custom model response"
        mock_response.usage.total_tokens = 100
        
        mock_azure_openai.chat.completions.create.return_value = mock_response

        response = await openai_client.generate_response(
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=100,
            model="gpt-4-turbo"
        )

        assert response == "Custom model response"
        
        # Verify custom model was used
        call_args = mock_azure_openai.chat.completions.create.call_args
        assert call_args[1]['model'] == "gpt-4-turbo"


@pytest.mark.integration
class TestOpenAIClientIntegration:
    """Integration tests for OpenAI client (requires actual API access)."""

    @pytest.mark.asyncio
    async def test_real_api_call(self):
        """Test real API call (if credentials are available)."""
        # This test would require real API credentials
        # For now, we'll skip it in CI/CD environments
        if os.environ.get("CI") or not os.environ.get("AZURE_OPENAI_API_KEY"):
            pytest.skip("Skipping integration test - no API credentials available")
        
        # Test would go here if API credentials are available
        pass
