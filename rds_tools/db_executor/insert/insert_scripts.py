# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 9:50
# @Author  : Xin Zhang
# @File    : insert_scripts.py

import warnings
from pandas import read_sql, datetime
from rds_tools.models.tables import (exchange, underlying, model_params,
                                     contract_info, model_paramdef, order_record_otc,
                                     client_terminal, portfolio, accountid_map)
from sqlalchemy.sql import select, and_, distinct


warnings.filterwarnings('ignore', category=Warning)

class DbInsert:
    pass
