"""Test as-of temporal traversal functionality."""
import pytest
import sys
import os
from datetime import date
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db
from src.graph.queries import asof_amendments, asof_neighbors


def test_asof_amendments():
    """Test as-of amendments query."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    # Test with a date where amendments should be visible
    test_date = date(2023, 7, 1)  # After the amendment valid_from date
    
    # Use the provision that has amendments in seed data
    provision_id = "civil-art-106"  # This provision has an amendment in seed data
    
    amendments = asof_amendments(provision_id, test_date)
    
    # Should find the amendment from seed data
    assert len(amendments) > 0, "Expected to find amendments for civil-art-106"
    
    # Check amendment structure
    for amendment in amendments:
        assert "id" in amendment
        assert "kind" in amendment
        assert "valid_from" in amendment
        # valid_to might be None for ongoing amendments
    
    db.close()


def test_asof_amendments_before_effective_date():
    """Test that amendments are not visible before their effective date."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    # Test with a date before the amendment
    test_date = date(2023, 5, 1)  # Before the amendment valid_from date
    
    provision_id = "civil-art-106"
    
    amendments = asof_amendments(provision_id, test_date)
    
    # Should not find amendments before their effective date
    assert len(amendments) == 0, "Should not find amendments before their effective date"
    
    db.close()


def test_asof_neighbors():
    """Test as-of neighbors traversal."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    test_date = date(2024, 1, 1)  # A date that should show relationships
    
    # Test with a provision that has relationships in seed data
    provision_id = "civil-art-106"  # This provision is cited by others
    
    neighbors = asof_neighbors(provision_id, test_date, ["CITES", "INTERPRETED_BY"])
    
    # Should find some neighbors based on seed data
    # The exact count depends on the seed data relationships
    
    # Check neighbor structure
    for neighbor in neighbors:
        assert "relationship_type" in neighbor
        assert "neighbor" in neighbor
        assert "path" in neighbor
        assert neighbor["relationship_type"] in ["CITES", "INTERPRETED_BY"]
    
    db.close()


def test_temporal_filtering():
    """Test that temporal filtering works correctly."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    # Test with provision that should have relationships
    provision_id = "civil-art-106"
    
    # Test at different dates
    early_date = date(2020, 1, 1)
    recent_date = date(2024, 1, 1)
    
    early_neighbors = asof_neighbors(provision_id, early_date)
    recent_neighbors = asof_neighbors(provision_id, recent_date)
    
    # Both should return results (our seed data is mostly static)
    # In a real system with temporal data, you'd expect differences
    
    assert isinstance(early_neighbors, list)
    assert isinstance(recent_neighbors, list)
    
    db.close()


def test_relationship_type_filtering():
    """Test filtering by relationship types."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    provision_id = "civil-art-106"
    test_date = date(2024, 1, 1)
    
    # Test with specific relationship types
    cite_neighbors = asof_neighbors(provision_id, test_date, ["CITES"])
    interpret_neighbors = asof_neighbors(provision_id, test_date, ["INTERPRETED_BY"])
    all_neighbors = asof_neighbors(provision_id, test_date, ["CITES", "INTERPRETED_BY"])
    
    # All results should respect the relationship type filter
    for neighbor in cite_neighbors:
        assert neighbor["relationship_type"] == "CITES"
    
    for neighbor in interpret_neighbors:
        assert neighbor["relationship_type"] == "INTERPRETED_BY"
    
    # Combined should be >= individual counts
    assert len(all_neighbors) >= len(cite_neighbors)
    assert len(all_neighbors) >= len(interpret_neighbors)
    
    db.close()


def test_nonexistent_provision():
    """Test behavior with nonexistent provision."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    test_date = date(2024, 1, 1)
    fake_provision_id = "fake-provision-123"
    
    # Should return empty results, not error
    amendments = asof_amendments(fake_provision_id, test_date)
    neighbors = asof_neighbors(fake_provision_id, test_date)
    
    assert amendments == []
    assert neighbors == []
    
    db.close()


def test_edge_case_dates():
    """Test behavior with edge case dates."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    provision_id = "civil-art-106"
    
    # Test with very early and very late dates
    very_early = date(1900, 1, 1)
    very_late = date(2100, 12, 31)
    
    early_amendments = asof_amendments(provision_id, very_early)
    late_amendments = asof_amendments(provision_id, very_late)
    
    # Should not error, even with extreme dates
    assert isinstance(early_amendments, list)
    assert isinstance(late_amendments, list)
    
    # Later date should show more or equal amendments
    assert len(late_amendments) >= len(early_amendments)
    
    db.close()


if __name__ == "__main__":
    pytest.main([__file__])
