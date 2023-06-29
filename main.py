from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Example data
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]

class User(BaseModel):
    id: int
    name: str

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return User(**user)
    return {"message": "User not found"}


