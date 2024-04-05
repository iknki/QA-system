import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging


from config.data_classes import Response, Message, User, ChatResponse, Session, createSession
from chat.ChatApi import get_chat_response

from db.ES.ESApi import ESApi
from db.Mysql.MysqlApi import MysqlApi


# from config.config import Config
# from llmmodel.model import Model


app = FastAPI()
# config = Config("./config.yaml")
# Model(config)
# 日志记录器
logger = logging.getLogger()
# 设置日志级别，只有大于等于这个级别的日志才能输出
logger.setLevel(logging.ERROR)

# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

# 输出到控制台
to_console = logging.StreamHandler()
to_console.setFormatter(formatter)
logger.addHandler(to_console)


# 允许所有域的请求访问后端接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mysql = MysqlApi()


@app.get("/api/status")
def status():
    return {"status": "ok"}

async def QA():
    start_time = time.time()


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""用户登录接口"""
# 注册接口
@app.post("/api/register")
async def register(UserRegistration: User):
    logger.info(UserRegistration)
    # 执行注册用户的逻辑
    response = mysql.create_user(UserRegistration.Username, UserRegistration.Password)
    return response
# 登陆接口
@app.post("/api/login")
async def register(UserRegistration: User):
    logger.info(UserRegistration)
    # 执行登陆用户的逻辑
    response = mysql.validate_user(UserRegistration.Username, UserRegistration.Password)
    return response


"""Chat对话接口"""
# 获得历史对话
@app.get("/api/chat/GetConversationHistory")
async def chat_getmessages(sessionId: int):
    response = mysql.get_conversation(sessionId)
        
    return response

# 获得对话回答
@app.post("/api/chat/GetChatAnswer")
async def chat_getmessages(session: Session):
    content = get_chat_response(session.question, 'book')
    messages = []
    messages.append(Message(role="robot", content=content))
    mysql.create_conversation(session.sessionId, [Message(role='user', content=session.question),
                                                  Message(role='robot', content=content)])
    return ChatResponse(status=0,messages=messages)


"""Session接口"""
# 获得Session列表
@app.get("/api/session/GetSessionList")
async def session_sessionlist(userid: int):
    response = mysql.get_sessionList(userid)
    return response

# 创建Session
@app.post("/api/session/CreateSession")
async def session_createsession(session: createSession):
    response = mysql.create_session(session.userId, session.sessionname)
    mysql.create_conversation(
        response['session']['sessionid'],
        Message(role="robot", content="你好，我是机器人小助手，有什么可以帮助你的吗？"),
    )
    return response
