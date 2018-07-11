import logging
import DataModel
import datetime
import DBConnector
import re

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

reader = open(r'C:\\Users\\macha\\Desktop\\2.txt', 'r', errors='replace')


def assemble_model():
    model = DataModel.Zhihu()
    model.url = text_list[0]
    model.author = text_list[1]
    model.question = text_list[2]
    model.post_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    model.like_num = int(like)
    model.comment_num = int(comment)
    index = answer_ori.rfind('编辑于')
    if index == -1:
        index = answer_ori.rfind('发布于')
    answer = answer_ori[:index]
    result, count = re.subn('<.*?>', '', answer)
    if count == 0:
        model.answer = answer
    else:
        model.answer = result
    return model


def add_zhihu_data_to_db():
    global text_list, answer_ori, comment, date_str, like
    line_count = 0
    while True:
        line = reader.readline()
        if not line:
            break
        text_list = line.split('\t')
        answer_ori = '\t'.join(text_list[5:])
        date_like_comment = answer_ori.split(' ')
        if '添加评论' in date_like_comment[-1]:
            comment = '0'
            date_str = date_like_comment[-1][:10]
            like = date_like_comment[-1].split('?')[0][10:]
            if 'K' in like:
                like = text_list[3].split(' ')[0].replace('"', '').replace(',', '')
        else:
            like = date_like_comment[-2].split('?')[0][10:]
            if 'K' in like:
                like = text_list[3].split(' ')[0].replace('"', '').replace(',', '')
            date_str = date_like_comment[-2][:10]
            comment = date_like_comment[-2][10:].split('?')[1].replace(',', '')
        line_count = line_count + 1
        print(line_count)
        write_model = assemble_model()
        DBConnector.db_writer(write_model)


