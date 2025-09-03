import os
import pickle
from typing import List, Tuple, Optional
import numpy as np
import faiss
from loguru import logger
from ..schemas.config import settings


class FAISSVectorDB:
    """FAISS vector database wrapper for similarity search."""
    
    def __init__(self, dimension: int = 1536):
        """Initialize FAISS index."""
        self.dimension = dimension
        self.index = None
        self.index_path = settings.faiss_index_path
        self.texts: List[str] = []
        self.metadata: List[dict] = []
        
    def create_index(self, index_type: str = "IndexFlatIP") -> bool:
        """Create FAISS index."""
        try:
            if index_type == "IndexFlatIP":
                self.index = faiss.IndexFlatIP(self.dimension)
            elif index_type == "IndexIVFFlat":
                # For larger datasets, use IVF
                quantizer = faiss.IndexFlatIP(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, 100)
            else:
                raise ValueError(f"Unsupported index type: {index_type}")
                
            logger.info(f"Created FAISS index: {index_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {e}")
            return False
            
    def add_vectors(
        self,
        vectors: List[List[float]],
        texts: List[str],
        metadata: Optional[List[dict]] = None
    ) -> bool:
        """Add vectors to the index."""
        if not self.index:
            logger.error("FAISS index not initialized")
            return False
            
        try:
            # Convert to numpy array
            vectors_np = np.array(vectors, dtype=np.float32)
            
            # Normalize vectors for cosine similarity
            faiss.normalize_L2(vectors_np)
            
            # Add to index
            self.index.add(vectors_np)
            
            # Store texts and metadata
            self.texts.extend(texts)
            if metadata:
                self.metadata.extend(metadata)
            else:
                self.metadata.extend([{} for _ in texts])
                
            logger.info(f"Added {len(vectors)} vectors to FAISS index")
            return True
        except Exception as e:
            logger.error(f"Failed to add vectors to FAISS: {e}")
            return False
            
    def search(
        self,
        query_vector: List[float],
        k: int = 10,
        threshold: float = 0.7
    ) -> List[Tuple[int, float, str, dict]]:
        """Search for similar vectors."""
        if not self.index:
            logger.error("FAISS index not initialized")
            return []
            
        try:
            # Convert query to numpy array and normalize
            query_np = np.array([query_vector], dtype=np.float32)
            faiss.normalize_L2(query_np)
            
            # Search
            scores, indices = self.index.search(query_np, k)
            
            # Filter by threshold and return results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1 and score >= threshold:
                    text = self.texts[idx] if idx < len(self.texts) else ""
                    meta = self.metadata[idx] if idx < len(self.metadata) else {}
                    results.append((int(idx), float(score), text, meta))
                    
            return results
        except Exception as e:
            logger.error(f"FAISS search error: {e}")
            return []
            
    def save(self) -> bool:
        """Save FAISS index and metadata."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            
            # Save index
            faiss.write_index(self.index, f"{self.index_path}.faiss")
            
            # Save metadata
            metadata_file = f"{self.index_path}.meta"
            with open(metadata_file, 'wb') as f:
                pickle.dump({
                    'texts': self.texts,
                    'metadata': self.metadata,
                    'dimension': self.dimension
                }, f)
                
            logger.info(f"Saved FAISS index to {self.index_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}")
            return False
            
    def load(self) -> bool:
        """Load FAISS index and metadata."""
        try:
            index_file = f"{self.index_path}.faiss"
            metadata_file = f"{self.index_path}.meta"
            
            if not os.path.exists(index_file) or not os.path.exists(metadata_file):
                logger.warning("FAISS index files not found")
                return False
                
            # Load index
            self.index = faiss.read_index(index_file)
            
            # Load metadata
            with open(metadata_file, 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.metadata = data['metadata']
                self.dimension = data['dimension']
                
            logger.info(f"Loaded FAISS index with {len(self.texts)} vectors")
            return True
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {e}")
            return False
            
    def get_stats(self) -> dict:
        """Get FAISS index statistics."""
        if not self.index:
            return {"error": "Index not initialized"}
            
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "texts_count": len(self.texts),
            "metadata_count": len(self.metadata),
            "index_type": type(self.index).__name__
        }
        
    def clear(self):
        """Clear the index and metadata."""
        self.index = None
        self.texts = []
        self.metadata = []
        logger.info("Cleared FAISS index")
