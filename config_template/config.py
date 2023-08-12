from typing import Tuple
import os
import configparser
import os.path


CONFIG_FILE = '/config.ini' # config 파일 경로는 프로젝트 기본 경로로 설정하는게 좋다 -> 현재 경로로 하게 되면 다른 폴더에서는 다른 config파일이 생성됨

CATEGORY = "CATEGORY_inform"

def make_config():
    config = configparser.ConfigParser()
    config[CATEGORY] = {}
    config[CATEGORY]['id'] = 'test1234'
    config[CATEGORY]['pw'] = 'asdf1234'
    config[CATEGORY]['next_key'] = '1234567'

    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def get_keys(key_type:str, *keys):
    # config 없으면 생성
    if not os.path.exists(CONFIG_FILE):
        make_config()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    values = []
    for key in keys:
        values.append(config[key_type][key])
    if len(values) == 0:
        return None
    elif len(values) == 1:
        return values[0]
    else:
        return tuple(values)


# 키값 설정
def set_keys(key_type:str, *key_val:Tuple[str,str]):
    # config 없으면 생성
    if not os.path.exists(CONFIG_FILE):
        make_config()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    for kv in key_val:
        key,val = kv
        config[key_type][key] = val
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
