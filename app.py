# encoding=utf-8
from flask import Flask, request, jsonify
import jieba
import jieba.analyse
import sys
import os
import requests

sys.path.append('../')

app = Flask(__name__)

USER_DICT_LOADED = False


@app.route('/jieba')
def index():
    global USER_DICT_LOADED
    if request.method == 'POST':
        text = request.form.get('text')
    else:
        text = request.args.get('text')

    if False == USER_DICT_LOADED:
        jieba.load_userdict('dict/dict.txt.big')
        jieba.analyse.set_idf_path('dict/idf.txt.big')
        jieba.analyse.set_stop_words('dict/stop_words.txt')
        USER_DICT_LOADED = True

    seg_list = jieba.cut_for_search(text)
    keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            keywords.append(keyword)

    tags = []
    for x, w in jieba.analyse.textrank(text, withWeight=True):
        tags.append(x)

    return jsonify(keywords=keywords, tags=tags)


@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    r = requests.get(url)
    return r.text
