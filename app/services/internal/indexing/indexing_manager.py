from datetime import datetime
from ...models import User
from .pinecone_manager import PineconeManager
from ..github.github_manager import GitHubManager
from typing import List, Dict, Any
import openai

class IndexingManager:
    def __init__(self, db, pinecone_api_key: str, pinecone_environment: str, github_api_key: str):
        self.db = db
        self.pinecone_manager = PineconeManager(pinecone_api_key, pinecone_environment)
        self.github_manager = GitHubManager(github_api_key)

    async def start_indexing(self, repo_id: str, user: User):
        repo_data = await self.github_manager.get_repo_contents(repo_id, user)
        vectors = await self.get_repo_embeddings(repo_data)
        self.pinecone_manager.create_index(repo_id, len(vectors[0]))
        self.pinecone_manager.upsert_vectors(repo_id, [d['id'] for d in repo_data], vectors)
        await self.update_index_status(repo_id, True)

    async def get_repo_embeddings(self, repo_data: List[Dict[str, Any]]) -> List[List[float]]:
        openai.api_key = 'your-openai-api-key'  # Replace with your actual OpenAI API key
        embeddings = []
        for item in repo_data:
            response = openai.Embedding.create(input=item['content'], engine="text-similarity-babbage-001")
            embeddings.append(response['data'][0]['embedding'])
        return embeddings

    async def update_index_status(self, repo_id: str, is_indexed: bool):
        await self.db['repo_details'].update_one(
            {'_id': repo_id},
            {'$set': {'is_indexed': is_indexed, 'last_indexed': datetime.now()}}
        )
