#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:20
# @Author  : John
# @File    : test_script.py

from rds_tools.utils.config_parser import mysql_conf

from rds_tools.models.tables import (
    underlying,
    model_params,
    order_record_otc)

from rds_tools.db_executor import FuturexDB

import pandas as pd

from sqlalchemy.sql import select, and_

from rds_tools.models.tables import usermodels

pd.read_sql(select([usermodels]), usermodels.bind)


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


def insert_data(data_list, conditions, table):
    pass


def update_data(data, condition, table):
    pass


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
            'delta': self.delta,
            'gamma': self.gamma,
            'rho': self.rho,
            'theta': self.theta,
            'vega': self.vega
        }

    def __str__(self):
        return str(self.to_dict())

    __repr__ = __str__


class OptionType(object):

    def __init__(self, root_type=''):
        self._path = root_type

    def __getattr__(self, path):
        return OptionType('{0}/{1}'.format(self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(OptionType().Euro.Call)

print(OptionType().America.Call)

print(OptionType().Setting.Fold)

greeks = Greeks()

print(greeks)

greeks.vega = 1
greeks.delta = 100
greeks.theta = 21
greeks.gamma = 30
greeks.rho = 10


greeks.to_dict()


print(greeks.to_dict())


class AbstractOption(metaclass=abc.ABCMeta):

    def __init__(self):

        self.underlying_price = None
        self.strike_price = None
        self.volatility = None
        self.start_date = None
        self.end_date = None
        self.r = None
        self.dividend = None
        self.__price_process = None
        self.__option_type = None
        self.__NPV = None
        self.__greeks = Greeks()

    @property
    def oid(self):
        return 1

    @abc.abstractmethod
    def greeks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def NPV(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_process(self, process):
        """
        price movements process
        :param process: default, BSM
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_exercise(self, exercise_type):
        """
        set European or American
        :param exercise_type:
        :return: None
        """
    @abc.abstractmethod
    def set_type(self, option_type):
        """
        set call or put
        :param option_type:
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_parameters(
            self,
            underlying_price,
            strike_price,
            volatility,
            start_date,
            end_date,
            r,
            dividend=None):
        raise NotImplementedError


class AbstractPricingMachine(metaclass=abc.ABCMeta):

    def __init__(self, option: AbstractOption):
        self.option = option

    @abc.abstractmethod
    def compute_price(self, compute_engine):
        """
        using compute engine to get option price
        :param compute_engine: theoretical or MC
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_greeks(self):

        raise NotImplementedError


class Pricing(AbstractPricingMachine):
    def compute_price(self, compute_engine):
        pass

    def compute_greeks(self):
        pass


import abc
# option


class opt_1:
    def __init__(self):
        self.price = None

    @property
    def oid(self):
        return 1


class opt_2:
    def __init__(self):
        self.price = None

    @property
    def oid(self):
        return 2


method_dict = {}


def add_method(cls_ins):
    method_dict[cls_ins.id] = cls_ins()
    return cls_ins


class AbstractPricing(metaclass=abc.ABCMeta):
    id = None

    @abc.abstractmethod
    def __call__(self, option):
        raise NotImplementedError


@add_method
class PA(AbstractPricing):
    id = 1

    def __call__(self, option):
        assert option.oid == self.id, 'Wrong type of option'
        option.price = 1


@add_method
class PB(AbstractPricing):
    id = 2

    def __call__(self, option):
        assert option.oid == self.id, 'Wrong type of option'
        option.price = 2


def pricing(option):
    method_dict[option.oid](option)


o1 = opt_1()
print(o1.price)
# compute
pricing(o1)
print(o1.price)  # auto call PA to price o1


o2 = opt_2()
print(o2.price)
# compute price
pricing(o2)
print(o2.price)  # auto call PB to price o2

PA()(o2)
