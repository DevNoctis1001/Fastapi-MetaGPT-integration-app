# https://gist.github.com/jvelezmagic/03ddf4c452d011aae36b2a0f73d72f68

import asyncio
from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel
from ....core.config import settings
from ....models import ChatRequest

CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You're a AI that knows everything about cats."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

class StreamingConversationChain:
    """
    Class for handling streaming conversation chains.
    It creates and stores memory for each conversation,
    and generates responses using the ChatOpenAI model from LangChain.
    """

    def __init__(
        self, openai_api_key: str = settings.openai_api_key, temperature: float = 0.0
    ):
        self.memories = {}
        self.openai_api_key = openai_api_key
        self.temperature = temperature

    

    async def generate_response(
        self, session_id: str, message: str
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronous function to generate a response for a conversation.
        It creates a new conversation chain for each message and uses a
        callback handler to stream responses as they're generated.

        :param session_id: The ID of the conversation (stored in the ai session).
        :param message: The message from the user.
        """
        callback_handler = AsyncIteratorCallbackHandler()
        llm = ChatOpenAI(
            callbacks=[callback_handler],
            streaming=True,
            temperature=self.temperature,
            openai_api_key=self.openai_api_key,
        )

        memory = self.memories.get(session_id)
        if memory is None:
            memory = ConversationBufferMemory(return_messages=True)
            self.memories[session_id] = memory

        chain = ConversationChain(
            memory=memory,
            prompt=CHAT_PROMPT_TEMPLATE,
            llm=llm,
        )

        run = asyncio.create_task(chain.arun(input=message))

        async for token in callback_handler.aiter():
            yield token

        await run


