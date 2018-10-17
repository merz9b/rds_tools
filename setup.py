# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 16:24
# @Author  : Xin Zhang
# @File    : setup.py.py


__author__ = 'Xin Zhang'

from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    require_lists = f.read().split('\n')

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
