# https://pypi.org/project/instructor/
# https://www.youtube.com/watch?v=yj-wSRJwrrc

from pydantic import BaseModel
from openai import OpenAI
import instructor

# Enables `response_model`
client = instructor.patch(OpenAI())

class UserDetail(BaseModel):
    name: str
    age: int

user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": "Extract Jason is 25 years old"},
    ]
)

assert isinstance(user, UserDetail)
assert user.name == "Jason"
assert user.age == 25


# # Async Version
# import instructor
# from openai import AsyncOpenAI

# aclient = instructor.apatch(AsyncOpenAI())

# class UserExtract(BaseModel):
#     name: str
#     age: int

# model = await aclient.chat.completions.create(
#     model="gpt-3.5-turbo",
#     response_model=UserExtract,
#     messages=[
#         {"role": "user", "content": "Extract jason is 25 years old"},
#     ],
# )

# assert isinstance(model, UserExtract)