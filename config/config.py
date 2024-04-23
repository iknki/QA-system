from typing import NamedTuple
import json
import yaml


class LLMKey(NamedTuple):
    key: str
    secret: str


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            self.config_file = "./config.yaml"
        else:
            self.config_file = config_file

        self.config = self.get_config()

    def get_config(self):
        with open(self.config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def edit_config(self, settings):
        # 将Python字典转换为YAML字符串
        yaml_string = yaml.dump(settings, default_flow_style=False)
        
        # 将YAML字符串写入文件
        with open(self.config_file, 'w') as file:
            file.write(yaml_string)
        print('设置修改成功')

