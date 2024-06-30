import time
import random
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Optional
import pandas as pd

from config.data_classes import *
from chat.ChatApi import ChatApi

from db.ES.ESApi import ESApi
from db.Mysql.MysqlApi import MysqlApi

from RecommendModel.RecommendModelApi import RecommendModelApi

from config.config import Config


questions = []


app = FastAPI()
config_path = "./config.yaml"
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


# 初始化服务
def init():
    config = Config("./config.yaml")
    # 初始化数据库
    mysqlconfig = config.config['mysql']
    mysql = MysqlApi(mysqlconfig["host"], mysqlconfig["user"], mysqlconfig["password"], mysqlconfig["database"], mysqlconfig["port"])

    # 初始化ES
    esconfig = config.config['es']
    es = ESApi(esconfig['user'], esconfig['password'])

    # 初始化大模型对话服务
    chatconfig = config.config['llm']
    chat = ChatApi(chatconfig['appid'], chatconfig['api_secret'], chatconfig['api_key'], chatconfig['Spark_url'], chatconfig['domain'])

    # 初始化推荐模型
    recommendModelconfig = config.config['recommendModel']
    recommendModel = RecommendModelApi(recommendModelconfig['base_path'])
    recommendModel.load_model(recommendModelconfig['model_name'])
    return mysql, es, chat, recommendModel

mysql, es, chat, recommendModel = init()


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
    if response["status"] == 0:
        mysql.create_log(
            response["token"]["id"],
            "创建用户 {" + str(response["token"]["id"]) + "}",
            "成功",
        )
    return response
# 登陆接口
@app.post("/api/login")
async def register(UserRegistration: User):
    logger.info(UserRegistration)
    # 执行登陆用户的逻辑
    response = mysql.validate_user(UserRegistration.Username, UserRegistration.Password)
    if response["status"] == 0:
        mysql.create_log(
            response["token"]["id"],
            "登陆系统",
            "成功",
        )
    else:
        mysql.create_log(
            response["id"],
            "登陆系统",
            "操作失败，" + "原因：" + response["message"],
        )
    return response


