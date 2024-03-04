import pinecone
import pandas as pd
from typing import List, Dict
from ....core.config import settings

api_key = settings.pinecone_api_key
environment = settings.pinecone_environment

class Pinecone:
    def __init__(self):
        pinecone.init(api_key=api_key, environment=environment)

    def create_index(self, index_name: str, dimension: int, metric: str = "cosine"):
        pinecone.create_index(name=index_name, dimension=dimension, metric=metric)

    def upsert_vectors(self, index_name: str, ids: List[str], vectors: List[List[float]]):
        data_df = pd.DataFrame({"id": ids, "vector": vectors})
        index = pinecone.Index(index_name)
        index.upsert(vectors=data_df.to_dict(orient='records'))

    def query_index(self, index_name: str, query_vectors: List[List[float]], top_k: int):
        index = pinecone.Index(index_name)
        return index.query(queries=query_vectors, top_k=top_k)

    def delete_index(self, index_name: str):
        pinecone.delete_index(name=index_name)
