#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import json
import cchardet
import jsbeautifier
sys.path.append("..")
from base.check import Check


# 二次封装 requests 类，便于操作
# 结合 socket ！！！


# 使引用文件使用 get 或者 'get' 效果一致
get, post, delete, put = 'get', 'post', 'delete', 'put'
GET, POST, DELETE, PUT = 'GET', 'POST', 'DELETE', 'PUT'

class Require(object):
    """
    Require 类的存在，意在更方便的使用 requests 类 ~(●'◡'●)~
    """
    # 限制实例输入的属性（暂时用不到，因为要传参 **kwargs）
    # __slots__ = ('url', 'method', 'cookies', 'headers', 'params', 'json', 'data')
    def __init__(self, url, method):
        """初始化参数自带 cookies 和 headers"""
        self.url = url
        self.method = method
        # self.cookies, self.headers, self.params, self.json, self.data = (None,) * 5

    def __str__(self):
        """Require 类的介绍"""
        return "Require 类的存在，意在更方便的使用 requests 类 ~(●'◡'●)~"
    __repr__ = __str__

    def __getattr__(self, attr):
        """如果找不到类中的属性，则返回 None，而非报错"""
        if attr not in ['url', 'method', 'cookies', 'headers', 'params', 'json', 'data', '']:
            return None
        raise AttributeError('\'Require\' object has no attribute \'%s\'' % attr)

    def require(self, **kwargs):
        """
        支持常用的请求方式：GET, POST, DELETE, PUT \n
        如果响应状态码为 200，返回 True，否则为 False
        """
        checker = Check()
        assert checker.isURL(self.url) == True
        URL, method = self.url, self.method.upper()
        params, json, data = (None,) * 3
        if(method == "GET"):
            params = self.params if hasattr(self, 'params') else None
            # try:
            #     if(params != None):
            #         assert checker.isJson(params) == True
            # except Exception as e:
            #     raise
        elif(method == "POST"):
            data = self.data if hasattr(self, 'data') else None
            json = self.json if hasattr(self, 'json') else None
            # try:
            #     if(data != None):
            #         assert checker.isJson(data) == True
            #     if(json != None):
            #         assert checker.isJson(json) == True
            # except Exception as e:
            #     raise
        elif(method == "PUT"):
            data = self.data if hasattr(self, 'data') else None
            # try:
            #     if(data != None):
            #         assert checker.isJson(data) == True
            # except Exception as e:
            #     raise
        elif(method == "DELETE"):
            pass
        else:
            return "错误提示: 传入 method 不符合规范"
        """
        # 直接在 require 函数中传入参数，正在 DEBUG
        items = {"params":[params], "json":[json], "data":[data]}
        for item in items.items():
            try:
                key, value = item[0], item[1][0]
                kwargs[key] # kwargs 传入了 key 参数
                assert kwargs[value] == None # 本身不存在 key 参数
            except KeyError as e:
                pass # 没有 key 参数
            except AssertionError as e:
                return "错误提示: 重复传入了 " + item[1] + " 参数"
            else:
                item[key][0] = kwargs[value]
                kwargs.pop(key)
        params, json, data = items['params'][0], items['json'][0], items['data'][0]
        print(params,json,data)
        """
        response = requests.request(method, URL, params=params, json=json, data=data, **kwargs)
        self.response = response
        return response.status_code == 200

    def info_1(self):
        """
        输出全部请求信息，包含：\n
        1. 请求头
        2. 载荷（请求参数）
        """
        if(hasattr(self, 'headers')):
            print("请求头:")
            print(self.headers, '\n')
        if(hasattr(self, 'cookies')):
            print("Cookies:")
            print(self.cookies, '\n')
        if(hasattr(self, 'params')):
            # print("载荷 params:\n" + jsbeautifier.beautify(self.params), '\n')
            print("载荷 params:\n", self.params, '\n')
        if(hasattr(self, 'json')):
            print("载荷 json:\n" + jsbeautifier.beautify(self.json), '\n')
        if(hasattr(self, 'data')):
            print("载荷 data:\n" + jsbeautifier.beautify(self.data), '\n')

    def info_2(self):
        """
        输出全部响应信息（前提是执行过 require 方法），包含：\n
        1. 响应码
        2. 响应头
        3. 响应内容
        """
        response = self.response
        encoding = cchardet.detect(response.content)['encoding']
        print("响应码:", response.status_code, '\n')
        print("响应头:")
        print(response.headers, '\n')
        content = response.content.decode(encoding)
        try:
            json.loads(content)
        except:
            print("响应内容:\n" + content)
            return
        print("响应 JSON:\n" + jsbeautifier.beautify(content))

    def info(self):
        """
        输出全部请求和响应信息（前提是执行过 require 方法），包含： \n
        1. 请求头
        2. 载荷（请求参数）
        3. 响应码
        4. 响应头
        5. 响应内容
        """
        self.info_1()
        self.info_2()

    def result(self):
        pass
        # 针对特定的响应文件打印 200，用继承类好了，加个 super


"""
示例::

>>> require = Require()

>>> require
Require 类的存在，意在更方便的使用 requests 类 ~(●'◡'●)~

>>> print(require.cookies)
# 打印默认的 cookies（类似的还有 headers 等）


>>> URL = "https://www.baidu.com"
>>> require = Require(URL, get)
>>> print(require.require())
True
>>> require.info_2()
响应码: 200 

响应头:
xxxxx

响应内容:
xxxxx


>>> URL = "https://www.baidu.com/sugrec"
>>> require = Require(URL, get)
>>> require.params = '{"tn":"48020221_4_hao_pg"}'
>>> require.cookies = info.cookies
>>> require.headers = info.headers
>>> require.require()
# 以上四行代码也可合为一行（但不建议这么做）:
# require.require()
>>> require.info_1()
请求头:
xxxxx

Cookies:
xxxxx

载荷 params:
{
    "tn": "48020221_4_hao_pg"
}
"""