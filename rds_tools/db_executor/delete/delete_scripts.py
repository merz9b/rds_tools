# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:08
# @Author  : Xin Zhang
# @File    : delete_scripts.py

import warnings
from sqlalchemy.sql import and_
from rds_tools.models.tables import (usermodels)


warnings.filterwarnings('ignore', category=Warning)


class DbDelete:
    @classmethod
    def del_order(cls, model_name, model_instance, account_id):
        resp = usermodels.bind.execute(
            usermodels.delete().where(
                and_(usermodels.c.model == model_name,
                     usermodels.c.modelinstance == model_instance,
                     usermodels.c.accountid == account_id)
            )
        )
        resp.close()
        return resp.rowcount
