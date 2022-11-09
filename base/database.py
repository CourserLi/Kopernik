#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import jieba
# import paddle
import pprint

# paddle.enable_static()

class Database(object):
    """
    与 MongoDB 数据库交互的类，能够实现将所需数据增删改查进数据库中\n
    数据库包含数据，介绍如下：\n
    - 项目名（数据库）- 用例分组（集合）- 用例步骤（文档）
    - 每个数据库代表了不同的项目（如邮件）
    - 每个集合代表了不同的用例分组（如邮件多选）
    - 每个文档代表了不同的场景用例（如切换至聚合模式）\n
    功能：支持的操作如下：\n
    1. 插入用例步骤
    2. 查看 / 获取用例步骤
    3. 修改用例步骤
    4. 删除用例分组
    5. 查看批量修改用例步骤的教程
    6. 构建中文分词索引
    """
    def __init__(self, database='邮件'):
        client = MongoClient('localhost', 27017)
        self.db = client[database]
    
    def insert(self, group, steps):
        """
        在一个用例分组中，插入一个或多个用例步骤 \n
        传入参数：用例分组（集合）+ 用例步骤（文档）\n
        输出：是否插入成功
        PS：传入用例步骤的格式是列表，列表中至少包含一个字典
        """
        collection = self.db[group]
        result = collection.insert_many(steps)
        nums = result.inserted_ids
        if(len(nums) == len(steps)):
            print("成功插入")
        else:
            print("插入失败")
    
    def find(self, name):
        """
        获取用例步骤的全部信息
        传入参数：用例名称
        输出：参数 JSON 值
        """
        colls = self.db.list_collection_names()
        for coll in colls:
            collection = self.db[coll]
            items = collection.find_one({"desc": name})
            if(items != None):
                # 打印参数 JSON 值
                # pprint.pprint(collection.find_one({"desc": name}))
                # 返回参数 JSON 值
                return items
    
    def change(self, name, value, value_new):
        """
        修改用例步骤的某个变量值
        传入参数：用例名称 + 要改的变量 + 要改的值
        输出：打印更改后的结果
        PS：如果是批量修改，推荐使用 mongoexport、mongoimport 命令进行批量处理（导出 + 导入）
        """
        colls = self.db.list_collection_names()
        for coll in colls:
            collection = self.db[coll]
            items = collection.find_one({"desc": name})
            if(items != None):
                myquery = { "desc": name }
                newvalues = { "$set": { value : value_new } }
                x = collection.update_many(myquery, newvalues) 
                print("用例步骤修改成功，结果如下：")
                pprint.pprint(collection.find_one({"desc": name}))
                return
    
    def delete(self, group):
        """
        删除用例分组
        传入参数：用例分组（集合）
        输出：是否删除成功
        PS：此功能一般与批量修改用例步骤（文档）联用，先导出集合，批量修改后，删除数据库中原有的集合，最后导入集合
        """
        collection = self.db[group]
        collection.drop()
        if(group not in self.db.list_collection_names()):
            print("成功删除")
        else:
            print("删除失败")

    def batch(self):
        """
        批量修改用例步骤的教程
        """
        print(r"""
        1. 命令行输入 mongoexport --collection=邮件多选 --db=邮件XX --out=C:\Users\WPS\Desktop\data.json
        2. 批量修改 data.json 中的内容
        3. 代码执行 database = Database() -> database.delete('邮件XX')
        4. 命令行输入 mongoimport --collection=邮件多选 --db=邮件XX --file=C:\Users\WPS\Desktop\data.json
        """)
    
    def index(self, group):
        """
        构建中文分词索引
        传入参数：用例分组（集合）
        输出：打印更改后的一条结果
        """
        collection = self.db[group]
        def bigram_tokenize(word): # 如果使用 paddle 模式，需要使用 anaconda 下载 paddle
            words = ""
            # jieba.enable_paddle()
            strs=[word]
            for str in strs:
                seg_list = jieba.cut(str,use_paddle=False) # use_paddle=True
                words += ' '.join(list(seg_list))
            return words
        # 在 _t 字段建立全文索引
        collection.create_index([('_t', 'text')])
        # 在 _t 字段储存 desc 的全部二元分词
        for item in collection.find():
            collection.update_one({'_id': item['_id']}, {'$set': {'_t': bigram_tokenize(item['desc'])}})
        pprint.pprint(collection.find_one())


r"""
示例::

# 连接 MongoDB 数据库，不带参数，默认连接邮件数据库
>>> database = Database()

# 插入用例步骤
>>> steps = [{
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
>>> database.insert('邮件多选', steps)
成功插入

# 查询用例步骤
>>> step = database.find('切换至聚合模式')
>>> print(step)
{'_id': ObjectId('630c89ab78fc94748d97ef00'), 'desc': '切换至聚合模式', 'method': 'put', 'uri': '/api/v2/mail_setting', 'body': '{\n\t"general": {\n\t\t"browse_mode": 1\n\t}\n}'}

# 修改用例步骤
>>> database.change('切换至聚合模式', 'method', 'get')
用例步骤修改成功，结果如下：
{'_id': ObjectId('630c89ab78fc94748d97ef00'),
 'body': '{\n\t"general": {\n\t\t"browse_mode": 1\n\t}\n}',
 'desc': '切换至聚合模式',
 'method': 'get',
 'uri': '/api/v2/mail_setting'}

# 删除用例分组
>>> database.delete('邮件多选')
成功删除

# 查看批量修改用例步骤的教程
>>> database.batch()
1. 命令行输入 mongoexport --collection=邮件多选 --db=邮件XX --out=C:\Users\WPS\Desktop\data.json
2. 批量修改 data.json 中的内容
3. 代码执行 database = Database() -> database.delete('邮件XX')
4. 命令行输入 mongoimport --collection=邮件多选 --db=邮件XX --file=C:\Users\WPS\Desktop\data.json

# 构建中文分词索引
>>> database = Database()
>>> database.index('邮件多选')
{'_id': ObjectId('630d708529bd493430410366'),
 '_t': '切换 至 聚合 模式',
 'body': '{\n\t"general": {\n\t\t"browse_mode": 1\n\t}\n}',
 'desc': '切换至聚合模式',
 'method': 'put',
 'uri': '/api/v2/mail_setting'}
"""