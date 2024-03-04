import jwt
import time
import httpx
from ....models import User
from ....core.config import settings


client_id = settings.github_app_client_id
client_secret = settings.github_app_secret

async def get_installation_access_token(installation_id):
    jwt_token = create_jwt()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github.v3+json"}
        )
        return response.json()["token"]
    
def create_jwt():
    # JWT token generation
    now = int(time.time())
    payload = {
        'iat': now,
        'exp': now + (10 * 60),  # JWT token expires in 10 minutes
        'iss': settings.github_app_id  # Your GitHub App's identifier (App ID)
    }
    private_key = settings.github_app_private_key
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token

    

async def exchange_code(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code
            },
            headers={"Accept": "application/json"}
        )
        return response.json()

async def get_user_info(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}"}
        )
        return response.json()

async def get_installation_id(token: str):
    jwt_token = create_jwt()
    async with httpx.AsyncClient() as client:
        # Assuming the GitHub user has a single installation of the GitHub App
        response = await client.get(
            "https://api.github.com/app/installations",
            headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github.v3+json"}
        )
        installations = response.json()
        if installations:
            return installations[0]['id']
        return None

