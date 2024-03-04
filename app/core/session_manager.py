import uuid
import datetime
from fastapi import HTTPException
from ..models import SessionModel

class SessionManager:
    def __init__(self, session_model: SessionModel):
        self.session_model = session_model

    async def create_user_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # 1 hour expiration
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.datetime.now(),
            "last_activity": datetime.datetime.now(),
            "expires_at": expires_at
        }
        await self.session_model.create_session(session_data)
        return session_id

    async def validate_session(self, session_id: str) -> bool:
        session_data = await self.session_model.get_session(session_id)
        if not session_data or datetime.datetime.now() > session_data.get("expires_at", datetime.datetime.max):
            return False
        session_data["last_activity"] = datetime.datetime.now()
        await self.session_model.update_session(session_id, session_data)
        return True

    async def renew_session(self, session_id: str) -> str:
        new_token = str(uuid.uuid4())
        session_data = await self.session_model.get_session(session_id)
        session_data["token"] = new_token
        session_data["last_activity"] = datetime.datetime.now()
        await self.session_model.update_session(session_id, session_data)
        return new_token

    async def terminate_session(self, session_id: str):
        await self.session_model.delete_session(session_id)