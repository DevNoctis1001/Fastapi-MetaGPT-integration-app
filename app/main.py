import os
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
import uvicorn
from contextlib import asynccontextmanager
import socketio
from fastapi_socketio import SocketManager
import logging
from .database import connect_to_mongo, close_mongo_connection
from .api.api_v1.endpoints import ai_sessions, users, repos
from .api.api_v1.endpoints import generate
from .api.auth import auth
from .services.external.github import github 
from .services.internal.websocket_manager import ConnectionManager
from .core import config
from jose import JWTError, jwt
from .models import Webhook, Branch, Commit, Action, Message, Question, ConsultScaffold, Task, ChatRequest, Conversation, AISession, Repository, RateLimit, User
# If metagpt is located in a subfolder, uncomment this with the correct path
# to add it to the Python path
# import sys
# sys.path.append('/path/to/metagpt')  # Replace with the actual path




# Database connection using lifespan event handlers 
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup ")
    await connect_to_mongo()
    yield
    # Clean up the ML models and release the resources
    print("Server shutdown")
    await close_mongo_connection()
    
# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
# manager = ConnectionManager(sio)  # Create an instance of ConnectionManager with the Socket.IO server

    
app = FastAPI(lifespan=lifespan,
              title="ProjectX",
    description="Develop your next app in minutes with AI Agents.",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        
        "email": "info@projectxlabs.co",
    },
    servers=[{"url": "http://localhost:8000", "description": "Development server"}],

)
# app.mount('/', manager.get_app())
origins = [
    "http://localhost:3000",  # The origin of your frontend
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different endpoints
app.include_router(ai_sessions.router, prefix="/api/v1/ai_sessions", tags=["ai_sessions"])
app.include_router(repos.router, prefix="/api/v1/repos", tags=["repos"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])


@app.get("/", operation_id="getApiRoot")
async def root():
    return {"message": "Hello World"}



# ------------------ OpenAPI schema models (for generation of frontend models) ------------------
# Dummy endpoint to include models in OpenAPI schema
@app.get("/models", response_model=Union[Webhook, Branch, Commit, Action, Message, Question, ConsultScaffold, Task, ChatRequest, Conversation, AISession, Repository, RateLimit, User], include_in_schema=False)
def models():
    raise HTTPException(status_code=404, detail="This endpoint is not intended for use.")
