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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL,
            NickName TEXT,
            Sex TEXT,
            Email TEXT,
            Phone TEXT,
            Area TEXT,
            Job TEXT,
            Age INT,
            UserRole ENUM('user', 'admin') DEFAULT 'user',
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (Username)
        )
    """
    )

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
            UserID INT NOT NULL,
            FOREIGN KEY (SessionID) REFERENCES Sessions(SessionID)
        )
    """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS KnowledgeBases (
            KBID INT AUTO_INCREMENT PRIMARY KEY,
            KBName VARCHAR(255) NOT NULL,
            Info TEXT,
            Indices VARCHAR(10) NOT NULL,
            UserID INT NOT NULL,
            DataCount INT NOT NULL,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            UNIQUE (Indices)
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Knowledge (
            KnowledgeID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(255) NOT NULL,
            Info TEXT NOT NULL,
            IsTrain ENUM('true', 'false') DEFAULT 'false' NOT NULL,
            KBID INT NOT NULL,
            KBName VARCHAR(255) NOT NULL,
            Indices VARCHAR(10) NOT NULL,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UserID INT NOT NULL,
            FOREIGN KEY (KBID) REFERENCES KnowledgeBases(KBID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
    """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Models (
            ModelID INT AUTO_INCREMENT PRIMARY KEY,
            ModelName VARCHAR(255) UNIQUE NOT NULL,
            Info TEXT,
            Status TEXT NOT NULL,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UserID INT NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
    """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Logs (
            LogID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT NOT NULL,
            UserName VARCHAR(255) NOT NULL,
            LogContent TEXT NOT NULL,
            Status TEXT NOT NULL,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
    """
    )

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
