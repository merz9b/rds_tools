#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:49
# @Author  : John
# @File    : tables.py


from ..utils.config_parser import mysql_conf
from sqlalchemy import MetaData
import warnings


def mapping_table_to_object(meta_data, table_name):
    try:
        return meta_data.tables[table_name]
    except KeyError:
        raise ValueError('Table <{tb}> not found'.format(tb=table_name))


meta_general = MetaData(bind=mysql_conf.production_engine())
meta_localuser = MetaData(bind=mysql_conf.production_engine('localuser'))

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    meta_general.reflect()
    meta_localuser.reflect()


# mapping db tables into python object
# # general
exchange = mapping_table_to_object(meta_general, 'exchange')
underlying = mapping_table_to_object(meta_general, 'underlying')
model_params = mapping_table_to_object(meta_general, 'model_params')

# >insert
usermodels = mapping_table_to_object(meta_general, 'usermodels')


# # localuser
contract_info = mapping_table_to_object(meta_localuser, 'contractinfo')
model_paramdef = mapping_table_to_object(meta_localuser, 'modelparamdef')
order_record_otc = mapping_table_to_object(meta_localuser, 'order_record_otc')
client_terminal = mapping_table_to_object(meta_localuser, 'client_terminal')
portfolio = mapping_table_to_object(meta_localuser, 'portfolio')
accountid_map = mapping_table_to_object(meta_localuser, 'accountid_map')
