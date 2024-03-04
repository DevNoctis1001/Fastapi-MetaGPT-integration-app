from fastapi import APIRouter, HTTPException, Depends
from ....database import db
from bson import ObjectId
from ....dependencies import get_current_user_id
from ....models import User

router = APIRouter()


@router.post("/", response_model=User, operation_id="create_user")
async def create_user(user: User):
    if await db.db["users"].find_one({"github_id": user.github_id}):
        raise HTTPException(status_code=400, detail="User already registered")
    await db.db["users"].insert_one(user.model_dump())
    return user
    # if await db.db["users"].find_one({"github_id": user.github_id}):
    #     raise HTTPException(status_code=400, detail="User already registered")
    # await db.db["users"].insert_one(user.dict())
    # return user


@router.get("/", response_model=User, operation_id="get_user")
async def get_user(user_id: str):
    user = await db.db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/", response_model=User, operation_id="update_user")
async def update_user(user_id: str, user: User):
    updated_user = await db.db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)}, {"$set": user.dict()}, return_document=True
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/", operation_id="delete_user")
async def delete_user(user_id: str):
    result = await db.db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
