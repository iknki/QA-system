import json

class Prompt:
    def __init__(self, file_path='./prompt.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.prompt = json.load(f)

    def get_prompt(self, key):
        return self.prompt[key]