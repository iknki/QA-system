
from typing import NamedTuple

import yaml


class LLMKey(NamedTuple):
    key: str
    secret: str


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            self.config_file = "../config.yaml"
        else:
            self.config_file = config_file

    def get_config(self):
        with open(self.config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def get_LLM_config(self):
        config = self.get_config()
        LLMConfig = config["llm"]

        sparkAPPID = LLMConfig["APPID"]
        sparkSecret = LLMConfig["APISecret"]
        sparkAPIKey = LLMConfig["APIKey"]
        sparkURL = LLMConfig["URL"]
        sparkDomain = LLMConfig["Domain"]
        return {
            "APPID": sparkAPPID,
            "APISecret": sparkSecret,
            "APIKey": sparkAPIKey,
            "URL": sparkURL,
            "Domain": sparkDomain,
        }