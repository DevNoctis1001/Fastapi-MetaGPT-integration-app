from openai import AsyncOpenAI
from ...core.config import settings

class OpenAI:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    def create_chat_message(self, system_message: str, user_message: str):
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

    async def get_chat_response(self, model: str, messages: list):
        response = await self.client.ChatCompletion.create(model=model, messages=messages)
        return response.choices[0].message.content

    async def send_chat_message(self, system_message: str, user_message: str, model="gpt-4"):
        messages = self.create_chat_message(system_message, user_message)
        return await self.get_chat_response(model, messages)
    
    async def get_embeddings(self, texts: list):
        responses = await self.client.Embedding.create(input=texts, engine="text-embedding-ada-002")
        return [response['embedding'] for response in responses['data']]

# Example usage (asynchronous context required)
# openai_manager = OpenAI()
# system_message = "You are a helpful assistant."
# user_message = "Tell me about the latest advancements in AI."
# response = await openai_manager.send_chat_message(system_message, user_message)
# print(response)
