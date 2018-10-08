#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:49
# @Author  : John
# @File    : tables.py


from ..utils.config_parser import mysql_conf
from sqlalchemy import MetaData
import warnings

meta_general = MetaData(bind=mysql_conf.production_engine())
meta_localuser = MetaData(bind=mysql_conf.production_engine('localuser'))

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    meta_general.reflect()
    meta_localuser.reflect()

# mapping db tables into python object
# # general
exchange = meta_general.tables.get('exchange')
underlying = meta_general.tables.get('underlying')
model_params = meta_general.tables.get('model_params')

# # localuser
contract_info = meta_localuser.tables.get('contractinfo')
model_paramdef = meta_localuser.tables.get('modelparamdef')
order_record_otc = meta_localuser.tables.get('order_record_otc')
client_terminal = meta_localuser.tables.get('client_terminal')
portfolio = meta_localuser.tables.get('portfolio')
accountid_map = meta_localuser.tables.get('accountid_map')
