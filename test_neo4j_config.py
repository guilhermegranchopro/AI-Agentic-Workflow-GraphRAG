import os
import sys
sys.path.append('backend')

from app.schemas.config import settings

print("=== Neo4j Configuration Test ===")
print(f"NEO4J_URI: {settings.neo4j_uri}")
print(f"NEO4J_USERNAME: {settings.neo4j_username}")
print(f"NEO4J_PASSWORD: {'***' if settings.neo4j_password else 'None'}")

print("\n=== Environment Variables ===")
print(f"NEO4J_URI env: {os.getenv('NEO4J_URI')}")
print(f"NEO4J_USERNAME env: {os.getenv('NEO4J_USERNAME')}")
print(f"NEO4J_PASSWORD env: {'***' if os.getenv('NEO4J_PASSWORD') else 'None'}")

print("\n=== All Settings ===")
print(f"All configured: {all([settings.neo4j_uri, settings.neo4j_username, settings.neo4j_password])}")
