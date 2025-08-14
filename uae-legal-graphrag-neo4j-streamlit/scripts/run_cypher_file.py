#!/usr/bin/env python3
"""
Fallback script to execute Cypher files when cypher-shell is not available.
Reads a .cypher file and executes statements via Neo4j Python driver.
"""

import os
import sys
import ssl
from pathlib import Path
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def parse_cypher_file(filepath):
    """Parse a Cypher file into individual statements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments (lines starting with //)
    lines = content.split('\n')
    lines = [line for line in lines if not line.strip().startswith('//')]
    content = '\n'.join(lines)
    
    # Split on semicolons, but be careful about semicolons in strings
    statements = []
    current_stmt = ""
    in_string = False
    
    for char in content:
        if char == "'" and not in_string:
            in_string = True
        elif char == "'" and in_string:
            in_string = False
        elif char == ';' and not in_string:
            if current_stmt.strip():
                statements.append(current_stmt.strip())
            current_stmt = ""
            continue
        
        current_stmt += char
    
    # Add final statement if exists
    if current_stmt.strip():
        statements.append(current_stmt.strip())
    
    return [stmt for stmt in statements if stmt and not stmt.isspace()]

from dotenv import load_dotenv
from neo4j import GraphDatabase
import ssl

def execute_cypher_file(filepath):
    """Execute a Cypher file against Neo4j."""
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not all([uri, user, password]):
        print("❌ Missing Neo4j credentials!")
        return False
    
    print(f"📁 Executing: {filepath}")
    print(f"🔗 Database: {database}")
    
    try:
        statements = parse_cypher_file(filepath)
        print(f"📝 Found {len(statements)} statements")
        
        # Handle AuraDB SSL issues (demo mode)
        if "bolt+s://" in uri:
            print("⚠️  Using insecure SSL mode for AuraDB demo")
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            plain_uri = uri.replace("bolt+s://", "bolt://")
            driver = GraphDatabase.driver(
                plain_uri, 
                auth=(user, password),
                encrypted=True,
                ssl_context=ssl_context
            )
        else:
            driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session(database=database) as session:
            for i, stmt in enumerate(statements, 1):
                print(f"⚡ Executing statement {i}/{len(statements)}")
                print(f"   {stmt[:60]}{'...' if len(stmt) > 60 else ''}")
                
                try:
                    # Most statements need write transactions for schema changes
                    if any(keyword in stmt.upper() for keyword in 
                           ['CREATE', 'DROP', 'ALTER', 'MERGE', 'SET', 'DELETE', 'REMOVE']):
                        def execute_write(tx):
                            result = tx.run(stmt)
                            summary = result.consume()
                            return summary
                        summary = session.execute_write(execute_write)
                    else:
                        result = session.run(stmt)
                        summary = result.consume()
                    
                    print(f"   ✅ Success ({summary.counters})")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    if "already exists" not in str(e).lower():
                        driver.close()
                        return False
        
        driver.close()
        print(f"✅ Successfully executed {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to execute {filepath}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_cypher_file.py <cypher_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    
    success = execute_cypher_file(filepath)
    sys.exit(0 if success else 1)
