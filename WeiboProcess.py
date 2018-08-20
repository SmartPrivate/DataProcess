import logging
import DataModel
import datetime
import DBConnector
import re
import time
import os

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def weibo_process():
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
    files=os.listdir('new_vec')
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