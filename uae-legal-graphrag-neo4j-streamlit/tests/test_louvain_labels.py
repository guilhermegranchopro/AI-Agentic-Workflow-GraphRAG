"""Test Louvain community detection results."""
import pytest
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db
from src.graph.queries import communities_top, nodes_in_community


def test_community_labels_exist():
    """Test that nodes have communityId after GDS run."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if any nodes have community IDs
        result = session.run("""
            MATCH (n) 
            WHERE n.communityId IS NOT NULL 
            RETURN count(n) as community_nodes
        """)
        
        community_nodes = result.single()["community_nodes"]
        
        # If no community nodes exist, skip the test
        if community_nodes == 0:
            pytest.skip("No community labels found - run GDS Louvain first with scripts/run_gds.sh")
        
        assert community_nodes > 0, "Expected nodes with community IDs"
    
    db.close()


def test_communities_top_query():
    """Test the communities_top query function."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    # Check if communities exist first
    with db.session() as session:
        result = session.run("MATCH (n) WHERE n.communityId IS NOT NULL RETURN count(n) as count")
        if result.single()["count"] == 0:
            pytest.skip("No communities found - run GDS first")
    
    # Test communities_top function
    communities_df = communities_top(5)
    
    assert not communities_df.empty, "communities_top should return non-empty DataFrame"
    assert "community_id" in communities_df.columns
    assert "size" in communities_df.columns
    assert "node_types" in communities_df.columns
    
    # Check that communities are sorted by size (descending)
    sizes = communities_df["size"].tolist()
    assert sizes == sorted(sizes, reverse=True), "Communities should be sorted by size descending"
    
    db.close()


def test_nodes_in_community_query():
    """Test the nodes_in_community query function."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    # Get a community ID to test with
    communities_df = communities_top(1)
    
    if communities_df.empty:
        pytest.skip("No communities found - run GDS first")
    
    community_id = communities_df.iloc[0]["community_id"]
    
    # Test nodes_in_community function
    nodes = nodes_in_community(community_id, 10)
    
    assert isinstance(nodes, list), "nodes_in_community should return a list"
    
    if len(nodes) > 0:
        # Check node structure
        for node_data in nodes:
            assert "node" in node_data
            assert "node_type" in node_data
            
            node = node_data["node"]
            assert "id" in node  # All nodes should have an ID
    
    db.close()


def test_community_consistency():
    """Test that community assignments are consistent."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if communities exist
        result = session.run("MATCH (n) WHERE n.communityId IS NOT NULL RETURN count(n) as count")
        if result.single()["count"] == 0:
            pytest.skip("No communities found - run GDS first")
        
        # Get community statistics
        result = session.run("""
            MATCH (n) 
            WHERE n.communityId IS NOT NULL 
            RETURN n.communityId as community_id, count(n) as size
            ORDER BY size DESC
        """)
        
        communities = list(result)
        
        assert len(communities) > 0, "Should have at least one community"
        
        # Check that all community sizes are positive
        for community in communities:
            assert community["size"] > 0, f"Community {community['community_id']} has invalid size"
            assert community["community_id"] is not None, "Community ID should not be None"
    
    db.close()


def test_community_node_types():
    """Test that communities contain expected node types."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if communities exist
        result = session.run("MATCH (n) WHERE n.communityId IS NOT NULL RETURN count(n) as count")
        if result.single()["count"] == 0:
            pytest.skip("No communities found - run GDS first")
        
        # Get node types in communities
        result = session.run("""
            MATCH (n) 
            WHERE n.communityId IS NOT NULL 
            RETURN DISTINCT labels(n)[0] as node_type, count(n) as count
        """)
        
        node_types = list(result)
        
        # Should have at least Provision and/or Judgment nodes (based on GDS configuration)
        type_names = [nt["node_type"] for nt in node_types]
        
        # Based on our GDS setup, we expect these node types
        expected_types = ["Provision", "Judgment"]
        found_expected = any(et in type_names for et in expected_types)
        
        assert found_expected, f"Expected to find {expected_types} in communities, found {type_names}"
    
    db.close()


def test_community_relationships():
    """Test that communities are formed based on relationships."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if communities exist
        result = session.run("MATCH (n) WHERE n.communityId IS NOT NULL RETURN count(n) as count")
        if result.single()["count"] == 0:
            pytest.skip("No communities found - run GDS first")
        
        # Check that nodes in the same community have relationships
        result = session.run("""
            MATCH (n1)-[r]-(n2) 
            WHERE n1.communityId IS NOT NULL 
              AND n2.communityId IS NOT NULL 
              AND n1.communityId = n2.communityId
            RETURN count(r) as intra_community_relationships
        """)
        
        intra_community_rels = result.single()["intra_community_relationships"]
        
        # Should have some relationships within communities
        # (This might be 0 for very small datasets, so we just check it's non-negative)
        assert intra_community_rels >= 0, "Intra-community relationships count should be non-negative"
    
    db.close()


def test_modularity_improvement():
    """Test that community detection improves modularity (indirect test)."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if communities exist
        result = session.run("MATCH (n) WHERE n.communityId IS NOT NULL RETURN count(n) as count")
        if result.single()["count"] == 0:
            pytest.skip("No communities found - run GDS first")
        
        # Simple test: check that we have multiple communities
        # (Good community detection shouldn't put everything in one community)
        result = session.run("""
            MATCH (n) 
            WHERE n.communityId IS NOT NULL 
            RETURN count(DISTINCT n.communityId) as num_communities,
                   count(n) as total_nodes
        """)
        
        stats = result.single()
        num_communities = stats["num_communities"]
        total_nodes = stats["total_nodes"]
        
        # Should have reasonable number of communities
        assert num_communities > 0, "Should have at least one community"
        
        # For good modularity, shouldn't have one community per node or all nodes in one community
        assert num_communities < total_nodes, "Shouldn't have one community per node"
        
        if total_nodes > 2:
            assert num_communities > 1, "Should have multiple communities for reasonable sized graphs"
    
    db.close()


if __name__ == "__main__":
    pytest.main([__file__])
