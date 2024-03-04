from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import shutil
import logging
from fastapi import APIRouter, HTTPException, Depends, Body, Request
from ....models import Repository, AISession, StatusValue, Message
from ....database import db
from datetime import datetime
from ....dependencies import get_current_user_id
from typing import Any
from ..utils.generate_utils import upload_to_github, simulate_metagpt_output

router = APIRouter()


@router.post("/", operation_id="generate")
async def generate(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    body = await request.json()
    print(body)
    # Simulate getting output from MetaGPT
    codebase_path = simulate_metagpt_output()

    # Upload to GitHub
    try:
        upload_to_github(body.repo_name, codebase_path, "your-github-token")
        return {"message": "Codebase uploaded to GitHub", codebase_path: codebase_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
