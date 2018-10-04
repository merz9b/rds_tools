#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:58
# @Author  : John
# @File    : read_sqls.py


import pandas as pd
from .config_parser import mysql_conf


def read_raw_sql(raw_sql, engine = mysql_conf.production_engine()):
    return pd.read_sql(raw_sql, engine)



