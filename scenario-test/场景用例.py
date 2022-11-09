#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import requests
from base.info import *
from base.database import Database
from base.mulapi import Mulapi
from base.demand import Demand

demand = Demand()

# 查看用例分组对应的 serviceid（一步到位）
"""
demand.serviceid()
"""

# 查看 ID 对应的场景用例（一步到位）
"""
name = demand.get(45760)
print(name)
"""

# 查看目标场景用例对应的 ID（一步到位）
"""
id = demand.get("目标用例")
print(id)
"""

# 自动创建场景用例
# 1. 查看用例分组对应的 serviceid 2. 获得创建用例的 ID
"""
id = demand.create("新用例", 3847)
print(id)
"""

# 新建场景用例
# 1. 查看用例分组对应的 serviceid 2. 自动创建场景用例并获得 ID 3. 填写用例名字和全部步骤用例
"""
def establish(serviceid, name, steps):
    ID = demand.create("新用例", serviceid)
    # 用例名字（收件箱-非聚合模式-批量标记星标）
    name = name
    # 全部步骤用例（切换至非聚合模式-发送一封邮件至收件箱-发送一封邮件至收件箱-刷新收件箱-获取收件箱列表（确保共两封邮件，获取前两封邮件 id）-批量星标（前两封邮件打星标）-获取收件箱列表（确保共两封邮件都已标记星标）-清空收件箱）
    steps = steps
    database = Database()
    mulapi = Mulapi(name, ID, teamid, project_id, serviceid)
    steps = steps.split('-')
    step_list = []
    for step_name in steps:
        step = mulapi.match(database.find(step_name))
        # 步骤累加
        step_list.append(step)
    json_data = mulapi.complete(step_list)
    response = requests.put(f'https://kepler.wps.cn/api/v1/mulapi/{ID}', cookies=cookies, headers=headers, json=json_data)
    # 返回结果
    print(response.json())

demand.serviceid()
serviceid = None
name = None
steps = None
establish(serviceid, name, steps)
"""

# 修改场景用例
# 1. 查看用例分组对应的 serviceid 2. 查看目标场景用例对应的 ID 3. 填写用例名字和全部步骤用例
"""
def change(serviceid, ID, name, steps):
    ID = ID
    # 用例名字（收件箱-非聚合模式-批量标记星标）
    name = name
    # 全部步骤用例（切换至非聚合模式-发送一封邮件至收件箱-发送一封邮件至收件箱-刷新收件箱-获取收件箱列表（确保共两封邮件，获取前两封邮件 id）-批量星标（前两封邮件打星标）-获取收件箱列表（确保共两封邮件都已标记星标）-清空收件箱）
    steps = steps
    database = Database()
    mulapi = Mulapi(name, ID, teamid, project_id, serviceid)
    steps = steps.split('-')
    step_list = []
    for step_name in steps:
        step = mulapi.match(database.find(step_name))
        # 步骤累加
        step_list.append(step)
    json_data = mulapi.complete(step_list)
    response = requests.put(f'https://kepler.wps.cn/api/v1/mulapi/{ID}', cookies=cookies, headers=headers, json=json_data)
    # 返回结果
    print(response.json())

demand.serviceid()
serviceid = None
ID = None
name = None
steps = None
change(serviceid, name, steps)
"""


print("---------------------- 场景用例 ----------------------")








