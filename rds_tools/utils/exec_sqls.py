#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:58
# @Author  : John
# @File    : exec_sqls.py


import pandas as pd
from sqlalchemy.sql import select,and_

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


def insert_into_db(table, list_of_content):
    feedback = table.bind.execute(
        table.insert(),
        list_of_content
    )
    return feedback
