#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:20
# @Author  : John
# @File    : test_script.py

from rds_tools.utils.config_parser import mysql_conf

import time

from rds_tools.models.tables import (
    underlying,
    model_params,
    order_record_otc)

from rds_tools.db_executor import FuturexDB

import pandas as pd

from sqlalchemy.sql import select, and_, insert

from rds_tools.models.tables import usermodels

time.time()

s1 = {
    'exercise_type': '0',
    'exp_date': '2018-06-13',
    'init_date': '2018-06-13',
    'option_type': '1',
    'ref_contract': 'c1901',
    'ref_exchange': 'DCE',
    'ref_underlying': 'c',
    'strike': '1820'
}

# ordername
model_instance = 'ovo123'  # fk
model_name = 'ovo'
account_id = '13001'  # fk

# new order api
# OrderManagement
# NewOrder.py => NewOrder
FuturexDB.insert.new_order(model_instance, model_name, account_id)

# new param data api
# OrderManagement
# NewParamData.py => NewParamData
FuturexDB.insert.new_param_data(s1, model_instance, model_name, account_id)

# new create order api
# OrderManagement
# CreateOrder.py => CreateOrder
FuturexDB.insert.create_order(model_instance, model_name, account_id, s1)

# new order record api
# OrderManagement
# NewOrderRecord.py => NewOrderRecord
s2 = {'customerid': '11001',
      'riskid': '14001',
      'price': '1234',
      'quantity': '16',
      'quantity_filled': '0',
      'is_buy': '1',
      'is_open': '1',
      'exec_type': '9',
      'tif': '0',
      'status': '14',
      'trading_type': '0',
      'tradingday': '2018-09-01',
      'errorcode': '0'}

FuturexDB.insert.new_order_record(s2, account_id, model_instance)

# update order_record_otc api
# OrderManagement | RiskManagement=>RiskMgt
# UpdateOrderStatus.py=> UpdateOrderStatus
FuturexDB.update.order_record_otc('status', '1', model_instance)

# update model_params api
# VolatilityModel
# ChangeParamData.py => Writeparamdata
FuturexDB.update.model_params('alpha', '0', 'DCE', 'C', '1')


# deleting
# 1
rsp_d1 = model_params.bind.execute(
    model_params.delete().where(
        model_params.c.modelinstance == model_instance
    )
)

rsp_d1.close()
print(rsp_d1.rowcount)
print(rsp_d1.closed)

# 2
rsp_d3 = order_record_otc.bind.execute(
    order_record_otc.delete().where(
        order_record_otc.c.modelinstance == model_instance
    )
)
rsp_d3.close()
print(rsp_d3.rowcount)
print(rsp_d3.closed)

# 3
# OrderManagement
# DelOrder.py => DelOrder
print(FuturexDB.delete.del_order(model_name, model_instance, account_id))


# Reference Documents


# ALL SELECT
# > Volatility Model
# GetDataMySQL.py

print(FuturexDB.select.get_param_data('DCE', 'C').head())

print(FuturexDB.select.get_param_data_std('DCE', 'C'))

print(FuturexDB.select.get_future_info())


# PyMySQLreadZH.py

print(FuturexDB.select.get_exchange_zh('CBOE'))

print(FuturexDB.select.get_exchange_zh('LME'))

print(FuturexDB.select.get_contract_zh('CFFEX', 'T'))


# GetUnderling.py
print(FuturexDB.select.get_underlying())


print(FuturexDB.select.get_multiplier('rb'))


# > OptionCalc
# GetContract.py
print(FuturexDB.select.get_contract('DCE', 'C'))


# > OrderManagement
# GetModelParamName.py
# replace GetContract
print(FuturexDB.select.get_paramdef_by_model('ovo'))

# GetOrderList.py
# replace GetOrderList
print(FuturexDB.select.get_order_record_otc('13001'))


# GetOrderParam.py
print(FuturexDB.select.get_order_param(
    '13001', 'ovo_13001_11005_1533785827.5574322'))


# GetRoleName.py
print(FuturexDB.select.get_role_by_name('13001'))

# GetRoletype.py | RiskManagement/GetRiskList.py/GetRiskList
print(FuturexDB.select.get_role_by_role_type('13'))

# risk list
print(FuturexDB.select.get_role_by_role_type('14'))


# > RiskManagement
# GetPoSymbol.py
print(FuturexDB.select.get_portfolio_by_id('12001'))


# GetRiskList.py
print(FuturexDB.select.get_order_by_risk_id('14001'))


# GetTraderId.py

# GetSlaveId
print(FuturexDB.select.get_account_id_map_by_master_id('14001'))

# GetTraderId
print(FuturexDB.select.get_trader_id_by_master_id('14001'))

# GetPortDetail.py
# GetPortDetail
print(FuturexDB.select.get_order_record_by_symbol_traderid('OTC-DCE-i', 12001))
# GetPortDetail2
print(FuturexDB.select.get_order_record_by_model_instance(
    'ovo_13001_11005_1533785827.5574322'))
# GetPortSub
print(FuturexDB.select.get_ref_contract())

print(FuturexDB.select._fxdb_cache)


FuturexDB.select.clear_all_cache()

print(FuturexDB.select._fxdb_cache)


############################################################
# ORM Example

pd.read_sql(
    select(
        [underlying]).where(
            underlying.c.underlying_symbol == 'rb'),
    mysql_conf.production_engine())


pd.read_sql(select([underlying]), mysql_conf.production_engine())


s = underlying.bind.execute(select([underlying.c.multiplier]).where(
    underlying.c.underlying_symbol == 'rb'))

print(s.rowcount)
print(s.returns_rows)


float(s.scalar())


stmt = select([underlying.c.multiplier]).where(
    underlying.c.underlying_symbol == 'rb')

stmt.execute().scalar()


modelinstance = '{exchange}-{index}'.format(exchange='DCE', index='C')

res_1 = model_params.bind.execute(
    select(
        [model_params]).where(
            and_(
                model_params.c.accountid == 20,
                model_params.c.model == 'wing',
                model_params.c.modelinstance.like(
                    '%{ml}%'.format(
                        ml=modelinstance))))).fetchall()


pd.read_sql(select([model_params]).where(
    and_(model_params.c.accountid == 20,
         model_params.c.model == 'wing',
         model_params.c.modelinstance.like('%{ml}%'.format(ml=modelinstance)))
), mysql_conf.production_engine())


def query_frame_from_table(table, column_list=None, conditions=None):
    if column_list is None:
        select_param = [table]
    else:
        assert isinstance(column_list, list), 'Expected type of column_list is list, given: %s' % (
            type(column_list))
        select_param = [table.c.get(s) for s in column_list]

    if conditions is None:
        return pd.read_sql(select(select_param), table.bind)

    else:
        return pd.read_sql(
            select(select_param).where(
                and_(*conditions)
            ), table.bind
        )


query_frame_from_table(underlying,
                       column_list=['underlying_symbol'],
                       conditions=[
                           underlying.c.underlying_symbol == 'OI'
                       ])


pd.read_sql(
    select([order_record_otc]).where(
        and_(
            order_record_otc.c.portfolio_symbol == 'OTC-DCE-i',
            order_record_otc.c.traderid == 12001,
            order_record_otc.c.status == 1
        )
    ),
    order_record_otc.bind
)
