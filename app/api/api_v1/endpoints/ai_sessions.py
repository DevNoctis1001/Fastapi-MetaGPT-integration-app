from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, logger
from ....services.internal.langchain.chatbot import Chatbot
from ....dependencies import get_current_user_id
from ....core.config import settings
from ....models import AISession

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.agents import BaseMultiActionAgent, AgentExecutor, Tool
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import ConversationChain
from ....database import db
from ....models import AISession, Message, Conversation



import json
import datetime


router = APIRouter()
# llm_agent = Chat()
# manager = ConnectionManager()


@router.post("/chat", operation_id="chat")
async def chat_endpoint(
    session_id: str,
    conversation: Conversation,
    user_id: str = Depends(get_current_user_id),
) -> Any:
    # 0. Get the latest messages from the user
    new_message = conversation.model_dump()["conversation"][-1]
    
    # 1. Get the existing conversation from the db
    session: AISession = await db["ai_sessions"].find_one({"_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    logger.info(f"Session: {session}")
    existing_conversation = session.message_history
    
    # 2. Update the conversation with the latest conversation message (or just replace existing conversation)
    existing_conversation["conversation"].append(new_message)

    # 3. Call the ai to get the latest response
    chatbot = Chatbot()
    response = await chatbot.send_response(session_id, existing_conversation)
    
    response.raise_for_status()
    assistant_message = response.json()["reply"]
    
    # 4. Update the conversation and save to the db
    existing_conversation["conversation"].append({"role": "ai", "content": assistant_message})
    
    return existing_conversation

# Get all ai sessions that are in not completed from the user
@router.get("/sessions", operation_id="getSessions")
async def get_sessions(user_id: str = Depends(get_current_user_id)) -> AISession:
    sessions = await db["ai_sessions"].find({"user_id": user_id, "completed": False}).to_list(length=5)
    return sessions

# Update an ai session
@router.put("/sessions", operation_id="updateSession")
async def update_session(session: AISession, user_id: str = Depends(get_current_user_id)) -> AISession:
    session = await db["ai_sessions"].find_one_and_update({"_id": session._id}, {"$set": session})
    return session