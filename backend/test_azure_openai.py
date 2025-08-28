#!/usr/bin/env python3
"""
Test script to diagnose Azure OpenAI configuration and list available deployments.
"""

import asyncio
import os
from openai import AsyncOpenAI
from loguru import logger

async def test_azure_openai():
    """Test Azure OpenAI connection and list deployments."""
    
    # Import settings from the app
    from app.schemas.config import settings
    
    # Get environment variables from settings
    api_key = settings.azure_openai_api_key
    endpoint = settings.azure_openai_endpoint
    deployment = settings.azure_openai_deployment
    api_version = settings.azure_openai_api_version
    
    print("=== Azure OpenAI Configuration ===")
    print(f"API Key: {'*' * 10 if api_key else 'NOT SET'}")
    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment}")
    print(f"API Version: {api_version}")
    print()
    
    if not api_key or not endpoint:
        print("❌ Missing required Azure OpenAI configuration")
        return
    
    try:
        # Initialize client
        base_url = f"{endpoint}openai"
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            default_headers={"api-version": api_version}
        )
        
        print("✅ Azure OpenAI client initialized successfully")
        print(f"Base URL: {base_url}")
        print()
        
        # Test 1: List deployments
        print("=== Testing: List Deployments ===")
        try:
            deployments = await client.models.list()
            print(f"✅ Found {len(deployments.data)} deployments:")
            for model in deployments.data:
                print(f"  - {model.id}")
        except Exception as e:
            print(f"❌ Failed to list deployments: {e}")
        print()
        
        # Test 2: Test specific deployment
        if deployment:
            print(f"=== Testing: Specific Deployment '{deployment}' ===")
            try:
                response = await client.chat.completions.create(
                    model=deployment,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                print(f"✅ Deployment '{deployment}' is working!")
                print(f"Response: {response.choices[0].message.content}")
            except Exception as e:
                print(f"❌ Deployment '{deployment}' failed: {e}")
        print()
        
        # Test 3: Try common deployment names
        print("=== Testing: Common Deployment Names ===")
        common_deployments = [
            "gpt-4",
            "gpt-35-turbo", 
            "gpt-4o",
            "gpt-4o-mini",
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large"
        ]
        
        for test_deployment in common_deployments:
            try:
                response = await client.chat.completions.create(
                    model=test_deployment,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                print(f"✅ Deployment '{test_deployment}' is available!")
                break
            except Exception as e:
                if "404" in str(e):
                    print(f"❌ Deployment '{test_deployment}' not found")
                else:
                    print(f"⚠️  Deployment '{test_deployment}' error: {e}")
        
    except Exception as e:
        print(f"❌ Failed to initialize Azure OpenAI client: {e}")

if __name__ == "__main__":
    asyncio.run(test_azure_openai())
