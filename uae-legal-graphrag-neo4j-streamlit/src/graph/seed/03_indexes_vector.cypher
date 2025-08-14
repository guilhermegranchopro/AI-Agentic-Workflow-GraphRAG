// Create vector index for provision embeddings
CREATE VECTOR INDEX prov_embedding_index IF NOT EXISTS
FOR (p:Provision) ON (p.embedding)
OPTIONS { indexConfig: { `vector.dimensions`: $dim, `vector.similarity_function`: 'cosine' } };
