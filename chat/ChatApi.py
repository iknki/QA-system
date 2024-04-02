from llmmodel import ModelApi as ModelApi
from llmmodel.Prompt import Prompt
from db.ES.ESApi import ESApi

# 以下密钥信息从控制台获取
appid = "508af837"  # 填写控制台中获取的 APPID 信息
api_secret = "ZTNkZjBkMmQwNzY0ZDVlNjkxZjBhNjY4"  # 填写控制台中获取的 APISecret 信息
api_key = "3df6675e31e2480676984973fb4965db"  # 填写控制台中获取的 APIKey 信息

domain = "generalv3.5"  # v3版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v3环境的地址（"wss://spark-api.xf-yun.com/v3.1/chat）

text = []




# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def get_chat_response(question, index_name):
    text.clear
    prompt = Prompt().get_prompt()
    es = ESApi("elastic", "w9nF5G7Pjt_lpVAcbqFy")
    knowledge = es.search_es(index_name, question)
    prompt = prompt.replace("{0}", str(knowledge))
    query = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": question}
    ]

    message = ModelApi.main(appid, api_secret, api_key, Spark_url, domain, query)
    return message




if __name__ == '__main__':
    text.clear
    while (1):
        question = input("\n" + "我:")
        print("星火:", end="")
        message = ModelApi.main(appid, api_secret, api_key, Spark_url, domain, question)

