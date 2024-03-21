from llmmodel.model import Model
from config.config import Config



text = []


# length = 0

# def getText(role, content):
#     jsoncon = {}
#     jsoncon["role"] = role
#     jsoncon["content"] = content
#     text.append(jsoncon)
#     return text
#
#
# def getlength(text):
#     length = 0
#     for content in text:
#         temp = content["content"]
#         leng = len(temp)
#         length += leng
#     return length
#
#
# def checklen(text):
#     while (getlength(text) > 8000):
#         del text[0]
#     return text


if __name__ == '__main__':
    config = Config("./config.yaml")
    #text.clear
    while (1):
        query = input("\n" + "我:")
        #question = checklen(getText("user", Input))
        print("星火:", end="")
        Model(config)
        Model.answer(query)
        #getText("assistant", Model.answer)
        # print(str(text))
