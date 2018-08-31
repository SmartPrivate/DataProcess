import logging
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import DBConnector, DataModel
import numpy as np
import xlwt
import math
import redis
import ZhihuProcess

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def load_data():
    models = DBConnector.query_all(DataModel.WeiboCut)
    word_cut_list = []
    for model in models:
        word_cut = model.word_cut.replace('\t', ' ')
        word_cut_list.append(word_cut)
    return word_cut_list


def calculate_tf_idf():
    # 读取数据
    word_cut_list = load_data()
    print('已载入{0}条数据。'.format(str(len(word_cut_list))))
    # 词频向量矩阵
    vectorizer = CountVectorizer()
    word_frequency_vector = vectorizer.fit_transform(word_cut_list)
    words = vectorizer.get_feature_names()
    # 计算TF-IDF
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(word_frequency_vector)
    tf_idf_array = tf_idf.toarray()

    for i in range(len(word_cut_list)):
        model_list = []
        for j in range(len(words)):
            if tf_idf_array[i][j] > 0.0:
                model = DataModel.WeiboTFIDF()
                model.weibo_cut_sid = i + 1
                model.word = words[j]
                model.tf_idf = float(tf_idf_array[i][j])
                model_list.append(model)
        DBConnector.db_list_writer(model_list)
        print('weibo_sid={0}'.format(str(i + 1)))


def calculate_total_tf_idf():
    models = DBConnector.query_all(DataModel.ZhihuCut)
    r = redis.Redis(host='192.168.22.197', port=8173, db=1, encoding='gbk')
    word_cut_list = load_data()
    word_list = []
    for model in models:
        model: DataModel.ZhihuCut
        words = model.answer_word_cut.split('\t')
        for word in words:
            word_list.append(word)
    total_words = len(word_list)
    total_lines = len(word_cut_list)
    vectorizer = CountVectorizer()
    word_frequency_vector = vectorizer.fit_transform(word_cut_list).toarray()
    words = vectorizer.get_feature_names()
    for i in range(len(words)):
        freq_count = 0
        has_count = 0
        for j in range(total_lines):
            if word_frequency_vector[i][j] > 0:
                freq_count = freq_count + word_frequency_vector[i][j]
                has_count = has_count + 1
        tf = freq_count / total_words
        idf_mother = has_count + 1
        idf = math.log(total_lines / idf_mother)
        tf_idf = tf * idf
        r.set(words[i], str(tf_idf))


def get_top_tf_idf_word_zhihu(top_key, zhihu_cut_sid):
    zhihu_cut_id_and_tf_idf_list = []
    models = DBConnector.get_zhihu_tf_idf_by_cut_sid(zhihu_cut_sid)
    for model in models:
        model: DataModel.ZhihuTFIDF
        zhihu_cut_id_and_tf_idf = (model.zhihu_cut_sid, model.word, model.tf_idf)
        zhihu_cut_id_and_tf_idf_list.append(zhihu_cut_id_and_tf_idf)
    sorted_list = sorted(zhihu_cut_id_and_tf_idf_list, key=lambda o: o[2], reverse=True)
    if len(sorted_list) < top_key:
        return sorted_list
    return sorted_list[:top_key]


def get_top_tf_idf_word_weibo(top_key, weibo_cut_id):
    weibo_cut_id_and_tf_idf_list = []
    models = DBConnector.get_zhihu_tf_idf_by_cut_sid(weibo_cut_id)
    for model in models:
        model: DataModel.WeiboTFIDF
        zhihu_cut_id_and_tf_idf = (model.weibo_cut_sid, model.word, model.tf_idf)
        weibo_cut_id_and_tf_idf_list.append(zhihu_cut_id_and_tf_idf)
    sorted_list = sorted(weibo_cut_id_and_tf_idf_list, key=lambda o: o[2], reverse=True)
    if len(sorted_list) < top_key:
        return sorted_list
    return sorted_list[:top_key]


def write_zhihu_csv():
    for i in range(1, 2834):
        result_list = get_top_tf_idf_word_zhihu(30, i)
        model = DataModel.ZhihuCut()
        model.sid = i
        word_list = []
        for item in result_list:
            word = item[1]
            word_list.append(word)
        model.top_word_cut = '\t'.join(word_list)
        zhihu_sid = DBConnector.get_zhihu_sid_by_cut_sid(i)
        vector_result = ZhihuProcess.vector_merge(zhihu_sid)
        if vector_result == 'empty':
            continue
        model.top_words_vector = vector_result
        DBConnector.update_zhihu_top_cut(model)
        print('完成zhihu_cut_sid={0}'.format(str(i)))


write_zhihu_csv()
