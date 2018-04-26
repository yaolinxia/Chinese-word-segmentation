from flask import Flask
from flask import render_template
from flask import request
import segmenter
import jieba
import test
import util
import thulac
import numpy as np
import mysql_db as mysql

app = Flask(__name__)

keywords = util.load_keyword("file/keyword.txt")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit',methods=['POST'])
def submit():
    text = request.form.get('text')
    thu_segmenter = thulac.thulac(seg_only=True)

    thu_list = thu_segmenter.cut(text)
    thu_array = np.array(thu_list)
    seg_list,keyword = segmenter.segment(text,keywords)
    jieba_list = jieba.cut(text)

    seg_result = "/".join(seg_list)
    jieba_result = "/".join(jieba_list)
    thu_result = "/".join(thu_array[:,0])


    jieba_similarity,jieba_result = test.similarity(seg_list,jieba_result.split("/"))
    thulac_similarity,thu_result = test.similarity(seg_list,thu_result.split("/"))
    jieba_similarity = util.float2percentage(jieba_similarity)
    thulac_similarity = util.float2percentage(thulac_similarity)

    keyword = list(keyword.keys())

    return render_template("submit.html",seg=seg_list,jieba=jieba_result,thulac=thu_result,jieba_similarity=jieba_similarity,thulac_similarity=thulac_similarity,keyword_first = keyword[0:10],keyword_second=keyword[10:20])

@app.route('/doc',methods=['POST'])
def get_doc():
    return mysql.get_random_doc()


if __name__ == '__main__':
    app.run()
