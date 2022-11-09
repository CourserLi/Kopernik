#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uncurl
import json
import re

class ConvertcURL(object):
    """
    用法：将 cURL 转换成 Python 代码 \n
    功能：可支持提取的参数如下：\n
    1. url / urls（不含参数 / 含参数）
    2. method（请求方法）
    3. headers（Json 格式）
    4. cookies（Json 格式）
    5. query（Json 格式）
    6. data（原装）
    """
    def __init__(self, cURL):
        self.__cURL = cURL
        self.convert()

    def convert(self):
        context = uncurl.parse_context(self.__cURL)
        self.__url = context.url
        self.__method = context.method
        self.__headers = context.headers
        self.__cookies = json.dumps(context.cookies, indent=4)
    
    def url(self):
        URL = self.__url
        url = URL.split('?')[0] if "?" in URL else URL
        return url

    def urls(self):
        return self.__url
    
    def method(self):
        return self.__method
    
    def headers(self):
        return json.dumps(self.__headers, indent=4)
    
    def cookies(self):
        return self.__cookies

    def query(self):
        URL = self.__url
        params = URL.split('?')[1] if "?" in URL else None
        if(params == None): return None
        Query = {}
        for item in params.split('&'):
            key, value = item.split('=')
            Query[key] = value
        return json.dumps(Query, indent=4)
    
    def data(self):
        try:
            result = re.search(r"--data-raw '(?P<data>.*?)'", self.__cURL)
            result.group('data')
        except Exception as e:
            return None
        else:
            return result.group('data')
    
    def include(self):
        pass

    def print(self):
        pass


"""
示例::

>>> cvCurl = ConvertcURL(cURL)

"""