# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 16:24
# @Author  : Xin Zhang
# @File    : setup.py.py


__author__ = 'Xin Zhang'

import json
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    require_lists = f.read().split('\n')

with open('connection_info.json.bak', 'r') as f:
    cfg = json.loads(f.read())
    with open('./rds_tools/db_configs/connection_info.json', 'w+') as f1:
        f1.write(json.dumps(cfg))

setup(
    name='rds_tools',
    version=0.1,
    author=__author__,
    author_email='zhangxin_chn@126.com',
    description='Guosen rds tools library.',
    keywords='rds tool',
    packages=find_packages(),
    include_package_data=True,
    dependency_links=[],
    install_requires=require_lists
)
