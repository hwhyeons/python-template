from typing import Any, Final
import os
import configparser
import os.path

CATEGORY_DEFAULT: Final = 'DEFAULT'

class ConfigHelper:
    def __init__(self,config_file_path: str, key_default_value_dict: dict[str,Any], create_if_not_exists: bool = True):
        self.config_file_path = config_file_path
        self.key_default_value_dict = key_default_value_dict
        self.__make_config(ignore_if_exists=True)

    def __make_config(self, ignore_if_exists: bool = True):
        config = configparser.ConfigParser()
        config[CATEGORY_DEFAULT] = {}
        if ignore_if_exists and os.path.exists(self.config_file_path):
            return
        for key,val in self.key_default_value_dict.items():
            config[CATEGORY_DEFAULT][key] = val
        # example : config[CATEGORY_DEFAULT]['id'] = 'test1234'
        with open(self.config_file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    def get_value(self, key: str) -> str | None:
        rt = self.get_key_value_multiple(key)
        if not rt:
            return None
        return rt[key]

    def get_key_value_multiple(self, *keys) -> dict[str,str]:
        """
        여러 key,value를 한번에
        :param keys:
        :return:
        """

        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f"config file not found : {self.config_file_path}")

        config = configparser.ConfigParser()
        config.read(self.config_file_path, encoding='utf-8')
        key_values: dict[str,str] = dict()
        for key in keys:
            key_values[key] = config[CATEGORY_DEFAULT][key]
        return key_values


    def set_value(self,key:str, val: str):
        return self.set_value_multiple((key, val))

    # 키값 설정
    def set_value_multiple(self, *key_val: tuple[str,str]):
        # config 없으면 생성
        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f"config file not found : {self.config_file_path}")
        config = configparser.ConfigParser()
        config.read(self.config_file_path, encoding='utf-8')
        for kv in key_val:
            key,val = kv
            config[CATEGORY_DEFAULT][key] = val
        with open(self.config_file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)


if __name__ == '__main__':
    test_config = ConfigHelper("test.ini",{'id':'test1234','pw':'test1234'})
    print(test_config.get_value('id'))
    print(test_config.set_value('pw','asdf'))
    pass
