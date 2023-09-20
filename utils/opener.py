import json

from utils.var import *


def get_bot_repo_version():
    with open(local_version, 'r') as version_file:
        bot_version = version_file.read()
    return bot_version

def get_config():
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config