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
        title = request.form.get('title')
        desc = request.form.get('desc')
    else:
        title = request.args.get('title')
        desc = request.args.get('desc')

    if False == USER_DICT_LOADED:
        jieba.load_userdict('dict/dict.txt.big')
        jieba.load_userdict('dict/freq.dict')
        jieba.analyse.set_idf_path('dict/idf.txt.big')
        jieba.analyse.set_stop_words('dict/stop_words.txt')
        USER_DICT_LOADED = True

    seg_list = jieba.cut(title, cut_all=True)
    title_keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            title_keywords.append(keyword)

    seg_list = jieba.cut(desc, cut_all=True)
    desc_keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            desc_keywords.append(keyword)

    text = "%s %s" % (title, desc)
    textrank_tags = jieba.analyse.textrank(text)

    tfidf_tags = jieba.analyse.extract_tags(text, 20)

    return jsonify(
        title=title_keywords,
        desc=desc_keywords,
        textrank=textrank_tags,
        tfidf=tfidf_tags,
    )


@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    r = requests.get(url)
    return r.text
