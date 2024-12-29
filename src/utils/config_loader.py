import autogen
import os
from dotenv import load_dotenv


def load_config(config_path):
    load_dotenv()
    return autogen.config_list_from_json(config_path)
