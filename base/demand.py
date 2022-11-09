#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
sys.path.append("..")
from base.info import *
from concurrent.futures import ThreadPoolExecutor

class Demand(object):
    """
    目前仅支持场景测试的一系列操作 \n
    用法：先查询所要操作用例的位置，再进行一系列操作 \n
    功能：支持的操作如下：\n
    1. 展示全部场景分组列表对应的 serviceid [需要手动记录]
    2. 查询目标场景用例所处的位置（支持模糊查询）
    3. 获取目标场景用例对应的 ID / 获取 ID 对应的场景用例
    4. 自动创建场景用例
    5. 删除用例分组下的全部场景用例
    """
    def __init__(self):
        self.name_serviceid = {
            "邮件查看": 3861,
            "邮件多选": 3847,
            "首页刷新": 3822,
            "邮件标签": 3818,
            "邮件聚合": 3798,
            "邮件搜索": 3794,
            "邮箱设置": 3745,
            "邮件文件夹操作": 3744,
            "邮件收发": 3742
        }

    def serviceid(self):
        # 显示全部用例分组及其子分组，暂时不需要
        # params = {'project_id': '753'}
        # response = requests.get('https://kepler.wps.cn/api/v1/mulapi/module/list', params=params, cookies=cookies, headers=headers)
        print("""
          用例分组 -> serviceid
        ----------------------
        |  webmail   |  3695  |
        ----------------------
        |  邮件查看  |  3861  |
        |  邮件多选  |  3847  |
        |  首页刷新  |  3822  |
        |  邮件标签  |  3818  |
        |  邮件聚合  |  3798  |
        |  邮件搜索  |  3794  |
        |  邮箱设置  |  3745  |
        |邮件文件夹操作| 3744 |
        |  邮件收发  |  3742  |
        ---------------------
        """)

    def serach(self):
        pass

    def get(self, target, serviceid=None):
        """
        1. 如果 target 传入 ID 则返回用例名
        2. 如果 target 传入用例名则返回对应 ID
        3. 当传入用例名，同时传入用例所在组（serviceid）时，速度会更快
        """
        if(str(target).isdigit()):
            response = requests.get(f'https://kepler.wps.cn/api/v1/mulapi/{target}/info', cookies=cookies, headers=headers)
            return response.json()['data']['description']
        else:
            if(serviceid != None):
                params = {
                    'teamid': teamid,
                    'projectid': project_id,
                    'serviceid': serviceid,
                    'type': 'service',
                    'offset': '0',
                    'limit': '1000',
                }
                response = requests.get('https://kepler.wps.cn/api/v1/autolist', params=params, cookies=cookies, headers=headers)
                total = int(response.json()['data']['total'])
                for i in range(total):
                    if(response.json()['data']['data'][i]['description'] == target):
                        return response.json()['data']['data'][i]['id']
                return None
            else:
                for serviceid in [3695, 3861, 3847, 3822, 3818, 3798, 3794, 3745, 3744, 3743, 3742]:
                    params = {
                        'teamid': teamid,
                        'projectid': project_id,
                        'serviceid': serviceid,
                        'type': 'service',
                        'offset': '0',
                        'limit': '1000',
                    }
                    response = requests.get('https://kepler.wps.cn/api/v1/autolist', params=params, cookies=cookies, headers=headers)
                    total = int(response.json()['data']['total'])
                    for i in range(total):
                        if(response.json()['data']['data'][i]['description'] == target):
                            return response.json()['data']['data'][i]['id']
                return None

    def create(self, name, serviceid=None):
        json_data = {
            'priority': 'P0',
            'testType': 'API',
            'testGroup': [
                "3695",
                str(serviceid),
            ],
            'description': name,
            'apidatas': [],
            'projectid': project_id,
            'serviceid': serviceid,
            'steps': [],
            'teamid': teamid,
        }
        response = requests.post('https://kepler.wps.cn/api/v1/mulapi', cookies=cookies, headers=headers, json=json_data)
        return response.json()['data']['id']
    
    def delete(self, name):
        serviceid = self.name_serviceid[name]
        params = {
            'teamid': teamid,
            'projectid': project_id,
            'serviceid': serviceid,
            'type': 'service',
            'offset': '0',
            'limit': '1000',
        }
        response = requests.get('https://kepler.wps.cn/api/v1/autolist', params=params, cookies=cookies, headers=headers)
        total = int(response.json()['data']['total'])
        with ThreadPoolExecutor(16) as t:
            def response_delete(id, params, cookies, headers, title):
                response = requests.delete('https://kepler.wps.cn/api/v1/mulapi/' + str(id), params=params, cookies=cookies, headers=headers)
                if(response.json()['result'] == "ok"): print("成功删除“" + title + "”用例")
            for i in range(total):
                id = response.json()['data']['data'][i]['id']
                title = response.json()['data']['data'][i]['description']
                params = {
                    'id': id,
                    'teamid': teamid,
                    'projectid': project_id,
                    'serviceid': serviceid,
                }
                t.submit(response_delete, id, params, cookies, headers, title)
        print("“" + name + "”的全部用例删除成功！！")


"""
# 目前仅适配于 Email 邮箱项目!!
示例::

>>> demand = Demand()

>>> demand.serviceid()
    用例分组 -> serviceid
    ----------------------
    |  webmail   |  3695  |
    ----------------------
    |  邮件多选  |  3847  |
    |  首页刷新  |  3822  |
    |  邮件标签  |  3818  |
    |  邮件聚合  |  3798  |
    |  邮件搜索  |  3794  |
    |  邮箱设置  |  3745  |
    |邮件文件夹操作| 3744 |
    |  邮件收发  |  3742  |
    |  文件操作  |  3696  |
    ---------------------

# 获取 ID 对应的场景用例
>>> name = demand.get(45760)
>>> print(name)
test

# 获取目标场景用例对应的 ID
>>> id = demand.get("test")
>>> print(id)
45760

# 获取目标场景用例对应的 ID（更速度快）
>>> id = demand.get("test", 3847)
>>> print(id)
45760

# 在用例组：邮件多选中（serviceid 为 3847）自动创建场景用例，并接收用例的 ID
>>> id = demand.create("新用例", 3847)
>>> print(id)
45800

# 删除用例分组下的全部用例
>>> demand.delete("邮件多选")
成功删除“收件箱-非聚合模式-批量标记星标”用例
“邮件多选”的全部用例删除成功！！
"""