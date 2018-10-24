import logging

import redis

import DataModel
import datetime
import DBConnector
import re
import time
import os
import WordCutter

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def weibo_process():
    """
    微博数据清洗
    :return:
    """
    reader = open(r'C:\\Users\\macha\\Desktop\\weibo.txt', 'r', errors='replace', encoding='gbk')
    model_list = []
    while True:
        line = reader.readline()
        if not line:
            break
        items = line.split('\t')
        model = DataModel.Weibo()
        model.url = items[0]
        model.author = items[1]
        content_ori = items[2]
        # 正则匹配，去除无意义标识
        result = re.subn('//@.*', '', content_ori)
        result = re.subn('@.*?：', '', result[0])
        result = re.subn('@.*?:', '', result[0])
        result = re.subn('@.*? ', '', result[0])
        result = re.subn('\(分享自.*', '', result[0])
        result = re.subn('\?+', '', result[0])
        result = re.subn('（.*秒拍.*?）', '', result[0])
        result = re.subn('\(.*秒拍.*?\)', '', result[0])
        result = re.subn('L.*秒拍视频', '', result[0])
        result = re.subn('#.*秒拍.*#', '', result[0])
        result = re.subn('O.*微博.*', '', result[0])
        result = re.subn('O.*微博.*', '', result[0])
        result = re.subn('&.*?;', '', result[0])
        # 字符串替换，去除无意义标识
        replace_list = ['O网页链接', 'O秒拍视频', '查看图片', '?查看图片', '(来自', '（分享自', 'L微博视频', '分享自秒拍用户', '...展开全文c',
                        '  的作品,一起来看~ ',
                        '我的秒拍作品，一起来看~', '我的秒拍作品,一起来看~', 'O秒拍直播', '我的秒拍作品', 'O秒拍直播', '最神奇的秒拍视频', '卡卡贷的秒拍视']
        content = result[0]
        for word in replace_list:
            content = content.replace(word, '')
        if content == '':
            continue

        model.weibo_content = content

        emoji = re.findall('\[.*?\]', content)
        if len(emoji) > 0:
            model.emoji = ','.join(emoji)
        else:
            model.emoji = ''
        time_str = items[3] + ' ' + items[4]
        # model.publish_time = time.strptime(time_str, '%Y/%m/%d %H:%M')
        model.publish_time = time_str
        model.device = items[5]
        if '转发' in items[6]:
            model.retweet = 0
        else:
            model.retweet = int(items[6])
        if '评论' in items[7]:
            model.comment = 0
        else:
            model.comment = int(items[7])
        if '赞' in items[8]:
            model.weibo_like = 0
        else:
            model.weibo_like = int(items[8])
        model_list.append(model)
    DBConnector.db_list_writer(model_list)


def file_db_writer():
    files = os.listdir('new_vec')
    for filename in files:
        reader = open('new_vec/{0}'.format(filename), 'r', encoding='gbk', errors='ignore')
        print('正在处理文件{0}......'.format(filename))
        model_list = []
        list_count = 0
        while True:
            line = reader.readline()
            if not line:
                break
            model = DataModel.WeiboWord2Vec()
            try:
                weibo_sid = int(line.split(':')[0])
                if weibo_sid <= 9808:
                    continue
                model.weibo_sid = weibo_sid
                model.word = line.split(':')[1]
                model.vector = line.split(':')[2]
            except IndexError:
                model.vector = None
                print(line)
                continue
            except ValueError:
                print(line)
                continue
            model_list.append(model)
            list_count = list_count + 1
            if list_count == 10000:
                DBConnector.db_list_writer(model_list)
                model_list.clear()
                list_count = 0


def weibo_vector_merge(min_weibo_sid, max_weibo_sid):
    """
    微博向量聚合
    :param min_weibo_sid:
    :param max_weibo_sid:
    :return:
    """
    db_session = DBConnector.create_db_session(DBConnector.DBName.MySQL)
    new_session = db_session()
    for i in range(min_weibo_sid, max_weibo_sid):
        models = DBConnector.query_weibo_word2vec_by_weibo_sid(i)
        if len(models) == 0:
            continue
        one_weibo_vector, one_weibo_vector_str_list = [], []
        for j in range(1024):
            one_weibo_vector.append(0.0)
        for model in models:
            model: DataModel.WeiboWord2Vec
            vector_list = model.vector.split(',')
            if len(vector_list) != 1024:
                continue
            for k in range(1024):
                one_weibo_vector[k] = one_weibo_vector[k] + float(vector_list[k])
        for item in one_weibo_vector:
            one_weibo_vector_str_list.append(str(item))
        one_weibo_vector_str = ','.join(one_weibo_vector_str_list)
        new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCut.weibo_sid == i).update(
            {DataModel.WeiboCut.words_vector: one_weibo_vector_str})
        new_session.commit()
        # DBConnector.update_weibo_word_cut_vector_by_sid(i, one_weibo_vector_str)
        print('完成weibo_sid={0}'.format(i))
    new_session.close()


def get_weibo_word_pos():
    r = redis.Redis(host='192.168.22.241', port=6379, db=1, encoding='gbk', decode_responses=True)
    weibo_models = DBConnector.query_all(DataModel.WeiboCutNoShort)
    word_processer = WordCutter.WordCut()
    writer = open('no_word_pos.csv', 'a', encoding='gbk')
    for model in weibo_models:
        model: DataModel.WeiboCutNoShort
        words = model.word_cut.replace('\t', ',')
        print(len(words.split(',')))
        result = word_processer.get_word_speech(words)
        if type(result) is str:
            continue
        print(len(result))
        print('Finish weibo_sid = {0}'.format(model.weibo_sid))


get_weibo_word_pos()
