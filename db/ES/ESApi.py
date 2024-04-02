import os
from elasticsearch import Elasticsearch


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

    def load_es_offline(self, index_name: str, folder_path: str):
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
            self.es.index(index=index_name, document=doc)

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






if __name__ == "__main__":
    es = ESApi("elastic", "w9nF5G7Pjt_lpVAcbqFy")
    # 测试连接
    if es.es.ping():
        print("Elasticsearch连接成功")
    else:
        print("Elasticsearch连接失败")
    index_name ="book"
    # 创建索引
    es.create_index(index_name)
    # 上传文档
    folder_path = ".../data/books"
    index_name = "book"
    es.load_es_offline(index_name, folder_path)

    


