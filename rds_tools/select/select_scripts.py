#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 15:02
# @Author  : John
# @File    : select_scripts.py

import warnings
from pandas import read_sql, datetime
from ..models.tables import (exchange, underlying, model_params,
                             contract_info, model_paramdef, order_record_otc,
                             client_terminal, portfolio, accountid_map)
from sqlalchemy.sql import select, and_, distinct


warnings.filterwarnings('ignore', category=Warning)


class FuturexDB:

    _fxdb_cache = {}

    @classmethod
    def clear_all_cache(cls):

        cls._fxdb_cache = dict()

    @classmethod
    def get_param_data(cls, exchange_name, index, model='wing', account_id=20):

        modelinstance = '{exchange}-{index}'.format(
            exchange=exchange_name, index=index)

        tdf = read_sql(
            select(
                [model_params]).where(
                and_(
                    model_params.c.accountid == account_id,
                    model_params.c.model == model,
                    model_params.c.modelinstance.like(
                        '%{ml}%'.format(
                            ml=modelinstance)))),
            model_params.bind)
        return tdf

    @classmethod
    def get_param_data_std(cls, exchange_, index, model='wing'):

        data = cls.get_param_data(exchange_, index, model=model)

        tmp = data[['modelinstance', 'paramname', 'paramvalue']]

        tmp = tmp.set_index(['modelinstance', 'paramname'])

        tmp = tmp.unstack()

        new_cols = [c[1] for c in tmp.columns]

        tmp.columns = new_cols

        tmp = tmp.assign(days=lambda tdf: list(map(
            lambda x: int(x.split('-')[2]), tdf.index))) \
            .sort_values(by=['days'])

        return tmp

    @classmethod
    def get_future_info(cls, account_id=20):

        res_tmp = select(
            [distinct(model_params.c.modelinstance)]
        ).where(
            model_params.c.accountid == account_id).execute().fetchall()

        return list(
            set(map(lambda x: '-'.join(x[0].split('-')[:-1]), res_tmp)))

    @classmethod
    def get_exchange_zh(cls, exchange_name):

        if cls._fxdb_cache.get('exchange_zh') is None:
            cls._fxdb_cache['exchange_zh'] = dict()

        if cls._fxdb_cache['exchange_zh'].get(exchange_name) is None:

            res = select([exchange.c.desc_zh]).where(
                exchange.c.symbol == exchange_name).execute().scalar()

            cls._fxdb_cache['exchange_zh'][exchange_name] = res

            return res

        else:
            return cls._fxdb_cache['exchange_zh'][exchange_name]

    @classmethod
    def get_contract_zh(cls, exchange_name, underlying_name):

        if cls._fxdb_cache.get('contract_zh') is None:
            cls._fxdb_cache['contract_zh'] = dict()

        if cls._fxdb_cache['contract_zh'].get(
                (exchange_name, underlying_name)) is None:

            res = select([underlying.c.desc_zh]).where(
                and_(
                    underlying.c.exchange_symbol == exchange_name,
                    underlying.c.underlying_symbol == underlying_name)
            ).execute().scalar()

            cls._fxdb_cache['contract_zh'][(
                exchange_name, underlying_name)] = res

            return res

        else:

            return cls._fxdb_cache['contract_zh'][(
                exchange_name, underlying_name)]

    @classmethod
    def get_underlying(cls, account_id=20):

        # read table to data frame
        tmp = read_sql(select([distinct(model_params.c.modelinstance)]).where(and_(
            model_params.c.accountid == account_id,
            model_params.c.model == 'wing'
        )), model_params.bind)

        # expand columns
        tmp1 = tmp.iloc[:, 0].str.split('-', expand=True).iloc[:, :2]

        selected_column_names = ['exchange', 'underlying']

        # set columns' names
        tmp1.columns = selected_column_names

        # drop duplicates
        tmp1 = tmp1.drop_duplicates(
            selected_column_names).reset_index(drop=True)

        # set exchange zh name
        tmp1 = tmp1.assign(
            exchange_zh=lambda tb: tb['exchange'].apply(
                lambda x: cls.get_exchange_zh(x)))

        # set contract zh name
        tmp1 = tmp1.assign(
            contract_zh=lambda tb: tb.apply(
                lambda x: cls.get_contract_zh(
                    x['exchange'],
                    x['underlying']),
                axis=1))
        return tmp1

    @classmethod
    def get_multiplier(cls, underlying_symbol):

        if cls._fxdb_cache.get('ud_multiplier') is None:
            cls._fxdb_cache['ud_multiplier'] = dict()

        if cls._fxdb_cache['ud_multiplier'].get(underlying_symbol) is None:

            s = select([underlying.c.multiplier]).where(
                underlying.c.underlying_symbol == underlying_symbol).execute().scalar()

            res = float(s)

            cls._fxdb_cache['ud_multiplier'][underlying_symbol] = res

            return res

        else:
            return cls._fxdb_cache['ud_multiplier'][underlying_symbol]

    @classmethod
    def get_contract(cls, exchange_, contract_, date_=None):
        if date_ is None:
            date_ = datetime.now().date()

        contract_list = select([contract_info.c.contract_symbol]).where(and_(
            contract_info.c.exchange_symbol == exchange_,
            contract_info.c.underlying_symbol == contract_,
            contract_info.c.expiration > date_
        )).execute().fetchall()

        return [s[0] for s in contract_list]

    @classmethod
    def get_paramdef_by_model(cls, model_name):

        tdf = read_sql(
            select(
                [model_paramdef]).where(
                model_paramdef.c.model == model_name),
            model_paramdef.bind)

        return tdf

    @classmethod
    def get_order_record_otc(cls, account_id):

        tdf = read_sql(select([order_record_otc]).where(
            order_record_otc.c.accountid == account_id
        ), order_record_otc.bind)

        return tdf

    @classmethod
    def get_order_param(cls, account_id, model_instance):

        tdf = read_sql(
            select(
                [model_params]).where(
                and_(
                    model_params.c.accountid == account_id,
                    model_params.c.modelinstance == model_instance)),
            model_params.bind)

        param_data = tdf.pivot('modelinstance', 'paramname', 'paramstring')

        return param_data

    @classmethod
    def get_role_by_name(cls, account_id):

        tdf = read_sql(
            select(
                [client_terminal]).where(
                client_terminal.c.accountid == account_id),
            client_terminal.bind)

        return tdf

    @classmethod
    def get_role_by_role_type(cls, role_type):

        tdf = read_sql(
            select(
                [client_terminal]).where(
                client_terminal.c.roletype == role_type),
            client_terminal.bind)

        return tdf

    @classmethod
    def get_portfolio_by_id(cls, account_id):

        tdf = read_sql(
            select([portfolio]).where(
                portfolio.c.accountid == account_id
            ),
            portfolio.bind
        )

        return tdf

    @classmethod
    def get_order_by_risk_id(cls, risk_id):

        tdf = read_sql(select([order_record_otc]).where(
            order_record_otc.c.riskid == risk_id
        ), order_record_otc.bind)

        return tdf

    @classmethod
    def get_account_id_map_by_master_id(cls, master_id):

        tdf = read_sql(
            select([accountid_map]).where(
                accountid_map.c.master_id == master_id
            ),
            accountid_map.bind
        )

        return tdf

    @classmethod
    def get_trader_id_by_master_id(cls, master_id, role_type=12):

        s_id = cls.get_account_id_map_by_master_id(master_id).slave_id
        trader_list = cls.get_role_by_role_type(role_type)

        return trader_list[trader_list['accountid'].isin(s_id)]

    @classmethod
    def get_order_record_by_symbol_traderid(cls, port_symbol, trader_id):

        tdf = read_sql(
            select([order_record_otc]).where(
                and_(
                    order_record_otc.c.portfolio_symbol == port_symbol,
                    order_record_otc.c.traderid == trader_id,
                    order_record_otc.c.status == 1
                )
            ),
            order_record_otc.bind
        )

        return tdf

    @classmethod
    def get_order_record_by_model_instance(cls, model_instance):

        tdf = read_sql(
            select([order_record_otc]).where(
                and_(
                    order_record_otc.c.modelinstance == model_instance
                )
            ),
            order_record_otc.bind
        )

        return tdf

    @classmethod
    def get_ref_contract(cls):

        res = select([model_params.c.paramstring]).where(
            and_(model_params.c.model.in_(['oao', 'ovo']),
                 model_params.c.paramname == 'ref_contract'))\
            .execute().fetchall()

        return list(set(r[0] for r in res))
