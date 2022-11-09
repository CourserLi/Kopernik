#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import os
import json
import time
import requests
from base.info import *
from base.database import Database
from base.mulapi import Mulapi
from base.demand import Demand
from concurrent.futures import ThreadPoolExecutor

"""
1. 维护用例步骤（数据库）-> 迭代用例步骤(name)
2. 维护场景用例（开普勒）-> 迭代场景用例(name)
3. 一键全部迭代 -> 迭代全部表单()
4. 一键调成 md 或 csv 格式 -> 未开发
"""

def 迭代用例步骤(name):
    collection = name
    # 读取用例步骤文件，做为新的集合
    f = open('.\\processing\\用例步骤\\'+ collection +'.txt', 'r', encoding='utf-8', errors='ignore')
    steps = []
    tmp_json = {}
    for line in f.readlines():
        tmp = line.strip()
        # print(tmp) # 把末尾的'\n'删掉
        if(tmp == "" and tmp_json != {}):
            steps.append(tmp_json)
            # print(tmp_json) # 打印 tmp_json
            tmp_json = {}
        elif(tmp[:4] == "####"): continue
        # 功能步骤（延迟步骤）
        elif(tmp[:4] == "dela"):
            split_list = tmp.split(" = ")
            delay = str(split_list[1])
            tmp_json.update({"delay": delay})
        elif(tmp[:4] == "desc"):
            split_list = tmp.split("'")
            desc, method, uri = split_list[1], split_list[3], split_list[5]
            tmp_json.update({"desc": desc})
            tmp_json.update({"method": method})
            tmp_json.update({"uri": uri})
        else:
            split_list = tmp.split(" = ")
            if(split_list[0] == ""): break
            if(split_list[0] == "body"):
                tmp_json.update({"body": tmp[8:-1].replace("\\n",'\n').replace("\\t",'\t').replace('\\\\"','\\\"').replace('\\"','\"')}) # 真复杂，浪费我半个小时
            else:
                tmp_json.update({split_list[0]: json.loads(split_list[1])})
    f.close()
    if(tmp_json != {}): steps.append(tmp_json)
    # print(steps) # 打印 steps
    # 删除已有数据库集合
    database = Database()
    database.delete(collection)
    # 迭代集合进数据库，并迭代索引
    database.insert(collection, steps)
    database.index(collection)

def 迭代场景用例(name):
    demand = Demand()
    database = Database()
    def establish(serviceid, name, steps):
        ID = demand.create("新用例", serviceid)
        # 用例名字（收件箱-非聚合模式-批量标记星标）
        name = name
        # 全部步骤用例（切换至非聚合模式-发送一封邮件至收件箱-发送一封邮件至收件箱-刷新收件箱-获取收件箱列表（确保共两封邮件，获取前两封邮件 id）-批量星标（前两封邮件打星标）-获取收件箱列表（确保共两封邮件都已标记星标）-清空收件箱）
        steps = steps
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
        if(response.json()['result'] == "ok"): print("成功创建“" + name + "”用例")

    collection = name
    f = open('.\\processing\\场景用例\\'+ collection +'.txt', 'r', encoding='utf-8', errors='ignore')
    name_list = []
    steps_list = []
    for line in f.readlines():
        tmp = line.strip()
        # print(tmp) # 把末尾的'\n'删掉
        if(tmp[:4] == "####"):
            name_list.append(tmp[5:])
        elif(tmp == ""): continue
        else:
            # 数据库搜索，搜不到则报错
            steps = tmp.split('-')
            for step in steps:
                result = database.find(step)
                if(result == None):
                    print("数据库中没有该步骤用例：" + step)
                    return
            steps_list.append(tmp)
    f.close()
    # print(name_list) # 打印 name_list
    # print(steps_list) # 打印 steps_list
    # 开普勒删除用例分组
    demand.delete(name)
    # 重新上传迭代用例
    with ThreadPoolExecutor(16) as t:
        for i in range(len(name_list)):
            serviceid = demand.name_serviceid[collection]
            name = name_list[i]
            steps = steps_list[i]
            t.submit(establish, serviceid, name, steps)
    print("“" + collection + "”的全部用例创建成功！！")

def 迭代全部表单():
    start = time.time()
    filename = [x for x in os.listdir('.\\processing\\用例步骤') if os.path.splitext(x)[1] == '.txt']
    for file in filename:
        file = file[:-4]
        # print(file)
        迭代用例步骤(file)
    filename = [x for x in os.listdir('.\\processing\\场景用例') if os.path.splitext(x)[1] == '.txt']
    for file in filename:
        file = file[:-4]
        # print(file)
        迭代场景用例(file)
    end = time.time()
    print("全部表单迭代成功，用时 " + str(end-start) + " 秒！！")


print("---------------------- 场景用例 ----------------------")


# 迭代全部表单()
# 迭代用例步骤("邮件多选")
# 迭代场景用例("邮件多选")

if __name__ == '__main__':
    迭代全部表单()



