#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from base.database import Database

"""
PS：如果要查询用例步骤，用 database 类确实可以查，但建议使用 MongoDB 中文全文检索，速度会更快
"""

database = Database()

# 添加用例步骤进数据库（可添加多个）
# 1. 填写用例步骤参数 2. 填写对应用例分组 3. 最后记得添加索引
"""
steps = [{
    "desc": "切换至聚合模式",
    "method": "put",
    "uri": "/api/v2/mail_setting",
    "body": '{\n\t"general": {\n\t\t"browse_mode": 1\n\t}\n}'
}, {
    "desc": "切换至非聚合模式",
    "method": "put",
    "uri": "/api/v2/mail_setting",
    "body": '{\n\t"general": {\n\t\t"browse_mode": 2\n\t}\n}'
}]
database.insert('邮件多选', steps)
database.index('邮件多选')
"""

# 修改用例步骤（一步到位）
# 传入参数：用例名称 + 要改的变量 + 要改的值
"""
database.change('切换至聚合模式', 'method', 'get')
"""

# 批量修改用例
r"""
1. 命令行输入 mongoexport --collection=邮件多选 --db=邮件XX --out=C:\Users\WPS\Desktop\data.json
2. 批量修改 data.json 中的内容
3. 代码执行 database = Database() -> database.delete('邮件XX')
4. 命令行输入 mongoimport --collection=邮件多选 --db=邮件XX --file=C:\Users\WPS\Desktop\data.json
"""

# 删除用例分组（一步到位）
"""
database.delete('邮件多选')
"""


print("---------------------- 数据库交互 ----------------------")









