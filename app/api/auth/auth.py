# auth.py
from fastapi.responses import JSONResponse
from ast import Dict
import time
from fastapi import APIRouter, Body, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from ...core.config import settings
from ...core.session_manager import SessionManager
from ...models import SessionModel
from ...database import db
from ...services.external.github.utils import get_installation_access_token, get_installation_id, create_jwt
import httpx


router = APIRouter()
client_oauth_id = settings.github_oauth_client_id
client_oauth_secret = settings.github_oauth_client_secret

client_app_id = settings.github_app_client_id
client_app_secret = settings.github_app_secret

session_manager = SessionManager(SessionModel(db))

@router.get("/login")
async def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={client_oauth_id}"
    )


@router.get("/github-oauth/callback")
async def oauth_callback(code: str):
    try:
        # POST it back to GitHub in exchange for an access token
        async with httpx.AsyncClient() as client:
            url = f'https://github.com/login/oauth/access_token?client_id={settings.github_oauth_client_id}&scope=user%20repo%20codespace' \
                f'&client_secret={settings.github_oauth_client_secret}&code={code}'
            headers = {'Accept': 'application/json'}

            response = await client.post(url, headers=headers)

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to get access token")

            # Extract the token and granted scopes
            access_token = response.json().get('access_token')
            
            # Fetch user data using the access token
            user_response = await client.get(
                'https://api.github.com/user',
                headers={'Authorization': f'token {access_token}'}
            )
            user_response.raise_for_status()
            user_data = user_response.json()
            user_id = user_data["id"]
            print(user_data)
            
            
            
            user = await db["users"].update_one(
                {"id": user_id},
                {"$set": {
                    "profile": {
                        "name": user_data["name"],
                        "email": user_data["email"],
                        "github_profile_url": user_data["html_url"]
                    },
                    "access_token": access_token
                }},
                upsert=True
            )
            # http://localhost:8000/api/v1/auth/logi
            
        print("Successfully logged in!")
        # return {"message": "Successfully logged in!"}
        # # Redirect to GitHub App installation after successful OAuth
        
        # Check if the user object already has an installation id
        updated_user = await db["users"].find_one({"id": user_id})
        


        # Redirect based on the presence of github_app_installation_id
        if "github_app_installation_id" not in updated_user:
            return RedirectResponse(
                f"https://github.com/apps/{settings.github_app_name}/installations/new"
            )
        else:
            session_id = await session_manager.create_user_session(user_id)
            print
            # Set the session_id in a secure, HTTP-only cookie
            response = JSONResponse(content={"message": "Successfully logged in! User already had installation id", "session_id": session_id })
            response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)

            # return response
            # Return the user to the frontend base url with the session
            return RedirectResponse(
                url=f"{settings.frontend_url}/dashboard?session_id={session_id}",
                status_code=303 # Redirect as GET
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in GitHub Oauth callback: {str(e)}")


@router.get("/github-app/callback")
async def app_callback(code: str, installation_id: str, setup_action: str):
    try:
        token_data = await exchange_code(code)
        if "access_token" in token_data:
            token = token_data["access_token"]
            user_info = await get_user_info(token)
            print(user_info)
            # installation_id = await get_installation_id(token)

            if installation_id:
                print(installation_id)
                installation_access_token = await get_installation_access_token(installation_id)
                

                # Upsert user data
                user_data = {
                    "id": user_info["id"],
                    "github_app_installation_id": installation_id,
                    "access_token": installation_access_token,
                    # Other fields as needed
                }
                await db["users"].update_one(
                    {"id": user_info["id"]}, 
                    {"$set": user_data}, 
                    upsert=True
                )
                
                # Create a session for the user
                session_id = await session_manager.create_user_session(user_info["id"])
                print(session_id)
                # Set the session_id in a secure, HTTP-only cookie
                response = JSONResponse(content={"message": "Successfully logged in!", "session_id": session_id })
                response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)
                
                # Return the user to the frontend base url with the session
                return RedirectResponse(
                    url=f"{settings.frontend_url}/dashboard?session_id={session_id}",
                    status_code=303 # Redirect as GET
                )

                # return f"Successfully installed github app! Welcome, {user_info.get('name', 'Unknown User')}."
            else:
                return "No valid GitHub App installation found for the user."
        else:
            return "Authorized, but unable to exchange code for token."
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def exchange_code(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": client_app_id,
                "client_secret": client_app_secret,
                "code": code
            },
            headers={"Accept": "application/json"}
        )
        
        access_token = response.json()
        print(access_token)
        
        return access_token
    
    
async def get_user_info(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}"}
        )
        return response.json()


# @router.post("/logout")
# async def logout(response: Response, session_id: str = Depends(get_current_session_id)):
#     if not session_id:
#         raise HTTPException(status_code=401, detail="No active session found")

#     # Invalidate the session in the database
#     await session_manager.terminate_session(session_id)

#     # Clear the session cookie in the response
#     response.delete_cookie(key="session_id")
#     return {"message": "Successfully logged out"}