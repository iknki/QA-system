import pymysql

# 连接到 MySQL 数据库
db_connection = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    password="123456",  # 数据库密码
    port=3306  # 数据库端口
)

# 创建数据库
def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS QADB")

# 使用创建的数据库
def use_database(cursor):
    cursor.execute("USE QADB")

# 创建表格
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL,
            UNIQUE (Username)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sessions (
            SessionID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT NOT NULL,
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            SessionName VARCHAR(255),
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Conversations (
            ConversationID INT AUTO_INCREMENT PRIMARY KEY,
            SessionID INT NOT NULL,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Message TEXT NOT NULL,
            FOREIGN KEY (SessionID) REFERENCES Sessions(SessionID)
        )
    """)

try:
    # 获取游标
    cursor = db_connection.cursor()

    # 创建数据库
    create_database(cursor)

    # 使用创建的数据库
    use_database(cursor)

    # 创建表
    create_tables(cursor)

    print("数据库和表创建成功！")

except pymysql.Error as err:
    print("数据库错误：", err)

finally:
    # 关闭数据库连接
    if db_connection.open:
        cursor.close()
        db_connection.close()
        print("数据库连接已关闭。")
