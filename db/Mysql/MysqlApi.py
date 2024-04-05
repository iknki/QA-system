import pymysql
from markdown import markdown

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

class MysqlApi:
    def __init__(self):
        # 连接数据库
        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.database = "QADB"
        self.port = 3306

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
            return {"status": 0, "message": "注册成功！","token": result[0]}

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
            return {"status": 0, "message": "登录成功！","token": result[0]}
        else:
            return {"status": 1, "message": "用户名或密码错误！","token": None}

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
    def update_user(self, username, password, newpassword):
        try:
            # 验证用户
            validate = validate_user(username, password)
            if validate.status == 1:
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
            # 更新用户数据
            cursor.execute("UPDATE Users SET Password = %s WHERE Username = %s", (newpassword, username))
            # 提交事务
            db_connection.commit()
            print("数据更新成功！")
            return {"status": 0, "message": "更新成功！","token": validate.token}

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
            cursor.execute("SELECT * FROM Sessions WHERE UserID = %s AND SessionID = %s", (userid, sessionid))
            result = cursor.fetchone()
            session={
               "sessionid": result[0],
                "createtime": result[2],
                "sessionname": result[3],                
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
            return {"status": err.args[0], "sessions": None}

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")

    # 删除Session
    def delete_session(self, userid, sessionname):
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
            # 删除Session数据
            cursor.execute("DELETE FROM Sessions WHERE UserID = %s AND SessionName = %s", (userid, sessionname))
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
    def update_session(self, userid, sessionname, newname):
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
            cursor.execute("UPDATE Sessions SET SessionName = %s WHERE UserID = %s AND SessionName = %s", (newname, userid, sessionname))
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
            # message_str = json.dumps(message)
            # 插入Conversation数据
            for message in messages:
                cursor.execute("INSERT INTO Conversations (SessionID, Message) VALUES (%s, %s)", (sessionid, message))
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

        finally:
            # 关闭数据库连接
            if db_connection.open:
                cursor.close()
                db_connection.close()
                print("数据库连接已关闭。")


if __name__ == "__main__":
    mysql_api = MysqlApi()
    mysql_api.create_user("Alice", "12345")
    #response = mysql_api.get_user("Alice")
    #print(response[2])
