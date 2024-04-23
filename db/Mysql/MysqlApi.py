import pymysql
from markdown import markdown
import string
import random
import datetime
from pydantic import BaseModel


class Knowledge(BaseModel):
    title: str
    info: str


# 将mysql中的messages转换为markdown格式
def trans(messages):
    res = []
    for message in messages:
        content_index = message.find("content=")
        # 获取角色 从第6个字符开始到content_index-1
        role = message[6 : content_index - 1].strip("'")
        content = message[content_index + len("content=") :].strip("'")

        # 将content转换为markdown格式
        content = content.replace("\\n", "\n")
        content = markdown(content)

        # 初始化空字典
        data_dict = {}
        # 添加键值对
        data_dict["role"] = role
        data_dict["content"] = content

        # 将字典添加到列表中
        res.append(data_dict)
    return res


# 生成随机字符串
def generate_random_string(length=10):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class MysqlApi:
    def __init__(self, host, user, password, database, port):
        # 连接数据库
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    """数据总览操作"""
    # 获取数据总览
    def get_overview(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            cursor = db_connection.cursor()
            # 鉴权
            cursor.execute("SELECT UserRole FROM Users WHERE UserID = %s", (userid))
            userrole = cursor.fetchone()[0]

            # 查询知识库总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM KnowledgeBases")
                kb_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM KnowledgeBases WHERE DATE(Timestamp) = CURDATE()"
                )
                kb_current = cursor.fetchone()[0]
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM KnowledgeBases WHERE UserID = %s", (userid)
                )
                kb_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM KnowledgeBases WHERE UserID = %s AND DATE(Timestamp) = CURDATE()",
                    (userid),
                )
                kb_current = cursor.fetchone()[0]
            # 查询知识总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM Knowledge")
                knowledge_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Knowledge WHERE DATE(Timestamp) = CURDATE()"
                )
                knowledge_current = cursor.fetchone()[0]
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM Knowledge WHERE UserID = %s", (userid)
                )
                knowledge_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Knowledge WHERE UserID = %s AND DATE(Timestamp) = CURDATE()",
                    (userid),
                )
                knowledge_current = cursor.fetchone()[0]
            # 查询对话总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM Conversations")
                conversation_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Conversations WHERE DATE(Timestamp) = CURDATE()"
                )
                conversation_current = cursor.fetchone()[0]
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM Conversations WHERE UserID = %s", (userid)
                )
                conversation_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Conversations WHERE UserID = %s AND DATE(Timestamp) = CURDATE()",
                    (userid),
                )
                conversation_current = cursor.fetchone()[0]
            # 查询模型总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM Models")
                model_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Models WHERE Status = '训练中'"
                )
                model_current = cursor.fetchone()[0]
            else:
                model_total = 0
                model_current = 0
            # 查询日志总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM Logs")
                log_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Logs WHERE Status != '成功'"
                )
                log_current = cursor.fetchone()[0]
            else:
                log_total = 0
                log_current = 0
            # 查询用户总数
            if userrole == "admin":
                cursor.execute("SELECT COUNT(*) FROM Users")
                user_total = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM Users WHERE DATE(Timestamp) = CURDATE()"
                )
                user_current = cursor.fetchone()[0]
            else:
                user_total = 0
                user_current = 0
            dataOverview = {
                "KB": {"total": kb_total, "current": kb_current},
                "Knowledge": {"total": knowledge_total, "current": knowledge_current},
                "Conversation": {"total": conversation_total, "current": conversation_current},
                "Model": {"total": model_total, "current": model_current},
                "Log": {"total": log_total, "current": log_current},
                "User": {"total": user_total, "current": user_current},
            }
            return {"status": 0, "dataOverview": dataOverview}

        except pymysql.Error as err:
            print("数据库错误：", err)
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()

    # 获取服务访问量
    def get_views(self):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            cursor = db_connection.cursor()
            # 查询服务访问量
            # 初始化每小时日志数量列表
            logs_count_by_hour = [0] * 24

            # 执行查询每小时日志数量的 SQL 查询语句
            cursor.execute("""
                SELECT HOUR(Timestamp) AS HourOfDay, COUNT(*) AS LogCount
                FROM Logs
                WHERE DATE(Timestamp) = CURDATE()
                GROUP BY HOUR(Timestamp)
            """)
            logs_by_hour = cursor.fetchall()

            # 更新每小时日志数量列表
            for hour, count in logs_by_hour:
                logs_count_by_hour[hour] = count
            return {"status": 0, "views": logs_count_by_hour}

        except pymysql.Error as err:
            print("数据库错误：", err)
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()

    """日志操作"""
    # 创建日志
    def create_log(self, userid, logcontent, status):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询用户名
            cursor.execute("SELECT UserName FROM Users WHERE UserID = %s", (userid))
            username = cursor.fetchone()[0]

            # 插入日志数据
            cursor.execute(
                "INSERT INTO Logs (UserID, UserName, LogContent, Status) VALUES (%s, %s, %s, %s)",
                (userid, username, logcontent, status),
            )
            # 提交事务
            db_connection.commit()
            print("日志插入成功！")
            return {"status": 0, "message": "日志插入成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除日志
    def delete_log(self, logid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()

            # 删除日志数据
            cursor.execute("DELETE FROM Logs WHERE LogID = %s", (logid))
            # 提交事务
            db_connection.commit()
            print("日志删除成功！")
            return {"status": 0, "message": "日志删除成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取日志列表
    def get_logList(self, pagenum, pagesize):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()

            # 查询日志数据
            cursor.execute("SELECT COUNT(*) AS total_count FROM Logs",)
            total_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT LogID, UserID, UserName, LogContent, Status, DATE_FORMAT(Timestamp, '%%Y-%%m-%%d %%H:%%i:%%S') FROM Logs ORDER BY Timestamp DESC LIMIT %s, %s",
                ((pagenum - 1) * pagesize, pagesize),
            )
            # 获取查询结果
            loglist = []
            results = cursor.fetchall()
            for result in results:
                loglist.append(
                    {
                        "logid": result[0],
                        "userid": result[1],
                        "username": result[2],
                        "logcontent": result[3],
                        "status": result[4],
                        "timestamp": result[5],
                    }
                )
            return {"status": 0, "logs": loglist, "total": total_count}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "loglist": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """用户操作"""
    # 创建用户
    def create_user(self, username, password):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 插入用户数据
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (%s, %s)",
                   (username, password))
            # 提交事务
            db_connection.commit()
            # 获取token
            cursor.execute("SELECT * FROM Users WHERE Username = %s", (username))
            result = cursor.fetchone()
            print("数据插入成功！")
            return {"status": 0, "message": "注册成功！","token": {"id": result[0], "role": result[3]}}

        except pymysql.Error as err:
            print("数据库错误：", err.args[0], err.args[1])
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1], "token": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取用户名
    def get_username(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            cursor = db_connection.cursor()
            # 查询用户名
            cursor.execute("SELECT Username FROM Users WHERE UserID = %s", (userid))
            username = cursor.fetchone()[0]
            return username

        except pymysql.Error as err:
            print("数据库错误：", err)
            return {"status": err.args[0], "username": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()

    # 获取用户
    def get_user(self, username):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询用户数据
            cursor.execute("SELECT * FROM Users WHERE Username = %s", (username))
            # 获取查询结果
            result = cursor.fetchone()
            return result

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 验证用户
    def validate_user(self, username, password):
        result = self.get_user(username)
        if result is None:
            return {"status": 1, "message": "用户不存在！","token": None}
        if result[2] == password:
            return {"status": 0, "message": "登录成功！","token": {"id": result[0], "role": result[3]}}
        else:
            return {"status": 1, "message": "用户名或密码错误！","id": result[0]}

    # 删除用户
    def delete_user(self, username, password):
        try:
            # 验证用户
            if self.validate_user(username, password).status == 1:
                return {"status": 1, "message": "用户名或密码错误！","token": None}
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 删除用户数据
            cursor.execute("DELETE FROM Users WHERE Username = %s", (username))
            # 提交事务
            db_connection.commit()
            print("数据删除成功！")
            return {"status": 0, "message": "删除成功！","token": None}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1], "token": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 更新用户密码
    def edit_password(self, username, password, newpassword):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询用户原密码
            cursor.execute("SELECT Password FROM Users WHERE Username = %s", (username))
            if cursor.fetchone()[0] != password:
                return {"status": 1, "message": "原密码错误！"}
            # 更新用户数据
            cursor.execute("UPDATE Users SET Password = %s WHERE Username = %s", (newpassword, username))
            # 提交事务
            db_connection.commit()
            print("数据更新成功！")
            return {"status": 0, "message": "更新成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取用户信息
    def get_userInfo(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            cursor = db_connection.cursor()
            # 查询用户数据
            cursor.execute(
                "SELECT Username, NickName, Age, Sex, Email, Phone, Area, Job, DATE_FORMAT(Timestamp, '%%m-%%d') FROM Users WHERE UserID = %s",
                (userid),
            )
            # 获取查询结果
            result = cursor.fetchone()
            userinfo = {
                "username": result[0],
                "nickname": result[1],
                "age": result[2],
                "sex": result[3],
                "email": result[4],
                "phone": result[5],
                "area": result[6],
                "job": result[7],
                "createtime": result[8],
            }
            return {"status": 0, "userinfo": userinfo}

        except pymysql.Error as err:
            print("数据库错误：", err)
            return {"status": err.args[0], "userinfo": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()

    # 更新用户信息
    def edit_userInfo(self, user):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            cursor = db_connection.cursor()
            # 更新用户数据
            cursor.execute(
                "UPDATE Users SET Username=%s, NickName=%s, Age=%s, Sex=%s, Email=%s, Phone=%s, Area=%s, Job=%s WHERE UserID = %s",
                (
                    user.username,
                    user.nickname,
                    user.age,
                    user.sex,
                    user.email,
                    user.phone,
                    user.area,
                    user.job,
                    user.userid,
                ),
            )
            # 提交事务
            db_connection.commit()
            print("数据更新成功！")
            return {"status": 0, "message": "更新成功！"}
        except pymysql.Error as err:
            print("数据库错误：", err)
            return {"status": err.args[0], "message": err.args[1]}
        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """Session操作"""
    # 创建Session
    def create_session(self, userid, sessionname):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 插入Session数据
            cursor.execute("INSERT INTO Sessions (UserID, SessionName) VALUES (%s, %s)", (userid, sessionname))
            # 提交事务
            sessionid = cursor.lastrowid
            db_connection.commit()
            print("数据插入成功！")
            cursor.execute(
                "SELECT SessionID, DATE_FORMAT(CreateTime, '%%m-%%d'), SessionName FROM Sessions WHERE UserID = %s AND SessionID = %s",
                (userid, sessionid),
            )
            result = cursor.fetchone()
            session={
               "sessionid": result[0],
                "createtime": result[1],
                "sessionname": result[2],                
            }
            return {"status": 0, "message": "创建成功！", "session": session}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取SessionList
    def get_sessionList(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询Session数据
            cursor.execute(
                "SELECT SessionID, DATE_FORMAT(CreateTime, '%%m-%%d'), SessionName FROM Sessions WHERE UserID = %s",
                (userid),
            )
            # 获取查询结果
            sessions = []
            results = cursor.fetchall()
            for result in results:
                sessions.append({"sessionid": result[0], "createtime":result[1], "sessionname": result[2]})
            return {"status": 0, "sessions": sessions}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message":err.args[1], "sessions": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除Session
    def delete_session(self, sessionid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 删除对话记录表中与该会话相关的所有对话记录
            cursor.execute(f"DELETE FROM Conversations WHERE SessionID = %s", (sessionid))
            # 删除会话
            cursor.execute("DELETE FROM Sessions WHERE SessionID = %s", (sessionid))
            # 提交事务
            db_connection.commit()
            print("数据删除成功！")
            return {"status": 0, "message": "删除成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 更新Session
    def update_session(self, sessionid, newname):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 更新Session数据
            cursor.execute("UPDATE Sessions SET SessionName = %s WHERE SessionName = %s", (newname, sessionid))
            # 提交事务
            db_connection.commit()
            print("数据更新成功！")
            return {"status": 0, "message": "更新成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """Conversation操作"""
    # 创建Conversation
    def create_conversation(self, sessionid, messages):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询用户ID
            cursor.execute("SELECT UserID FROM Sessions WHERE SessionID = %s", (sessionid))
            userid = cursor.fetchone()[0]
            # 插入Conversation数据
            for message in messages:
                cursor.execute("INSERT INTO Conversations (SessionID, Message, UserID) VALUES (%s, %s, %s)", (sessionid, message, userid))
            # 提交事务
            db_connection.commit()
            print("对话插入成功！")

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取Conversation
    def get_conversation(self, sessionid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询Conversation数据
            cursor.execute("SELECT * FROM Conversations WHERE SessionID = %s ORDER BY Timestamp ASC", (sessionid))
            # 获取查询结果
            messages = []
            results = cursor.fetchall()
            for result in results:
                messages.append(result[3])
            messages = trans(messages)
            print(messages)
            return {"status": 0, "messages": messages}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """知识库操作"""
    # 新建知识库
    def create_indices(self, kbname, info, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取索引名
            indices = generate_random_string()
            # 插入索引数据
            cursor.execute(
                "INSERT INTO KnowledgeBases (KBName, Info, Indices, UserID, DataCount) VALUES (%s, %s, %s, %s, %s)",
                (kbname, info, indices, userid, 0),
            )
            # 提交事务
            db_connection.commit()
            kbid = cursor.lastrowid
            print("知识库创建成功！")
            kblist = {
                "kbid": kbid,
                "kbname": kbname,
                "info": info,
                "indices": indices,
                "datacount": 0,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            return {"status": 0, "message": "创建成功！", "kblist": kblist}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 编辑知识库
    def edit_kb(self, kbid, kbname, info):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 更新知识库数据
            cursor.execute("UPDATE KnowledgeBases SET KBName = %s, Info = %s WHERE KBID = %s", (kbname, info, kbid))
            # 提交事务
            db_connection.commit()
            # 更新知识条目数据
            cursor.execute(
                "UPDATE Knowledge SET KBName = %s WHERE KBID = %s",
                (kbname, kbid),
            )
            # 提交事务
            db_connection.commit()
            print("知识库编辑成功！")
            return {"status": 0, "message": "编辑成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除知识库
    def delete_kb(self, indices):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取知识库名字
            cursor.execute(
                "SELECT KBName FROM KnowledgeBases WHERE Indices = %s", (indices)
            )
            kbname = cursor.fetchone()[0]
            # 删除知识库数据
            cursor.execute(
                "Delete FROM Knowledge WHERE Indices = %s", (indices)
            )
            # 提交事务
            db_connection.commit()
            # 删除知识库
            cursor.execute(
                "Delete FROM KnowledgeBases WHERE Indices = %s", (indices)
            )
            db_connection.commit()
            print("知识库删除成功！")
            return {"status": 0, "message": "删除成功！", "kbname": kbname}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获得知识库列表
    def get_kbList(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 用户鉴权
            cursor.execute(
                "SELECT * FROM Users WHERE UserID = %s",
                (userid),
            )
            result = cursor.fetchone()
            userrole = result[3]
            id = ''
            # 查询知识库数据
            if(userrole == 'admin'):
                cursor.execute(
                    "SELECT KBID, KBName, Info, Indices, DataCount, DATE_FORMAT(Timestamp, '%Y-%m-%d %H:%i:%S'), UserID FROM KnowledgeBases"
                )
            else:
                cursor.execute(
                    "SELECT KBID, KBName, Info, Indices, DataCount, DATE_FORMAT(Timestamp, '%%Y-%%m-%%d %%H:%%i:%%S'), UserID FROM KnowledgeBases WHERE UserID = %s",
                    (userid,),
                )
            # 获取查询结果
            kblist = []
            results = cursor.fetchall()
            for result in results:
                # 查询拥有者名字
                cursor.execute(
                    "SELECT * FROM Users WHERE UserID = %s",
                    (result[6]),
                )
                result2 = cursor.fetchone()
                username = result2[1]
                kblist.append(
                    {
                        "kbid": result[0],
                        "kbname": result[1],
                        "info": result[2],
                        "indices": result[3],
                        "datacount": result[4],
                        "timestamp": result[5],
                        "username": username,
                    }
                )
            return {"status": 0, "kblist": kblist}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "kblist": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取ES的索引名
    def get_indices(self, id, flag):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            if flag==0: # flag=0表示知识库
                cursor.execute("SELECT Indices FROM KnowledgeBases WHERE KBID = %s", (id))
            else: # flag=1表示知识
                cursor.execute("SELECT Indices FROM Knowledge WHERE KnowledgeID = %s", (id))
            result = cursor.fetchone()
            return result[0]

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """知识操作"""
    # 新建知识条目
    def create_knowledge(self, indices, title, info, userid, istrain='false'):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取知识库ID和知识数目
            cursor.execute("SELECT KBID, KBName, DataCount FROM KnowledgeBases WHERE Indices = %s", (indices))
            result = cursor.fetchone()
            count = result[2]
            # 插入知识数据
            count = count+1
            cursor.execute(
                "INSERT INTO Knowledge (Title, Info, IsTrain, KBID, KBName, Indices, UserID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, info, istrain, result[0], result[1], indices, userid),
            )
            # 提交事务
            db_connection.commit()
            # 查询新建知识数据
            id = cursor.lastrowid

            # 更新知识库的条目
            cursor.execute(
                "UPDATE KnowledgeBases SET DataCount = %s WHERE Indices = %s", (count, indices)
            )
            # 提交事务
            db_connection.commit()

            cursor.execute(
                "SELECT KnowledgeID, Title, Info, KBID, KBName, Indices, DATE_FORMAT(Timestamp, '%%Y-%%m-%%d %%H:%%i:%%S'), IsTrain FROM Knowledge WHERE KnowledgeID = %s",
                (id),
            )
            # 获取查询结果
            result = cursor.fetchone()
            knowledge = {
                "knowledgeid": result[0],
                "title": result[1],
                "info": result[2],
                "kbid": result[3],
                "kbname": result[4],
                "indices": result[5],
                "timestamp": result[6],
                "istrain": result[7],
            }
            print("知识创建成功！")
            return {"status": 0, "message": "知识创建成功！", "knowledge": knowledge}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 编辑知识条目
    def edit_knowledge(self, knowledgeid, title, info, istrain):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            cursor.execute("UPDATE Knowledge SET Title = %s, Info = %s, IsTrain = %s WHERE KnowledgeID = %s",
                   (title, info, istrain, knowledgeid))
            db_connection.commit()
            print("知识编辑成功！")
            return {"status": 0, "message": "知识编辑成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除知识条目
    def delete_knowledge(self, index_name, knowledgeid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取知识标题
            cursor.execute("SELECT Title FROM Knowledge WHERE KnowledgeID = %s", (knowledgeid))
            title = cursor.fetchone()[0]
            # 删除知识数据
            cursor.execute("DELETE FROM Knowledge WHERE KnowledgeID = %s", (knowledgeid))
            db_connection.commit()
            # 减少知识库的知识数量
            cursor.execute(
                "SELECT DataCount FROM KnowledgeBases WHERE Indices = %s",
                (index_name),
            )
            count = cursor.fetchone()[0]
            # 更新数量
            count = count - 1
            cursor.execute(
                "UPDATE KnowledgeBases SET DataCount = %s WHERE Indices = %s",
                (count, index_name),
            )
            # 提交事务
            db_connection.commit()
            print("知识删除成功！")
            return {"status": 0, "message": "知识删除成功！", "title": title}

        except pymysql.Error as err:
            print("数据库错误：", err)
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取知识列表
    def get_knowledgeList(self, pagenum, pagesize, kbid, title, userid, istrain):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 对用户进行鉴权
            cursor.execute(
                "SELECT UserRole FROM Users WHERE UserID = %s",
                (userid),
            )
            userrole = cursor.fetchone()[0]
            # 查询知识数据
            query = "SELECT KnowledgeID, Title, Info, KBID, KBName, Indices, DATE_FORMAT(Timestamp, '%%Y-%%m-%%d %%H:%%i:%%S'), IsTrain FROM Knowledge WHERE 1=1"
            query2 = "SELECT COUNT(*) AS total_count FROM Knowledge WHERE 1=1"
            params = []
            if kbid is not None:
                query += " AND KBID = %s"
                query2 += " AND KBID = %s"
                params.append(kbid)
            if title is not None:
                query += " AND Title LIKE %s"
                query2 += " AND Title LIKE %s"
                params.append(f"%{title}%")
            if userrole != 'admin':
                query += " AND UserID = %s"
                query2 += " AND UserID = %s"
                params.append(userid)
            if istrain != '':
                query += " AND IsTrain = %s"
                query2 += " AND IsTrain = %s"
                params.append(istrain)

            # 执行总数查询
            cursor.execute(query2, tuple(params))
            # 获取查询结果
            total_count = cursor.fetchone()[0]

            # 设置排序
            query += " ORDER BY Timestamp DESC"
            # 分页
            query += " LIMIT %s, %s"
            params.append((pagenum - 1) * pagesize)
            params.append(pagesize)
            # 执行原始查询
            cursor.execute(query, tuple(params))
            # 获取查询结果
            knowledgelist = []
            results = cursor.fetchall()
            for result in results:
                knowledgelist.append(
                    {
                        "knowledgeid": result[0],
                        "title": result[1],
                        "info": result[2],
                        "kbid": result[3],
                        "kbname": result[4],
                        "indices": result[5],
                        "timestamp": result[6],
                        "istrain": result[7],
                    }
                )
            return {"status": 0, "knowledgelist": knowledgelist, "total": total_count}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "knowledgelist": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    """模型操作"""
    # 获取模型列表
    def get_modelList(self, userid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 查询模型数据
            cursor.execute(
                "SELECT ModelID, ModelName, Info, status, DATE_FORMAT(Timestamp, '%%Y-%%m-%%d %%H:%%i:%%S'), UserID, UserName FROM Models WHERE UserID = %s",
                (userid),
            )
            # 获取查询结果
            modellist = []
            results = cursor.fetchall()
            for result in results:
                modellist.append(
                    {
                        "modelid": result[0],
                        "modelname": result[1],
                        "info": result[2],
                        "status": result[3],
                        "timestamp": result[4],
                        "userid": result[5],
                        "username": result[6],
                    }
                )
            return {"status": 0, "modellist": modellist}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], 'message':'获取模型列表失败', "modellist": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 创建模型
    def create_model(self, modelname, info, userid, status="训练中"):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取用户名
            cursor.execute("SELECT Username FROM Users WHERE UserID = %s", (userid))
            username = cursor.fetchone()[0]
            # 插入模型数据
            cursor.execute("INSERT INTO Models (ModelName, Info, UserID, Status, UserName) VALUES (%s, %s, %s, %s, %s)",
                   (modelname, info, userid, status, username))
            # 提交事务
            db_connection.commit()
            print("新模型创建成功！")
            return {"status": 0, "message": "新模型创建成功、正在训练！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            # 回滚事务
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 编辑模型
    def edit_model(self, modelid, modelname, info, status):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            cursor.execute("UPDATE Models SET ModelName = %s, Info = %s, Status = %s WHERE ModelID = %s",
                   (modelname, info, status, modelid))
            db_connection.commit()
            print("模型编辑成功！")
            return {"status": 0, "message": "模型编辑成功！"}

        except pymysql.Error as err:
            print("数据库错误：", err)
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除模型
    def delete_model(self, modelid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            # 获取模型名
            cursor.execute("SELECT ModelName FROM Models WHERE ModelID = %s", (modelid))
            modelname = cursor.fetchone()[0]
            # 删除模型
            cursor.execute("DELETE FROM Models WHERE ModelID = %s", (modelid))
            db_connection.commit()
            print("模型删除成功！")
            return {"status": 0, "message": "模型删除成功！", "modelname": modelname}

        except pymysql.Error as err:
            print("数据库错误：", err)
            db_connection.rollback()
            return {"status": err.args[0], "message": err.args[1]}

        finally:
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 获取模型名称
    def get_modelname(self, modelid):
        try:
            # 获取游标
            db_connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            cursor = db_connection.cursor()
            cursor.execute("SELECT ModelName FROM Models WHERE ModelID = %s", (modelid))
            result = cursor.fetchone()
            return result[0]

        except pymysql.Error as err:
            print("数据库错误：", err)
            db_connection.rollback()

        finally:
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")


if __name__ == "__main__":
    mysql_api = MysqlApi()
    mysql_api.create_user("Alice", "12345")
    #response = mysql_api.get_user("Alice")
    #print(response[2])
