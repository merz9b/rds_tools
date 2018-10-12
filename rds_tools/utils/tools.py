#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 10:14
# @Author  : John
# @File    : tools.py


import requests
import json


def get_public_ip():
    rsp = requests.get('http://pv.sohu.com/cityjson')
    r_j = json.loads(rsp.text.lstrip('var returnCitySN = ').rstrip(';'))
    return r_j['cip']
