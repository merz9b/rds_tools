#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:26
# @Author  : John
# @File    : config_parser.py


import os
import json
from sqlalchemy import create_engine
from rds_tools import PROJECT_PATH

from .tools import get_public_ip


class JsonConfig:
    def __init__(self, config_path):
        self.path = config_path
        self.info = None
        self.is_read = False

    def read_config(self):
        with open(self.path, 'r') as f:
            self.info = json.loads(f.read())
        self.is_read = True


class MysqlConfig(JsonConfig):
    def __init__(self):
        super(
            MysqlConfig,
            self).__init__(
            os.path.join(
                PROJECT_PATH,
                'db_configs',
                'connection_info.json'))

    def test_info(self):
        if not self.is_read:
            self.read_config()
        return self.info['testing']

    def production_info(self):
        if not self.is_read:
            self.read_config()
        return self.info['production']

    def test_engine(self):
        pass

    def production_engine(self, user='gxqh'):
        conn_str = '''mysql+pymysql://{usr}:{pwd}@{ip}:{port}/{db}?charset=utf8'''
        info = self.production_info()
        tgt_ip = info[user]['ip']
        try:
            current_ip = get_public_ip()
        except:
            current_ip = tgt_ip
        if current_ip == tgt_ip:
            info[user]['ip'] = 'localhost'
        return create_engine(conn_str.format(**info[user]))


mysql_conf = MysqlConfig()
