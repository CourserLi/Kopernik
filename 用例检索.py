#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
# import paddle
from pymongo import MongoClient
from flask import Flask, request, render_template

# paddle.enable_static()

client = MongoClient('localhost', 27017)
db = client["邮件"]

def bigram_tokenize(word): # 如果使用 paddle 模式，需要使用 anaconda 下载 paddle
    words = ""
    # jieba.enable_paddle()
    strs=[word]
    for str in strs:
        seg_list = jieba.cut(str,use_paddle=False) # use_paddle=True
        words += ' '.join(list(seg_list))
    return words

def match(step):
    desc, method, uri = step["desc"], step["method"], step["uri"]
    body = step["body"] if ("body" in step) else "None"
    params = step["params_dict"] if ("params_dict" in step) else "None"
    extracts = step["extracts_dict"] if ("extracts_dict" in step) else "None"
    validations = step["validations_dict"] if ("validations_dict" in step) else "None"
    delay = step["delay"] if ("delay" in step) else "None"
    return [desc, method, uri, body, params, extracts, validations, delay]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test_form():
    return render_template('test.html')

@app.route('/', methods=['POST'])
def test():
    desc = request.form['desc']
    posts = []
    colls = db.list_collection_names()
    for coll in colls:
        collection = db[coll]
        for items in collection.find({'$text': {'$search': f'"{bigram_tokenize(desc)}"'}}):
            item = match(items)
            post = []
            post.append("desc: " + item[0])
            post.append("method: " + item[1])
            post.append("uri: " + item[2])
            post.append("body: " + item[3])
            post.append("params: " + str(item[4]))
            post.append("extracts: " + str(item[5]))
            post.append("validations: " + str(item[6]))
            post.append("delay: " + str(item[7]))
            posts.append(post)
    return render_template('test.html', posts=posts)

if __name__ == '__main__':
    app.run()


