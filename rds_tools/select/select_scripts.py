#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 15:02
# @Author  : John
# @File    : select_scripts.py

import warnings
from ..utils.config_parser import mysql_conf
from ..utils.read_sqls import read_raw_sql
from ..models.tables import exchange, underlying, model_params
from sqlalchemy.sql import select, and_, distinct

warnings.filterwarnings('ignore', category= Warning)

class FuturexDB:


    _fxdb_cache = {}

    @classmethod
    def clear_all_cache(cls):

        cls._fxdb_cache = dict()

    @classmethod
    def get_param_data(cls, exchange_name,index,model='wing'):


        modelinstance = '{exchange}-{index}'.format(exchange=exchange_name, index=index)

        tdf = read_raw_sql(select([model_params]).where(
            and_(model_params.c.accountid == 20,
                 model_params.c.model == model,
                 model_params.c.modelinstance.like('%{ml}%'.format(ml =modelinstance)))
        ))
        return tdf

    @classmethod
    def get_param_data_std(cls, exchange,index,model='wing'):

        data = cls.get_param_data(exchange, index, model = model)

        tmp = data[['modelinstance', 'paramname', 'paramvalue']]

        tmp = tmp.set_index(['modelinstance', 'paramname'])

        tmp = tmp.unstack()

        new_cols = [c[1] for c in tmp.columns]

        tmp.columns = new_cols

        tmp = tmp.assign(days=
                         lambda tdf: list(map(
                             lambda x: int(x.split('-')[2]), tdf.index))) \
            .sort_values(by=['days'])

        return tmp


    @classmethod
    def get_future_info(cls):

        res_tmp = mysql_conf.production_engine().execute(
            select(
                [distinct(model_params.c.modelinstance)]
                )
            .where(
                model_params.c.accountid == 20
                )
            ).fetchall()

        return list(set(map(lambda x: '-'.join(x[0].split('-')[:-1]), res_tmp)))

    @classmethod
    def get_exchange_zh(cls, exchange_name):

        if cls._fxdb_cache.get('exchange_zh') is None:
            cls._fxdb_cache['exchange_zh'] = dict()

        if cls._fxdb_cache['exchange_zh'].get(exchange_name) is None:

            res = mysql_conf.production_engine().execute(
                select([exchange.c.desc_zh]).where(exchange.c.symbol == exchange_name)
            ).scalar()


            cls._fxdb_cache['exchange_zh'][exchange_name] = res

            return res

        else:
            return cls._fxdb_cache['exchange_zh'][exchange_name]

    @classmethod
    def get_contract_zh(cls, exchange_name, underlying_name):

        if cls._fxdb_cache.get('contract_zh') is None:
            cls._fxdb_cache['contract_zh'] = dict()

        if cls._fxdb_cache['contract_zh'].get((exchange_name, underlying_name)) is None:

            res = mysql_conf.production_engine().execute(
                select([underlying.c.desc_zh]).where(
                    and_(
                        underlying.c.exchange_symbol == exchange_name,
                        underlying.c.underlying_symbol == underlying_name)
                )
            ).scalar()

            cls._fxdb_cache['contract_zh'][(exchange_name, underlying_name)] = res

            return res

        else:

            return cls._fxdb_cache['contract_zh'][(exchange_name, underlying_name)]

    @classmethod
    def get_underlying(cls):

        # read table to data frame
        tmp = read_raw_sql(select([distinct(model_params.c.modelinstance)]).where(and_(
            model_params.c.accountid == 20,
            model_params.c.model == 'wing'
        )))

        # expand columns
        tmp1 = tmp.iloc[:, 0].str.split('-', expand=True).iloc[:, :2]

        selected_column_names = ['exchange', 'underlying']

        # set columns' names
        tmp1.columns = selected_column_names

        # drop duplicates
        tmp1 = tmp1.drop_duplicates(selected_column_names).reset_index(drop=True)

        # set exchange zh name
        tmp1 = tmp1.assign(exchange_zh=lambda tb: tb['exchange'].apply(lambda x: cls.get_exchange_zh(x)))

        # set contract zh name
        tmp1 = tmp1.assign(
            contract_zh=lambda tb: tb.apply(lambda x: cls.get_contract_zh(x['exchange'], x['underlying']),
                                            axis=1))
        return tmp1

    @classmethod
    def get_multiplier(cls, underlying_symbol):

        if cls._fxdb_cache.get('ud_multiplier') is None:
            cls._fxdb_cache['ud_multiplier'] = dict()

        if cls._fxdb_cache['ud_multiplier'].get(underlying_symbol) is None:

            s = mysql_conf.production_engine().execute(
                select([underlying.c.multiplier]).where(underlying.c.underlying_symbol == underlying_symbol)
            ).scalar()

            res = float(s)

            cls._fxdb_cache['ud_multiplier'][underlying_symbol] = res

            return res

        else:
            return cls._fxdb_cache['ud_multiplier'][underlying_symbol]




