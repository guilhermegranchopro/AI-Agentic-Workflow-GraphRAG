"""Test database connectivity and basic operations."""
import pytest
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db


def test_database_connection():
    """Test that we can connect to Neo4j database."""
    
    # Load environment for testing
    load_dotenv()
    
    # Test connection
    db.connect()
    
    with db.session() as session:
        result = session.run("RETURN 1 as test_value")
        record = result.single()
        assert record["test_value"] == 1
    
    db.close()


def test_constraints_exist():
    """Test that required constraints are in place."""
    
    db.connect()
    
    with db.session() as session:
        # Check for constraints
        result = session.run("SHOW CONSTRAINTS")
        constraints = list(result)
        
        # Should have constraints for our main entities
        constraint_names = [c["name"] for c in constraints]
        
        # We expect at least some constraints to exist
        assert len(constraints) > 0, "No constraints found in database"
    
    db.close()


def test_seed_data_exists():
    """Test that seed data was loaded."""
    
    db.connect()
    
    with db.session() as session:
        # Check for provisions
        result = session.run("MATCH (p:Provision) RETURN count(p) as count")
        provision_count = result.single()["count"]
        assert provision_count > 0, "No provisions found in database"
        
        # Check for instruments
        result = session.run("MATCH (i:Instrument) RETURN count(i) as count")
        instrument_count = result.single()["count"]
        assert instrument_count > 0, "No instruments found in database"
        
        # Check for relationships
        result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
        relationship_count = result.single()["count"]
        assert relationship_count > 0, "No relationships found in database"
    
    db.close()


def test_health_check():
    """Test the health check functionality."""
    
    db.connect()
    
    health_data = db.health_check()
    
    assert health_data["status"] == "healthy"
    assert health_data["connected"] is True
    assert health_data["node_count"] > 0
    
    db.close()


if __name__ == "__main__":
    pytest.main([__file__])
