import logging
from fastapi import APIRouter, HTTPException, Depends, Body
from ....models import Repository, AISession, StatusValue, Message
from ....database import db
from datetime import datetime
from ....dependencies import get_current_user_id
from typing import Any


router = APIRouter()


@router.post("/", operation_id="create_repository")
async def create_repository(
    repo_details: dict = Body(...),
    user_id: str = Depends(get_current_user_id),
) ->  str | None:
    logging.info("Creating new repository", repo_details)
    logging.info("Current user: %s", user_id)
    print(repo_details)

    # # Initialize new repository
    new_repository = Repository(
        user_id=user_id,
        name=repo_details["name"],
        description=repo_details["description"],
        visibility=repo_details["visibility"],
    )

    new_repository = await db["repositories"].insert_one(new_repository.model_dump())
    # Get the repositories id and save to a variable as a string
    new_repository_id = new_repository.inserted_id.__str__()
    print("New repository ID: ", new_repository_id)

    # Create the first AI Session linked to this repository
    first_ai_session = AISession(
        user_id=user_id,
        repository_id=new_repository_id,
        stages={
            "consult": "in_progress",
            "planning": "not_started",
            "coding": "not_started",
        },
        message_history=[
            Message(
                sender="AI",
                text="Hello there 👋 What do you want to build?",
                actions=[],
                created_at=datetime.now(),
            ),
        ],
    )

    insert_result = await db["ai_sessions"].insert_one(first_ai_session.model_dump())
    inserted_id = insert_result.inserted_id

    first_ai_session: AISession = await db["ai_sessions"].find_one({"_id": inserted_id})

    print("First AI Session: ", first_ai_session)

    # Assuming the 'model_dump()' method returns a dictionary with an 'id' field
    return inserted_id.__str__()



# Additional endpoints for updating repositories, retrieving repository details, etc.
@router.get("/", operation_id="get_repositories")
async def get_repositories(
    user_id=Depends(get_current_user_id),
) -> list[Repository] | None:
    logging.info("Getting repositories")
    logging.info("Current user: %s", user_id)
    # print("Getting repositories")
    # print("Current user: ", user_id)

    # repositories = (
    #     await db["repositories"].find({"user_id": user_id}).to_list(length=10)
    # ): list[Repository]
    repositories = [
        Repository(**document)
        for document in await db["repositories"]
        .find({"user_id": user_id})
        .to_list(length=10)
    ]
    return repositories
