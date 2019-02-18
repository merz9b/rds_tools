# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 11:26
# @Author  : Xin Zhang
# @File    : test1.py

from sqlalchemy.ext.automap import automap_base
from rds_tools.utils.config_parser import mysql_conf

conn_str = '''mysql+pymysql://{usr}:{pwd}@{ip}:{port}/{db}?charset=utf8'''
info = mysql_conf.production_info()
conn_str.format(**info['gxqh'])

ms_engine = mysql_conf.production_engine()

Base = automap_base()
# Base.prepare(ms_engine, reflect = True)
# "mysql+pymysql://gxjy:MyNewPass5!@localhost:33306/futurexdb?charset=utf8"

'''
CREATE OR REPLACE ALGORITHM = UNDEFINED 
DEFINER = `gxqh`@`%` 
SQL SECURITY DEFINER
VIEW futurexdb.vm_underlying_portfolio
AS
select t3.*, t4.riskid from (select 
t1.trading_exchange_symbol AS ref_exchange,
t1.trading_underlying_symbol AS ref_underlying,
t2.portfolio_symbol AS portfolio_symbol,
t2.accountid AS traderid
from futurexdb.strategy_underlying t1
left join futurexdb.strategy_portfolio t2 
on 
t1.accountid = t2.accountid 
and
t1.strategy_symbol = t2.strategy_symbol) t3
left join 
(SELECT master_id as riskid, slave_id as traderid FROM futurexdb.accountid_map where relation = 2) t4
on 
t3.traderid = t4.traderid
;
'''
