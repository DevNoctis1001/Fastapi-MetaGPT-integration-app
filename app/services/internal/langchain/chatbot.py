# Watch this to see how https://www.youtube.com/watch?v=I_4jEnDwGwI

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
import openai
from langchain.prompts import PromptTemplate
import logging
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from ....database import db
from ....models import AISession, Message
from datetime import datetime
from ....core.config import settings
from .prompts import prompt_template


ROLE_CLASS_MAP = {"assistant": AIMessage, "user": HumanMessage, "system": SystemMessage}


def create_messages(conversation):
    return [
        ROLE_CLASS_MAP[message.role](content=message.content)
        for message in conversation
    ]


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    conversation: List[Message]


class Chatbot:
    def __init__(self, openai_api_key: str = settings.openai_api_key):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key)

    def send_response(self, conversation: Conversation):
        prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)
        chat = ChatOpenAI(temperature=0)

        messages = [prompt] + create_messages(conversation=conversation.conversation)

        response = chat(messages)

        return response
