import os
from elasticsearch import Elasticsearch
from db.Mysql.MysqlApi import MysqlApi
import pandas as pd
from pydantic import BaseModel


class Knowledge(BaseModel):
    title: str
    info: str


class ESApi(object):
    def __init__(self, user:str, password:str):
        self.es = Elasticsearch("http://127.0.0.1:9200", basic_auth=(user, password))

    def create_index(self, index_name):
        index_body = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "ik_max_word",  # 使用ik分词器进行分词处理
                        "search_analyzer": "ik_smart"
                    },
                    "info": {
                        "type": "text",
                        "analyzer": "ik_max_word",  # 使用ik分词器进行分词处理
                        "search_analyzer": "ik_smart"
                    }
                }
            }
        }
        self.es.indices.create(index=index_name, body=index_body)
        print(f"Index '{index_name}' created successfully.")

    # 创建索引，并插入mysql
    def create_index_mysql(self, kbname, info, userid):
        mysql = MysqlApi("localhost", "root", "123456", "QADB", 3306)
        response = mysql.create_indices(kbname=kbname, info=info, userid=userid)
        index_name = response["kblist"]["indices"]
        self.create_index(index_name)
        return response

    # 离线上传txt文档
    def load_es_offline_txt(self, index_name: str, userid, folder_path: str):
        mysql = MysqlApi()
        data = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):  # 确保只处理文本文件
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    for line in lines:
                        title = ""
                        info = ""
                        for item in line.split():
                            if item.startswith("title:"):
                                title = item[6:]
                                info += item + " "
                                info = info.replace("title", "标题")
                            elif item.startswith("rating:") or item.startswith("writer:") or item.startswith(
                                    "translator:") or item.startswith("pub_info:") or item.startswith(
                                "ISBN:") or item.startswith(
                                "series:") or item.startswith("tags:"):
                                info += item + " "
                                info = info.replace("rating", "评分")
                                info = info.replace("writer", "作者")
                                info = info.replace("translator", "译者")
                                info = info.replace("pub_info", "出版信息")
                                info = info.replace("series", "系列")
                                info = info.replace("tags", "标签")
                        data.append({"title": title, "info": info.strip()})
        docs = data
        for doc in docs:
            # 插入mysql数据库
            response = mysql.create_knowledge(
                indices=index_name, title=doc["title"], info=doc["info"], userid=userid, istrain='true'
            )
            # 插入es数据库
            self.es.index(index=index_name, document=doc, id=response["knowledge"]["knowledgeid"])

    # 离线上传csv文档
    def load_es_offline_csv(self, index_name: str, userid, folder_path: str):
        mysql = MysqlApi()
        docs = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):  # 确保只处理csv文件
                file_path = os.path.join(folder_path, filename)
                # 读取csv文件
                df = pd.read_csv(file_path)
                # 将每行数据转换为字典，添加到docs列表中
                docs = df.to_dict(orient="records")

        for doc in docs:
            doc["title"] = doc.pop("title")
            doc["info"] = doc.pop("reply")
            # 插入mysql数据库
            response = mysql.create_knowledge(index_name, title=doc["title"], info=doc["info"], userid=userid, istrain='true')
            # 插入es数据库
            self.es.index(index=index_name, document=doc, id=response["knowledge"]["knowledgeid"])

    def search_es(self, index_name: str, query: str):
        # 构建查询语句
        array = []
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "info"]
                }
            },
            "size": 5
        }

        # 执行查询
        results = self.es.search(index=index_name, body=body)
        for hit in results["hits"]["hits"]:
            array.append({"title": hit["_source"]["title"], "info": hit["_source"]["info"]})

        # 返回结果

        return array

        # print("Search results:")
        # for hit in results["hits"]["hits"]:
        #     print("Title:", hit["_source"]["title"])
        #     print("Info:", hit["_source"]["info"])
        #     print()

    # 删除索引
    def delete_index(self, index_name):
        self.es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")

    # 在线添加文档
    def add_document(self, index_name, doc, doc_id):
        try:
            response = self.es.index(index=index_name, body=doc, id=doc_id)
            print(f"文档添加成功：{response}")
            return True
        except Exception as e:
            print(f"添加文档时出现错误：{e}")
            return False

    # 修改文档
    def update_document(self, index_name, doc, doc_id):
        try:
            response = self.es.update(index=index_name, body={"doc": doc}, id=doc_id)
            print(f"文档更新成功：{response}")
        except Exception as e:
            print(f"更新文档时出现错误：{e}")

    # 删除文档
    def delete_document(self, index_name, doc_id):
        try:
            response = self.es.delete(index=index_name, id=doc_id)
            print(f"文档删除成功：{response}")
        except Exception as e:
            print(f"删除文档时出现错误：{e}")

if __name__ == "__main__":
    es = ESApi("elastic", "9YfcLUcxKiDvtzef1piK")
    # 测试连接
    if es.es.ping():
        print("Elasticsearch连接成功")
    else:
        print("Elasticsearch连接失败")
    # 创建索引
    index_name = "book"
    es.create_index(index_name)
    # 上传文档
    folder_path = ".../data/books"
    index_name = "book"
    es.load_es_offline(index_name, folder_path)
