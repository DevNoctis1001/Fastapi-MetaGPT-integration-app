import jwt
import httpx
from octokit import Octokit
from ....models import User  # Assuming the User model is defined in models.py
from ....core.config import settings
from ....core.session_manager import SessionManager
from ....database import db
from .utils import get_installation_access_token, create_jwt

class GitHub:
    def __init__(self):
        self.octokit = Octokit(type='app', token=create_jwt())
        
    async def get_repos(self,  user: User, repo_id: str | None = None):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.repos.list_for_authenticated_user(
            token=installation_token
        )
        return response.json()
    
    async def create_repo(self, user: User, repo_name: str):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.repos.create_for_authenticated_user(
            name=repo_name, token=installation_token
        )
        return response.json()
        
    async def get_repo_contents(self, repo_id: str, user: User):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.repos.get_contents(
            owner=user.username, repo=repo_id, token=installation_token
        )
        return response.json()
    
    async def create_branch(self, repo_id: str, branch_id: str, user: User):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.git.create_ref(
            owner=user.username, repo=repo_id,
            ref=f'refs/heads/{branch_id}', sha='start_commit_sha',
            token=installation_token
        )
        return response.json()

    async def get_branch(self, repo_id: str, branch_id: str, user: User):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.git.get_ref(
            owner=user.username, repo=repo_id, ref=f'refs/heads/{branch_id}',
            token=installation_token
        )
        return response.json()

    async def create_commit(self, repo_id: str, branch_id: str, user: User, commit_message: str, tree_sha: str, parent_commit_sha: str):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.git.create_commit(
            owner=user.username, repo=repo_id, message=commit_message,
            tree=tree_sha, parents=[parent_commit_sha],
            token=installation_token
        )
        return response.json()

    async def get_commit(self, repo_id: str, branch_id: str, user: User):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.repos.list_commits(
            owner=user.username, repo=repo_id, sha=branch_id,
            token=installation_token
        )
        return response.json()

    async def create_pull_request(self, repo_id: str, user: User, head: str, base: str, title: str, body: str):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.pulls.create(
            owner=user.username, repo=repo_id, head=head, base=base,
            title=title, body=body, token=installation_token
        )
        return response.json()

    async def get_pull_request(self, repo_id: str, user: User):
        installation_token = await get_installation_access_token(user)
        response = await self.octokit.pulls.list(
            owner=user.username, repo=repo_id, token=installation_token
        )
        return response.json()

