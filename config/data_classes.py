from pydantic import BaseModel
class Response(BaseModel):
    status : int
    message: str
    token: str

class Message(BaseModel):
    role: str
    content: str

class User(BaseModel):
    Username: str
    Password: str

class ChatResponse(BaseModel):
    status: int
    messages: list[Message]


class Session(BaseModel):
    sessionId: int
    question: str

class createSession(BaseModel):
    userId: int
    sessionname: str