# 修改密码接口
@app.get("/api/user/EditPassword")
async def user_edit_password(username: str, oldpassword: str, newpassword: str):
    userid = mysql.get_userid(username)
    response = mysql.edit_password(username, oldpassword, newpassword)
    if response["status"] == 0:
        mysql.create_log(
            userid,
            "修改密码",
            "成功",
        )
    else:
        mysql.create_log(
            userid,
            "修改密码",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 获取用户列表接口
@app.get("/api/user/GetUserList")
async def user_get_userlist(pagenum: int, pagesize: int):
    response = mysql.get_userList(pagenum, pagesize)
    return response

# 新增用户接口
@app.post("/api/user/CreateUser")
async def user_create_user(user: User):
    response = mysql.add_user(user.Username, user.Password, user.Role)
    if response["status"] == 0:
        mysql.create_log(
            1,
            "创建用户 {" + user.Username + "}",
            "成功",
        )
    else:
        mysql.create_log(
            1,
            "创建用户 {" + user.Username + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 删除用户接口
@app.get("/api/user/DeleteUser")
async def user_delete_user(userid: int):
    response = mysql.delete_user(userid)
    if response["status"] == 0:
        mysql.create_log(
            1,
            "删除用户 {" + str(userid) + "}",
            "成功",
        )
    else:
        mysql.create_log(
            1,
            "删除用户 {" + str(userid) + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 编辑用户信息接口
@app.post("/api/user/EditUser")
async def user_edit_user(user: User):
    response = mysql.edit_user(user.UserID, user.Username, user.Password, user.Role)
    if response["status"] == 0:
        mysql.create_log(
            1,
            "编辑用户 {" + str(user.Username) + "}",
            "成功",
        )
    else:
        mysql.create_log(
            1,
            "编辑用户 {" + str(user.Username) + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 获取用户信息接口
@app.get("/api/user/GetUserInfo")
async def user_get_userinfo(userid: int):
    response = mysql.get_userInfo(userid)
    return response

# 编辑用户信息接口
@app.post("/api/user/EditUserInfo")
async def user_edit_userinfo(user: UserInfo):
    response = mysql.edit_userInfo(user)
    if response["status"] == 0:
        mysql.create_log(
            user.userid,
            "编辑用户信息",
            "成功",
        )
    else:
        mysql.create_log(
            user.id,
            "编辑用户信息",
            "操作失败，" + "原因：" + response["message"],
        )
    return response


"""数据总览接口"""
# 获得数据总览
@app.get("/api/data/GetDataOverview")
async def data_get_overview(userid: int):
    response = mysql.get_overview(userid)
    return response

# 获得服务访问量
@app.get("/api/data/GetDataViews")
async def data_get_views():
    response = mysql.get_views()
    return response

"""Chat对话接口"""
# 获得历史对话
@app.get("/api/chat/GetConversationHistory")
async def chat_get_messages(sessionId: int, userId: int):
    response = mysql.get_conversation(sessionId)
    if response["status"] == 0:
        mysql.create_log(
            userId,
            "获取会话 {" + str(sessionId) + "} 历史记录",
            "成功",
        )
    else:
        mysql.create_log(
            userId,
            "获取会话 {" + str(sessionId) + "} 历史记录",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 获得对话回答
@app.post("/api/chat/GetChatAnswer")
async def chat_get_messages(session: Session):
    content = chat.get_chat_response(session.question, "202mp6w1r6")
    messages = []
    messages.append(Message(role="robot", content=content))
    mysql.create_conversation(session.sessionId, [Message(role='user', content=session.question),
                                                  Message(role='robot', content=content)])
    mysql.create_log(session.userId, "提问 {" + session.question + "}", "成功")
    return ChatResponse(status=0,messages=messages)

# 获得推荐问题序列
@app.get("/api/chat/GetRecommendQuestions")
async def chat_get_recommend_questions(userId: int, flag:bool, question: Optional[str] = None):
    global questions
    if not flag:
        if question == None:
            # 读取CSV数据集
            df = pd.read_csv('./data/law/law1.csv')  # 替换为你的数据集文件路径
            # 获取问题title列
            questions = df['title'].sample(n=20).tolist()
        else:
            questions = await recommendModel.recommend_similar_questions(question)
    recommend_questions = random.sample(questions, 5)
    return {"status": 0, "message": "获取推荐问题成功", "questions": recommend_questions}

"""Session接口"""
# 获得Session列表
@app.get("/api/session/GetSessionList")
async def session_get_sessionlist(userid: int):
    response = mysql.get_sessionList(userid)
    if response["status"] == 0:
        mysql.create_log(
            userid,
            "获取历史会话",
            "成功",
        )
    else:
        mysql.create_log(
            userid,
            "获取历史会话",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 创建Session
@app.post("/api/session/CreateSession")
async def session_create_session(session: CreateSession):
    response = mysql.create_session(session.userId, session.sessionname)
    mysql.create_conversation(
        response['session']['sessionid'],
        [Message(role="robot", content="你好，我是机器人小助手，有什么可以帮助你的吗？")],
    )
    if response["status"] == 0:
        mysql.create_log(
            session.userId,
            "创建会话 {" + session.sessionname + "}",
            "成功",
        )
    else:
        mysql.create_log(
            session.userId,
            "创建会话 {" + session.sessionname + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 删除Session
@app.post("/api/session/DeleteSession")
async def session_delete_session(session: DeleteSession):
    response = mysql.delete_session(session.sessionId)
    if response["status"] == 0:
        mysql.create_log(
            session.userId,
            "删除会话 {" + str(session.sessionId) + "}",
            "成功",
        )
    else:
        mysql.create_log(
            session.userId,
            "删除会话 {" + str(session.sessionId) + "}",
            "操作失败，" + "原因：" + response["message"],
        )
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
    if response["status"] == 0:
        mysql.create_log(
            createKnowledgeBase.userId,
            "创建知识库 {" + createKnowledgeBase.kbname + "}",
            "成功",
        )
    else:
        mysql.create_log(
            createKnowledgeBase.userId,
            "创建知识库 {" + createKnowledgeBase.kbname + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 编辑知识库
@app.post("/api/knowledgebase/EditKB")
async def knowledgebase_edit_kb(knowledgeBase: KnowledgeBase):
    response = mysql.edit_kb(knowledgeBase.kbId, knowledgeBase.kbname, knowledgeBase.info)
    if response["status"] == 0:
        mysql.create_log(
            knowledgeBase.userId,
            "编辑知识库 {" + knowledgeBase.kbname + "}",
            "成功",
        )
    else:
        mysql.create_log(
            knowledgeBase.userId,
            "编辑知识库 {" + knowledgeBase.kbname + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 删除知识库
@app.get("/api/knowledgebase/DeleteKB")
async def knowledgebase_delete_kb(indices: str, userId: int):
    es.delete_index(indices)
    response = mysql.delete_kb(indices)
    if response["status"] == 0:
        mysql.create_log(
            userId,
            "删除知识库 {" + response["kbname"] + "}",
            "成功",
        )
    else:
        mysql.create_log(
            userId,
            "删除知识库 {" + response["kbname"] + "}",
            "操作失败，" + "原因：" + response["message"],
        )
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
    if response["status"] == 0:
        mysql.create_log(
            knowledge.userid,
            "创建知识 {" + knowledge.title + "}",
            "成功",
        )
    else:
        mysql.create_log(
            knowledge.userid,
            "创建知识 {" + knowledge.title + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 编辑知识
@app.post("/api/knowledge/EditKnowledge")
async def knowledge_edit_knowledge(knowledge: EditKnowledge):
    index_name = mysql.get_indices(knowledge.knowledgeid, 1)
    es.update_document(index_name, {"title": knowledge.title, "info": knowledge.info}, knowledge.knowledgeid)
    response = mysql.edit_knowledge(knowledge.knowledgeid, knowledge.title, knowledge.info, knowledge.istrain)
    if response["status"] == 0:
        mysql.create_log(
            knowledge.userid,
            "编辑知识 {" + knowledge.title + "}",
            "成功",
        )
    else:
        mysql.create_log(
            knowledge.userid,
            "编辑知识 {" + knowledge.title + "}",
            "操作失败，" + "原因：" + response["message"],
        )
    return response

# 删除知识
@app.get("/api/knowledge/DeleteKnowledge")
async def knowledge_delete_knowledge(knowledgeid: int, userid: int):
    index_name = mysql.get_indices(knowledgeid, 1)
    es.delete_document(index_name, knowledgeid)
    response = mysql.delete_knowledge(index_name, knowledgeid)
    if response["status"] == 0:
        mysql.create_log(
            userid,
            "删除知识 {" + response["title"] + "}",
            "成功",
        )
    else:
        mysql.create_log(
            userid,
            "删除知识 {" + response["title"] + "}",
            "操作失败，" + "原因：" + response["message"],
        )
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

# 测试模型
@app.get("/api/model/TestModel")
async def model_test_model(modelid: int, question: str, userid: int):
    # 获得模型名称
    modelname = mysql.get_modelname(modelid)
    questionList = await recommendModel.recommend_similar_questions(question, model_name=modelname)
    
    return {"status": 0, "message": "测试成功", "questionList": questionList}


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


"""系统设置接口"""
# 获得系统设置数据
@app.get("/api/setting/GetSettings")
async def setting_get_settings():
    config = Config(config_path)
    settings = config.config
    return {"status": 0, "message": "获取系统设置成功", "settings": settings}

# 编辑系统设置
@app.post("/api/setting/EditSettings")
async def setting_edit_settings(settings: Settings):
    global mysql, es, chat, recommendModel
    settings = settings.data
    print(settings)
    config = Config(config_path)
    global mysql, es, chat, recommendModel
    if settings['recommendModel']['model_id'] != config.config['recommendModel']['model_id']:
        model_name = mysql.get_modelname(settings['recommendModel']['model_id'])
        settings['recommendModel']['model_name'] = model_name
    config.edit_config(settings)
    # mysql, es, chat, recommendModel = init()
    return {"status": 0, "message": "修改系统设置成功，重启生效"}
