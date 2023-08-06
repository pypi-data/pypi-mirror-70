# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import requests
from ..utils import Log

class Service:

    @classmethod
    def api(cls, url, params, headers, http_method):
        res = ""
        if http_method.upper() == "POST":
            try:
                res = requests.post(url, params, headers=headers)
                Log.info("正在发送POST请求")
            except Exception as e:
                Log.error("POST请求出现了异常：{0}".format(e))
        elif http_method.upper() == "GET":
            try:
                res = requests.get(url, params, headers=headers)
                Log.info("正在发送GET请求")
            except Exception as e:
                Log.error("GET请求出现了异常：{0}".format(e))

        Log.info("收到请求返回数据:")
        Log.info(res.json())

        return res