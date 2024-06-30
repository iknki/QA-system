from llmmodel import ModelApi as ModelApi
from llmmodel.Prompt import Prompt
from db.ES.ESApi import ESApi
from sparkai.core.messages import ChatMessage
import random

# 以下密钥信息从控制台获取
appid = "508af837"  # 填写控制台中获取的 APPID 信息
api_secret = "ZTNkZjBkMmQwNzY0ZDVlNjkxZjBhNjY4"  # 填写控制台中获取的 APISecret 信息
api_key = "3df6675e31e2480676984973fb4965db"  # 填写控制台中获取的 APIKey 信息

domain = "generalv3.5"  # v3版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v3环境的地址（"wss://spark-api.xf-yun.com/v3.1/chat）


class ChatApi:
    def __init__(self, appid, api_secret, api_key, Spark_url, domain):
        self.appid = appid
        self.api_secret = api_secret
        self.api_key = api_key
        self.Spark_url = Spark_url
        self.domain = domain

    def query(self, query):
        message = ModelApi.main(self.appid, self.api_secret, self.api_key, self.Spark_url, self.domain, query)
        return message

    def get_chat_response(self, question, index_name):
        prompt = Prompt().get_prompt('summary')
        es = ESApi("elastic", "9YfcLUcxKiDvtzef1piK")
        knowledge = es.search_es(index_name, question)
        prompt = prompt.replace("{0}", str(knowledge))
        print(prompt)
        query = [
            #{"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
        # query = [
        #     ChatMessage(role="system", content=prompt),
        #     ChatMessage(role="user", content=question),
        # ]

        message = self.query(query)
        return message

    def get_rephrase_question(self, question):
        prompt = Prompt().get_prompt('rephrase')
        prompt = prompt.replace("{0}", question)
        query = [
            ChatMessage(role="system", content=prompt),
            ChatMessage(role="user", content=question)
        ]
        message = self.query(query)
        return message


if __name__ == '__main__':
    while (1):
        question = input("\n" + "我:")
        print("星火:", end="")
        message = ModelApi.main(appid, api_secret, api_key, Spark_url, domain, question)
