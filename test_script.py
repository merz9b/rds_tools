#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:20
# @Author  : John
# @File    : test_script.py



from rds_tools.utils.config_parser import mysql_conf

from rds_tools.models.tables import (underlying, exchange, model_params,
                                     contract_info, model_paramdef, client_terminal,
                                     portfolio, accountid_map, order_record_otc)

from rds_tools.select import FuturexDB

import pandas as pd

from sqlalchemy.sql import select, and_, distinct


pd.read_sql(select([underlying]).where(underlying.c.underlying_symbol == 'rb'), mysql_conf.production_engine())



pd.read_sql(select([underlying]), mysql_conf.production_engine())


s = underlying.bind.execute(
    select([underlying.c.multiplier]).where(underlying.c.underlying_symbol == 'rb')
)

print(s.rowcount)
print(s.returns_rows)


float(s.scalar())


modelinstance = '{exchange}-{index}'.format(exchange= 'DCE', index= 'C')

res_1 = model_params.bind.execute(
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



#
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



# > Volatility Model
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


# > OptionCalc
# GetContract.py
print(FuturexDB.get_contract('DCE', 'C'))



# > OrderManagement
# GetModelParamName.py
# replace GetContract
print(FuturexDB.get_paramdef_by_model('ovo'))

# GetOrderList.py
# replace GetOrderList
print(FuturexDB.get_order_record_otc('13001'))


# GetOrderParam.py
print(FuturexDB.get_order_param('13001', 'ovo_13001_11005_1533785827.5574322'))


# GetRoleName.py
print(FuturexDB.get_role_by_name('13001'))

# GetRoletype.py | RiskManagement/GetRiskList.py/GetRiskList
print(FuturexDB.get_role_by_role_type('13'))

# risk list
print(FuturexDB.get_role_by_role_type('14'))



# > RiskManagement
# GetPoSymbol.py
print(FuturexDB.get_portfolio_by_id('12001'))


# GetRiskList.py
print(FuturexDB.get_order_by_risk_id('14001'))


# GetTraderId.py

# GetSlaveId
print(FuturexDB.get_account_id_map_by_master_id('14001'))

# GetTraderId
print(FuturexDB.get_trader_id_by_master_id('14001'))

print(FuturexDB._fxdb_cache)

FuturexDB.clear_all_cache()

print(FuturexDB._fxdb_cache)




def query_frame_from_table(table, column_list = None, conditions = None):
    if column_list is None:
        select_param = [table]
    else:
        assert isinstance(column_list, list), 'Expected type of column_list is list, given: %s'%(type(column_list))
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
                       conditions= [
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



import abc

class Greeks:
    def __init__(self):
        self._delta = None
        self._gamma = None
        self._rho = None
        self._theta = None
        self._vega = None
    @property
    def delta(self):
        return self._delta
    @property
    def gamma(self):
        return self._gamma
    @property
    def rho(self):
        return self._rho
    @property
    def theta(self):
        return self._theta
    @property
    def vega(self):
        return self._vega

    @delta.setter
    def delta(self, delta):
        self._delta = delta

    @gamma.setter
    def gamma(self, gamma):
        self._gamma = gamma

    @rho.setter
    def rho(self, rho):
        self._rho = rho

    @theta.setter
    def theta(self, theta):
        self._theta = theta

    @vega.setter
    def vega(self, vega):
        self._vega = vega

    def to_dict(self):

        return {
            'delta':self.delta,
            'gamma':self.gamma,
            'rho':self.rho,
            'theta':self.theta,
            'vega':self.vega
        }


class TypeChain:
    def __init__(self):
        pass



greeks = Greeks()

greeks.vega = 1
greeks.delta = 100
greeks.theta = 21
greeks.gamma = 30
greeks.rho = 10

greeks.to_dict()





class Option(metaclass= abc.ABCMeta):

    @abc.abstractmethod
    def greeks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def NPV(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_process(self, process):
        raise NotImplementedError

    @abc.abstractmethod
    def set_type(self, option_type):
        raise NotImplementedError

    @abc.abstractmethod
    def set_engine(self, pricing_engine):
        raise NotImplementedError

    @abc.abstractmethod
    def set_parameters(self, underlying_price, strike_price, volatility, start_date, end_date, r, dividend = None):
        raise NotImplementedError







