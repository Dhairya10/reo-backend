import vecs
from typing import List, Dict, Union, Optional
import numpy as np

class SupabaseVectorDB:
    def __init__(self, db_connection: str, collection_name: str, dimension: int = 1536):
        """
        Initialize the SupabaseVectorDB client.
        
        :param db_connection: PostgreSQL connection string
        :param collection_name: Name of the vector collection
        :param dimension: Dimension of the vectors (default is 1536 for OpenAI embeddings)
        """
        try:
            self.client = vecs.create_client(db_connection)
            self.collection = self.client.get_or_create_collection(name=collection_name, dimension=dimension)
            print(f"Successfully connected to collection: {collection_name}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Supabase: {str(e)}")

    def add_vectors(self, records: List[tuple], batch_size: int = 1000):
        """
        Add vectors to the collection.
        
        :param records: List of tuples (id, vector, metadata)
        :param batch_size: Number of records to upsert in each batch
        """
        try:
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                self.collection.upsert(records=batch)
            print(f"Successfully added {len(records)} vectors to the collection.")
        except Exception as e:
            raise RuntimeError(f"Failed to add vectors: {str(e)}")

    def query_vectors(self, 
                      query_vector: Union[List[float], np.ndarray],
                      limit: int = 5,
                      filters: Optional[Dict] = None,
                      measure: str = "cosine_distance",
                      include_value: bool = False,
                      include_metadata: bool = True) -> List[Dict]:
        """
        Query vectors from the collection.
        
        :param query_vector: The query vector
        :param limit: Number of results to return
        :param filters: Metadata filters
        :param measure: Distance measure to use
        :param include_value: Include distance values in results
        :param include_metadata: Include metadata in results
        :return: List of query results
        """
        try:
            results = self.collection.query(
                data=query_vector,
                limit=limit,
                filters=filters or {},
                measure=measure,
                include_value=include_value,
                include_metadata=include_metadata
            )
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query vectors: {str(e)}")

    def create_index(self, method: str = "auto", measure: str = "cosine_distance"):
        """
        Create an index for the collection.
        
        :param method: Indexing method ('auto', 'hnsw', or 'ivfflat')
        :param measure: Distance measure for the index
        """
        try:
            self.collection.create_index(method=method, measure=measure)
            print(f"Successfully created index with method: {method} and measure: {measure}")
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {str(e)}")

    def delete_vectors(self, ids: Optional[List[str]] = None, filters: Optional[Dict] = None):
        """
        Delete vectors from the collection.
        
        :param ids: List of vector IDs to delete
        :param filters: Metadata filters for deletion
        """
        try:
            if ids:
                deleted = self.collection.delete(ids=ids)
            elif filters:
                deleted = self.collection.delete(filters=filters)
            else:
                raise ValueError("Either 'ids' or 'filters' must be provided for deletion.")
            print(f"Successfully deleted {len(deleted)} vectors from the collection.")
        except Exception as e:
            raise RuntimeError(f"Failed to delete vectors: {str(e)}")

    def __del__(self):
        """Cleanup method to disconnect the client when the object is destroyed."""
        if hasattr(self, 'client'):
            self.client.disconnect()
            print("Disconnected from Supabase.")


'''

# Initialize the client
db = SupabaseVectorDB(
    db_connection="postgresql://<user>:<password>@<host>:<port>/<db_name>",
    collection_name="my_vectors",
    dimension=1536
)

# Add vectors
vectors_to_add = [
    ("id1", [0.1, 0.2, 0.3, ...], {"metadata": "data1"}),
    ("id2", [0.4, 0.5, 0.6, ...], {"metadata": "data2"}),
    # ... more vectors
]
db.add_vectors(vectors_to_add)

# Create an index (optional, but recommended for performance)
db.create_index()

# Query vectors
query_result = db.query_vectors(
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=5,
    filters={"metadata": {"$eq": "data1"}}
)

# Delete vectors
db.delete_vectors(ids=["id1", "id2"])


-------------------------------------------

# Adding a vector with metadata
db.add_vectors([
    ("doc1", [0.1, 0.2, 0.3, ...], {"author": "Jane Doe", "date": "2023-07-21", "category": "science"})
])

# Querying with a metadata filter
results = db.query_vectors(
    query_vector=[0.1, 0.2, 0.3, ...],
    filters={"category": {"$eq": "science"}, "date": {"$gte": "2023-01-01"}}
)

'''