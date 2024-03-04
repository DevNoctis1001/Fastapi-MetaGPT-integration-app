# services/internal/ai_session/llm_agent.py

from typing import Any, List, Tuple, Union
from fastapi import HTTPException, logger
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.agents import BaseMultiActionAgent, AgentExecutor, Tool
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.conversational_chat.base import ConversationalChatAgent


from app.mongo_utils import PyObjectId
from ....database import db
from ....models import AISession, Message
from datetime import datetime
from ....core.config import settings


class LLMAgentService:
    def __init__(self, openai_api_key: str = settings.openai_api_key):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("You are a helpful chatbot engaged in a conversation."),
                MessagesPlaceholder(variable_name="chat_history"),
            ]
        )

        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True, memory=self.memory)
        self.agent = ConversationalChatAgent()
        self.agent_executor = AgentExecutor.from_agent_and_tools(self.agent, tools=[], verbose=True)



    # async def send_response(self, session_id: str, incoming_message: str):
    #     connection_string = settings.database_url
    #     message_history = MongoDBChatMessageHistory(
    #         connection_string=connection_string, session_id="test-session"
    #     )

    #     message_history.add_user_message("hi!")

    #     message_history.add_ai_message("whats up?")
    async def send_response(self, session_id: str, incoming_message: str):
        # Retrieve session and update message history
        session = await db["ai_sessions"].find_one({"_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        logger.info(f"Session: {session}")

        user_message = Message(content=incoming_message, sender="user")
        session["message_history"].append(user_message.model_dump())
        logger.info(f"User Message: {user_message}")

        # Save the incoming message to the conversation buffer
        self.memory.save_context({"input": incoming_message}, {"output": ""})
        # Generate the response using the conversational agent's plan method
        response_content = self.agent.aplan(intermediate_steps=session["message_history"], user_input=incoming_message)
        # Construct the response Message
        response = Message(content=response_content, sender="ai")
        # Save the response to the conversation buffer
        self.memory.save_context({"input": incoming_message}, {"output": response_content})
        # Update the session's message history with the response
        session["message_history"].append(response.model_dump())
        
        # Persist the updated session
        await db["ai_sessions"].replace_one({"_id": session_id}, session)

        return response