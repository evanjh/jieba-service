# encoding=utf-8
import jieba
import jieba.analyse
import sys
import os

sys.path.append('../')


def index(text):

    jieba.load_userdict('dict/dict.txt.big')
    jieba.load_userdict('dict/freq.dict')
    # jieba.analyse.set_idf_path('dict/idf.txt.big')
    jieba.analyse.set_stop_words('dict/stop_words.txt')

    seg_list = jieba.cut(text, cut_all=True)
    keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            keywords.append(keyword)
    print(keywords)

    seg_list = jieba.cut_for_search(text)
    keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            keywords.append(keyword)
    print(keywords)
    tags = []
    for x, w in jieba.analyse.textrank(text, withWeight=True):
        tags.append(x)
    print(tags)


index('Cloudflare在中国Cloudflare在中国的用户（站长）交流群%20我们聊：关于站长/开发者资源（工具、脚本、源码）事件、网站防火墙/CDN/DNS等（攻略教程/使用优化）、DDoS防护、Cloudflare最新动态以及SuCloud宿云的有关话题')
