# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 9:50
# @Author  : Xin Zhang
# @File    : insert_scripts.py

import warnings
import traceback
from rds_tools.models.tables import (meta_general, meta_localuser,
                                     usermodels, model_params,
                                     order_record_otc)


warnings.filterwarnings('ignore', category=Warning)


class DbInsert:

    @classmethod
    def _new_order(cls, model_instance, model_name, account_id, conn):

        rsp = conn.execute(
            usermodels.insert().values(
                accountid=account_id,
                modelinstance=model_instance,
                model=model_name
            )
        )

        assert rsp.rowcount == 1, 'Failed to insert new order.'

        return rsp

    @classmethod
    def new_order(cls, model_instance, model_name, account_id):
        rsp = cls._new_order(
            model_instance,
            model_name,
            account_id,
            conn=meta_general.bind)
        rsp.close()

    @classmethod
    def _new_param_data(
            cls,
            params_info: dict,
            model_instance,
            model_name,
            account_id,
            conn):

        insert_list = [{'paramname': itm,
                        'paramstring': v,
                        'accountid': account_id,
                        'modelinstance': model_instance,
                        'model': model_name} for itm, v in params_info.items()]

        rsp_ts = conn.execute(
            model_params.insert(),
            insert_list
        )

        assert rsp_ts.rowcount == len(
            insert_list), 'Failed to insert all params.'

        return rsp_ts

    @classmethod
    def new_param_data(
            cls,
            params_info: dict,
            model_instance,
            model_name,
            account_id):

        conn = model_params.bind.connect()
        # begin a transaction
        ts_bg = conn.begin()

        try:
            cls._new_param_data(
                params_info,
                model_instance,
                model_name,
                account_id,
                conn=conn)
            ts_bg.commit()

        except BaseException:
            # error, rollback insert
            ts_bg.rollback()
            traceback.print_exc()
        finally:
            conn.close()

    @classmethod
    def create_order(
            cls,
            model_instance,
            model_name,
            account_id,
            params_info: dict):

        # start a connection
        conn = meta_general.bind.connect()
        # begin a transaction
        ts_bg = conn.begin()

        try:
            # insert new order
            cls._new_order(model_instance, model_name, account_id, conn=conn)
            # insert model params data
            cls._new_param_data(
                params_info,
                model_instance,
                model_name,
                account_id,
                conn=conn)

            ts_bg.commit()
        except BaseException:
            # error, rollback insert
            ts_bg.rollback()
            traceback.print_exc()
        finally:
            conn.close()

    @classmethod
    def _new_order_record(
            cls,
            order_info: dict,
            account_id,
            model_instance,
            conn):
        order_i = dict(order_info)
        order_i['accountid'] = account_id
        order_i['modelinstance'] = model_instance

        rsp = conn.execute(
            order_record_otc.insert().values(
                **order_i
            )
        )

        assert rsp.rowcount == 1, 'Failed to insert new order record.'

        return rsp

    @classmethod
    def new_order_record(cls, order_info: dict, account_id, model_instance):

        rsp = cls._new_order_record(
            order_info,
            account_id,
            model_instance,
            conn=meta_localuser.bind)

        rsp.close()
