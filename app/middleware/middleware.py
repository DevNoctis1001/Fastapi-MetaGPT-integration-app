from fastapi import Request, HTTPException
from ..core.session_manager import SessionManager

async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_manager = SessionManager(request.app.state.db)
        session = await session_manager.get_user_session(session_id)
        request.state.session = session
    else:
        request.state.session = None

    response = await call_next(request)
    return response
