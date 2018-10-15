# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:08
# @Author  : Xin Zhang
# @File    : update_scripts.py

import warnings
from sqlalchemy.sql import and_
from rds_tools.models.tables import (meta_localuser,
                                     order_record_otc)


warnings.filterwarnings('ignore', category=Warning)


class DbUpdate:
    @classmethod
    def _order_record_otc(
            cls,
            change_item,
            change_value,
            account_id,
            model_instance,
            conn):

        resp = conn.execute(
            order_record_otc.update().where(
                and_(order_record_otc.c.accountid == account_id,
                     order_record_otc.c.modelinstance == model_instance)
            ).values(
                **{change_item: change_value}
            )
        )

        assert resp.rowcount == 1, 'Failed to update order_record_otc.'

        return resp

    @classmethod
    def order_record_otc(
            cls,
            change_item,
            change_value,
            account_id,
            model_instance):

        resp = cls._order_record_otc(
            change_item,
            change_value,
            account_id,
            model_instance,
            conn=meta_localuser.bind)
        resp.close()
