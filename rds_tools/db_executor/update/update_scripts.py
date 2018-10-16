# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:08
# @Author  : Xin Zhang
# @File    : update_scripts.py

import warnings
import traceback
from sqlalchemy.sql import and_
from rds_tools.models.tables import (meta_localuser, meta_general,
                                     order_record_otc, model_params)
warnings.filterwarnings('ignore', category=Warning)


class DbUpdate:
    @classmethod
    def _order_record_otc(
            cls,
            change_item,
            change_value,
            model_instance,
            conn):

        resp = conn.execute(
            order_record_otc.update().where(
                order_record_otc.c.modelinstance == model_instance)
            .values(
                **{change_item: change_value}
            ))

        assert resp.rowcount == 1, 'Failed to update order_record_otc.'

        return resp

    @classmethod
    def order_record_otc(
            cls,
            change_item,
            change_value,
            model_instance):

        resp = cls._order_record_otc(
            change_item,
            change_value,
            model_instance,
            conn=meta_localuser.bind)
        resp.close()

    @classmethod
    def _model_params(
            cls,
            change_item,
            change_value,
            exchange_,
            index_,
            days_,
            account_id,
            conn):

        assert all([exchange_ is not None, index_ is not None, days_ is not None]
                   ), 'Param exchange, index and days should not be empty.'

        model_instance = '-'.join([exchange_, index_, days_])

        resp = conn.execute(
            model_params.update().where(
                and_(
                    model_params.c.accountid == account_id,
                    model_params.c.modelinstance == model_instance,
                    model_params.c.paramname == change_item
                )
            ).values(paramvalue=change_value)
        )

        assert resp.rowcount == 1, 'Failed to update model_params.'

        return resp

    @classmethod
    def model_params(
            cls,
            change_item,
            change_value,
            exchange_,
            index_,
            days_,
            account_id=20):
        conn = meta_general.bind.connect()
        # begin a transaction
        ts_bg = conn.begin()
        try:
            cls._model_params(change_item=change_item,
                              change_value=change_value,
                              exchange_=exchange_,
                              index_=index_,
                              days_=days_,
                              account_id=account_id,
                              conn=conn
                              )
            ts_bg.commit()
        except BaseException:
            # error, rollback insert
            ts_bg.rollback()
            traceback.print_exc()
        finally:
            conn.close()
