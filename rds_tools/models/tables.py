#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:49
# @Author  : John
# @File    : tables.py


from ..utils.config_parser import mysql_conf
from sqlalchemy import MetaData
import warnings

meta = MetaData(bind= mysql_conf.production_engine())

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    meta.reflect()

exchange = meta.tables.get('exchange')
underlying = meta.tables.get('underlying')
model_params = meta.tables.get('model_params')

