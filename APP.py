import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Optional


from config.data_classes import Message, User, ChatResponse, Session, CreateSession, DeleteSession, CreateKnowledgeBase, KnowledgeBase, CreateKnowledge, EditKnowledge, CreateModel, EditModel
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
es = ESApi("elastic", "9YfcLUcxKiDvtzef1piK")


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
async def chat_get_messages(sessionId: int):
    response = mysql.get_conversation(sessionId)
        
    return response

# 获得对话回答
@app.post("/api/chat/GetChatAnswer")
async def chat_get_messages(session: Session):
    content = get_chat_response(session.question, "202mp6w1r6")
    messages = []
    messages.append(Message(role="robot", content=content))
    mysql.create_conversation(session.sessionId, [Message(role='user', content=session.question),
                                                  Message(role='robot', content=content)])
    return ChatResponse(status=0,messages=messages)


"""Session接口"""
# 获得Session列表
@app.get("/api/session/GetSessionList")
async def session_get_sessionlist(userid: int):
    response = mysql.get_sessionList(userid)
    return response

# 创建Session
@app.post("/api/session/CreateSession")
async def session_create_session(session: CreateSession):
    response = mysql.create_session(session.userId, session.sessionname)
    mysql.create_conversation(
        response['session']['sessionid'],
        [Message(role="robot", content="你好，我是机器人小助手，有什么可以帮助你的吗？")],
    )
    return response

# 删除Session
@app.post("/api/session/DeleteSession")
async def session_delete_session(session: DeleteSession):
    response = mysql.delete_session(session.sessionId)
    return response


"""KnowledgeBase接口"""
# 获得知识库列表
@app.get("/api/knowledgebase/GetKBList")
async def knowledgebase_get_kblist(userId: str):
    response = mysql.get_kbList(userId)
    return response


# 创建知识库
@app.post("/api/knowledgebase/CreateKB")
async def knowledgebase_create_kb(createKnowledgeBase: CreateKnowledgeBase):
    response = es.create_index_mysql(createKnowledgeBase.kbname, createKnowledgeBase.info, createKnowledgeBase.userId)
    return response

# 编辑知识库
@app.post("/api/knowledgebase/EditKB")
async def knowledgebase_edit_kb(knowledgeBase: KnowledgeBase):
    response = mysql.edit_kb(knowledgeBase.kbId, knowledgeBase.kbname, knowledgeBase.info)
    return response

# 删除知识库
@app.get("/api/knowledgebase/DeleteKB")
async def knowledgebase_delete_kb(indices: str):
    es.delete_index(indices)
    response = mysql.delete_kb(indices)
    return response


"""Knowledge接口"""
# 获得知识列表
@app.get("/api/knowledge/GetKnowledgeList")
async def knowledge_get_knowledgelist(
    pagenum: int,
    pagesize: int,
    userid: int,
    kbid: Optional[int] = None,
    title: Optional[str] = None,
    istrain: Optional[str] = None,
):
    response = mysql.get_knowledgeList(pagenum, pagesize, kbid, title, userid, istrain)
    return response


# 创建知识
@app.post("/api/knowledge/CreateKnowledge")
async def knowledge_create_knowledge(knowledge: CreateKnowledge):
    index_name = mysql.get_indices(knowledge.kbid, 0)
    response = mysql.create_knowledge(
        index_name,
        knowledge.title,
        knowledge.info,
        knowledge.userid,
        knowledge.istrain,
    )
    if es.add_document(index_name, {"title": knowledge.title, "info": knowledge.info}, response["knowledge"]["knowledgeid"]) != True:
        mysql.delete_knowledge(response["knowledge"]["knowledgeid"])
        response = {"status": 405, "message": "添加知识失败！"}
    return response

# 编辑知识
@app.post("/api/knowledge/EditKnowledge")
async def knowledge_edit_knowledge(knowledge: EditKnowledge):
    index_name = mysql.get_indices(knowledge.knowledgeid, 1)
    es.update_document(index_name, {"title": knowledge.title, "info": knowledge.info}, knowledge.knowledgeid)
    response = mysql.edit_knowledge(knowledge.knowledgeid, knowledge.title, knowledge.info, knowledge.istrain)
    return response

# 删除知识
@app.get("/api/knowledge/DeleteKnowledge")
async def knowledge_delete_knowledge(knowledgeid: int):
    index_name = mysql.get_indices(knowledgeid, 1)
    es.delete_document(index_name, knowledgeid)
    response = mysql.delete_knowledge(index_name, knowledgeid)
    return response


"""推荐模型接口"""
# 获得model列表
@app.get("/api/model/GetModelList")
async def model_get_modellist(userid: int):
    response = mysql.get_modelList(userid)
    return response

# 创建model
@app.post("/api/model/CreateModel")
async def model_create_model(createModel: CreateModel):
    response = mysql.create_model(createModel.modelname, createModel.info, createModel.userid)
    if response["status"] == 0:
        mysql.create_log(
            createModel.userid, "创建模型 {" + createModel.modelname + "}", "成功"
        )
    else:
        mysql.create_log(
            createModel.userid,
            "创建模型 {" + createModel.modelname + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 编辑model
@app.post("/api/model/EditModel")
async def model_edit_model(model: EditModel):
    response = mysql.edit_model(model.modelid, model.modelname, model.info, model.status)
    if response["status"] == 0:
        mysql.create_log(model.userid, "编辑模型 {" + model.modelname + "}", "成功")
    else:
        mysql.create_log(
            model.userid,
            "编辑模型 {" + model.modelname + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 删除model
@app.get("/api/model/DeleteModel")
async def model_delete_model(modelid: int, userid: int):
    response = mysql.delete_model(modelid)
    if response["status"] == 0:
        mysql.create_log(userid, "删除模型 {" + response["modelname"] + "}", "成功")
    else:
        mysql.create_log(
            userid,
            "删除模型 {" + response["modelname"] + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response


"""日志接口"""
# 获得日志列表
@app.get("/api/log/GetLogList")
async def log_get_loglist(pagenum: int, pagesize: int, userid: int):
    response = mysql.get_logList(pagenum, pagesize)
    return response

# 删除日志
@app.get("/api/log/DeleteLog")
async def log_delete_log(logid: int, userid: int):
    response = mysql.delete_log(logid)
    if response["status"] == 0:
        mysql.create_log(userid, "删除日志 {" + str(logid) + "}", "成功")
    else:
        mysql.create_log(
            userid,
            "删除日志 {" + str(logid) + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response