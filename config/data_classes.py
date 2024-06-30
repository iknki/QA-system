from pydantic import BaseModel
from typing import Optional
import json

class UserInfo(BaseModel):
    username: str
    userid: int
    nickname: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    area: Optional[str] = None
    job: Optional[str] = None


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
    UserID: Optional[int] = None
    Role: Optional[str] = None

class ChatResponse(BaseModel):
    status: int
    messages: list[Message]


class Session(BaseModel):
    sessionId: int
    userId: int
    question: str

class CreateSession(BaseModel):
    userId: int
    sessionname: str


class DeleteSession(BaseModel):
    sessionId: int
    userId: int

class CreateKnowledgeBase(BaseModel):
    userId: int
    kbname: str
    info: str

class KnowledgeBase(BaseModel):
    kbId: int
    kbname: str
    info: str
    userId: int

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
    userid: int

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

class Settings(BaseModel): 
    data : dict
