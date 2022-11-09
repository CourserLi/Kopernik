#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Mulapi(object):
    """
    开普勒 Kepler 专用场景用例的步骤类 \n
    用法：先传入场景用例的环境参数，再填入需要的步骤参数 \n
    功能：支持填入的步骤参数如下：\n
    1. 待测试 api 的主体信息（描述 / 请求方法 / 请求路径）
    2. 请求体（raw - JSON）
    3. Query（key - value）
    4. 参数提取（默认提取响应体）
    5. 校验方式（默认是 JSON 匹配）
    """
    def __init__(self, description, id, teamid, projectid, serviceid):
        self.json_data = {
            'description': description,
            'id': id,
            'teamid': teamid,
            'projectid': projectid,
            'serviceid': serviceid,
            'testType': 'API',
            'version': None,
            'apidatas': [],
        }
    
    def match(self, step):
        """
        接收 step 字典，返回适配此类的字典
        """
        desc, method, uri = step["desc"], step["method"], step["uri"]
        body = step["body"] if ("body" in step) else ""
        params = self.add_param(step["params_dict"]) if ("params_dict" in step) else []
        extracts = self.add_extract(step["extracts_dict"]) if ("extracts_dict" in step) else []
        validations = self.add_validate(step["validations_dict"]) if ("validations_dict" in step) else None
        delay = step["delay"] if ("delay" in step) else None
        mathc_step = self.add_step(desc, method, uri, params=params, body=body, extracts=extracts, validations=validations, delay=delay)
        return mathc_step
    
    def complete(self, step_list):
        steps = {'steps': step_list}
        json_data = self.json_data
        json_data.update(steps)
        return json_data

    def add_param(self, params_dict):
        params = []
        for key, value in params_dict.items():
            param = {
                'key': key,
                'value': value,
                'valueType': 'String',
                'desc': '',
                'name': key,
                'enabled': True,
            }
            params.append(param)
        # 返回 param 列表
        return params
    
    def add_extract(self, extracts_dict):
        extracts = []
        for key, value in extracts_dict.items():
            extract = {
                'name': key,
                'key': '',
                'valueType': 'body',
                'value': value,
                'desc': '',
            }
            extracts.append(extract)
        # 返回 extracts 列表
        return extracts

    def add_validate(self, validations_dict):
        validations = [
            {
                'valueType': 'HTTP_CODE',
                'disableKeyInput': True,
                'value': 200,
                'key': '',
                'name': '',
            }
        ]
        for key, value in validations_dict.items():
            validation = {
                'valueType': 'JSON',
                'name': key,
                'key': '',
                'value': value,
            }
            validations.append(validation)
        # 返回 validations 列表
        return validations

    def add_step(self, desc, method, uri, params=[], body='', extracts=[], validations=None, delay=None):
        step = {
            'wsapi': None,
            'extends': None,
            'type': 'api',
            'delay': None,
            'priority': 1,
            'enabled': True,
            'is_executed': False,
            'parent': None,
            'steps': []
        }
        # 如果是功能步骤，则不需要 api，更改 step
        if(delay != None):
            step["type"] = "delay"
            step["delay"] = int(delay)
            step["extends"] = {}
            step.pop("wsapi")
            step.pop("priority")
            step.pop("is_executed")
            pass
        else:
            api = {
                'httpType': 'https',
                'host': 'email.wps.cn',
                'headers': [
                    {
                        'key': 'content-type',
                        'value': '${content-type_a}',
                        'desc': '',
                        'enabled': True,
                        'name': 'content-type',
                        'valueType': 'String',
                    },
                    {
                        'key': 'cookie',
                        'value': '${cookie}',
                        'desc': '',
                        'enabled': True,
                        'name': 'cookie',
                        'valueType': 'String',
                    },
                    {
                        'key': 'referer',
                        'value': '${referer}',
                        'desc': '',
                        'enabled': True,
                        'name': 'referer',
                        'valueType': 'String',
                    },
                    {
                        'key': 'origin',
                        'value': '${origin}',
                        'desc': '',
                        'enabled': True,
                        'name': 'origin',
                        'valueType': 'String',
                    },
                    {
                        'key': 'x-csrftoken',
                        'value': '${x-csrftoken}',
                        'desc': '',
                        'enabled': True,
                        'name': 'x-csrftoken',
                        'valueType': 'String',
                    },
                ],
                'rest': [],
                'validations': [
                    {
                        'valueType': 'HTTP_CODE',
                        'disableKeyInput': True,
                        'value': 200,
                        'key': '',
                        'name': '',
                    },
                ],
                'cookies': '',
                'timeout': 10,
                'sign': 'NO',
                'ak': '',
                'retry': 10,
                'pre_code': '',
                'post_code': '',
                'checkcode': 200,
                'checkvalue': '',
                'checkkey': '',
                'id': 10000,
                'retry_interval': 3,
                'yapi': None,
                'mulapi': None,
            }
            # 更新 api 中的键值对
            method = {'method': method}
            uri = {'uri': uri}
            bodyType = {'bodyType': 'JSON'} if body != '' else {'bodyType': 'none'}
            body = {'body': body}
            params = {'params': params}
            extracts = {'outputParams': extracts}
            api.update(method)
            api.update(uri)
            api.update(bodyType)
            api.update(body)
            api.update(params)
            api.update(extracts)
            if(validations != None):
                del api['validations']
                validations = {'validations': validations}
                api.update(validations)
            api = {'api': api}
            step.update(api)
        # 更新 step 中的键值对
        desc = {'desc': desc}
        step.update(desc)
        # 返回 step 字典
        return step


"""
# 目前仅适配于 Email 邮箱项目!!
示例::

# 场景用例环境参数
>>> description, id, teamid, projectid, serviceid = 'test', 45760, 352, 753, 3847
>>> mulapi = Mulapi(description, id, teamid, projectid, serviceid)

# 申请单个步骤，并初始化环境参数
>>> desc, method, uri = ['刷新邮件', 'get', '/api/v1/mail/refresh']

# 传入步骤参数 -- 请求体
>>> body = '{\n\t"draft_mbox": "草稿箱",\n\t"mail_id": "${mail_id}",\n\t"from": "${from}",\n\t"to": "${to}",\n\t"subject": "WPS金山666"\n}'

# 传入步骤参数 -- Query
>>> params_dict = {'mail_id': '1438', 'mbox': 'INBOX'}
>>> params = mulapi.add_param(params_dict)

# 传入步骤参数 -- 参数提取
>>> extracts_dict = {'result': '$.result'}
>>> extracts = mulapi.add_extract(extracts_dict)

# 传入步骤参数 -- 校验方式
>>> validations_dict = {'$.result': 'ok'}
>>> validations = mulapi.add_validate(validations_dict)

# 获得单个步骤
>>> step = mulapi.add_step(desc, method, uri, params=params, body=body, extracts=extracts, validations=validations)

# 步骤累加
>>> step_list = [step, step]

# 获得场景用例的全部信息
>>> json_data = mulapi.complete(step_list)
>>> print(json_data)
{'description': 'new', 'id': 45760, 'teamid': 352, 'projectid': 753, ......, 'desc': '刷新邮件'}]}

# 更新目标场景用例
>>> response = requests.put(f'https://kepler.wps.cn/api/v1/mulapi/{id}', cookies=cookies, headers=headers, json=json_data)
>>> print(response.json())
{'result': 'ok', 'data': None, 'msg': None}
"""