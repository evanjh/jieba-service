# encoding=utf-8
from flask import Flask, request, jsonify
import jieba
import jieba.analyse
import sys

sys.path.append('../')

app = Flask(__name__)

jieba.load_userdict('dict/dict.txt.big')
jieba.analyse.set_idf_path('dict/idf.txt.big')
jieba.analyse.set_stop_words('dict/stop_words.txt')


@app.route('/')
def index():
    if request.method == 'POST':
        text = request.form.get('text')
    else:
        text = request.args.get('text')

    seg_list = jieba.cut_for_search(text)
    keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            keywords.append(keyword)

    tags = []
    for x, w in jieba.analyse.textrank(text, withWeight=True):
        tags.append(x)

    return jsonify(keywords=keywords, tags=tags)
