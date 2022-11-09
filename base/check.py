#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

class Check(object):
    """
    用法：判断所需的参数是否合乎规范
    功能：支持 JSON, URL 判断
    """
    def __init__(self):
        """传递的参数本质都是字符串，判断函数返回布尔类型"""
    def isURL(self, URL):
        """判断 URL 是否规范"""
        try:
            result = re.search(r"(https|http)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", URL)
            testURL = result.group()
            assert testURL == URL
        except:
            raise AssertionError("错误提示: 传入 URL 不符合规范")
        else:
            return True
    def isJson(self, JSON):
        """判断 JSON 是否规范"""
        try:
            json.loads(JSON)
        except Exception as e:
            print("错误提示: 传入 JSON 不符合规范")
            return e
        return True


"""
示例::

>>> checker = Check()

>>> URL = "https://baidu.com"
>>> print(checker.isURL(URL))
True

>>> JSON = '{"a":123, "b":"456"}'
>>> print(checker.isJson(JSON))
True

"""