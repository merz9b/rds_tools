# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 16:24
# @Author  : Xin Zhang
# @File    : setup.py.py


__author__ = 'Xin Zhang'

from setuptools import setup

with open('requirements.txt', 'r') as f:
    require_lists = f.read().split('\n')

setup(
    name='rds_tools',
    version=0.1,
    author=__author__,
    author_email='zhangxin_chn@126.com',
    description='Guosen rds tools library.',
    keywords='rds tool',
    packages=['rds_tools',
              'rds_tools.db_executor',
              'rds_tools.models',
              'rds_tools.utils',
              'rds_tools.db_executor.delete',
              'rds_tools.db_executor.insert',
              'rds_tools.db_executor.select',
              'rds_tools.db_executor.update'],
    dependency_links=[],
    install_requires=require_lists
)
