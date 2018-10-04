#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:20
# @Author  : John
# @File    : test_script.py



from rds_tools.utils.config_parser import mysql_conf

from rds_tools.models.tables import underlying, exchange, model_params

from rds_tools.select import FuturexDB


import pandas as pd

from sqlalchemy.sql import select, and_, distinct


pd.read_sql(select([underlying]).where(underlying.c.underlying_symbol == 'rb'), mysql_conf.production_engine())



pd.read_sql(select([underlying]), mysql_conf.production_engine())


s = mysql_conf.production_engine().execute(
    select([underlying.c.multiplier]).where(underlying.c.underlying_symbol == 'rb')
).scalar()

float(s)


modelinstance = '{exchange}-{index}'.format(exchange= 'DCE', index= 'C')

res_1 = mysql_conf.production_engine().execute(
    select([model_params]).where(
        and_(model_params.c.accountid == 20,
             model_params.c.model == 'wing',
             model_params.c.modelinstance.like('%{ml}%'.format(ml =modelinstance)))
    )
).fetchall()



pd.read_sql(select([model_params]).where(
        and_(model_params.c.accountid == 20,
             model_params.c.model == 'wing',
             model_params.c.modelinstance.like('%{ml}%'.format(ml =modelinstance)))
    ), mysql_conf.production_engine())




res_tmp = mysql_conf.production_engine().execute(
    select([distinct(model_params.c.modelinstance)]).where(model_params.c.accountid == 20)
).fetchall()

res = list(set(map(lambda x:'-'.join(x[0].split('-')[:-1]), res_tmp)))


pd.read_sql(exchange.select().where(exchange.c.symbol == 'CBOE'), mysql_conf.production_engine())


mysql_conf.production_engine().execute(exchange.select().where(exchange.c.symbol == 'CBOE')).fetchone()


mysql_conf.production_engine().execute(
    select([underlying.c.desc_zh]).where(
        and_(underlying.c.exchange_symbol == 'CFFEX',underlying.c.underlying_symbol == 'T')
    )
).scalar()



# GetDataMySQL.py

print(FuturexDB.get_param_data('DCE', 'C').head())

print(FuturexDB.get_param_data_std('DCE', 'C'))

print(FuturexDB.get_future_info())


# PyMySQLreadZH.py

print(FuturexDB.get_exchange_zh('CBOE'))

print(FuturexDB.get_exchange_zh('LME'))

print(FuturexDB.get_contract_zh('CFFEX', 'T'))


# GetUnderling.py
print(FuturexDB.get_underlying())



print(FuturexDB.get_multiplier('rb'))





print(FuturexDB._fxdb_cache)

FuturexDB.clear_all_cache()

print(FuturexDB._fxdb_cache)



