# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 10:00
# @Author  : Xin Zhang
# @File    : __init__.py.py

from .select import DbSelect
from .insert import DbInsert


class FuturexDB:
    select = DbSelect
    insert = DbInsert
