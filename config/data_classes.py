from pydantic import BaseModel
from typing import Optional
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

class CreateSession(BaseModel):
    userId: int
    sessionname: str


class DeleteSession(BaseModel):
    sessionId: int

class CreateKnowledgeBase(BaseModel):
    userId: int
    kbname: str
    info: str

class KnowledgeBase(BaseModel):
    kbId: int
    kbname: str
    info: str

class CreateKnowledge(BaseModel):
    kbid: int
    title: str
    info: str
    userid: int
    istrain: str

class EditKnowledge(BaseModel):
    knowledgeid: int
    title: str
    info: str
    istrain: str

class CreateModel(BaseModel):
    pastmodelid: Optional[int] = None
    modelname: str
    info: str
    userid: int
    knowledgeIDList: list[int]

class EditModel(BaseModel):
    modelid: int
    modelname: str
    info: str
    userid: int
    status: str
