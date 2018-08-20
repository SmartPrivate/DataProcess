import logging
import DataModel
import datetime
import DBConnector
import re
import WordCutter
import json

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


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
    reader = open(r'C:\\Users\\macha\\Desktop\\2.txt', 'r', errors='replace')
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


def zhihu_word_cut():
    models = DBConnector.query_all(DataModel.ZhihuClean)
    cut_model_list = []
    for model in models:
        model: DataModel.ZhihuClean
        result_code, result, result_json = WordCutter.word_cut_baiduyun(model.answer)
        if result_code != 0:
            print(model.sid)
            print(result)
            continue
        cut_model = DataModel.ZhihuCut()
        cut_line = result
        cut_model.zhihu_sid = model.sid
        cut_model.zhihu_answer = model.answer
        cut_model.answer_word_cut = cut_line
        print(cut_line)
        cut_model_list.append(cut_model)
    DBConnector.db_list_writer(cut_model_list)


def zhihu_clean():
    models = DBConnector.query_all(DataModel.ZhihuCleanCopy)
    model_list = []
    for item in models:
        item: DataModel.ZhihuClean
        for word in ['泻药', '谢邀', '谢谢邀请', '感谢邀请', '"谢邀']:
            if item.answer.startswith(word):
                item.answer = item.answer.replace(word, '')
            if item.answer.startswith('。'):
                item.answer = item.answer.replace('。', '')
                print(item.answer)
        new_model = DataModel.ZhihuClean()
        new_model.url = item.url
        new_model.answer = item.answer
        new_model.author = item.author
        new_model.comment_num = item.comment_num
        new_model.like_num = item.like_num
        new_model.post_date = item.post_date
        new_model.question = item.question
        model_list.append(new_model)

    DBConnector.db_list_writer(model_list)


def too_long_process():
    models = DBConnector.query_all(DataModel.ZhihuCut)
    cutter = WordCutter.WordCut(stop_word_list='stoplist_最终使用版.txt')
    long_str_list = []
    for model in models:
        model: DataModel.ZhihuCut
        if len(model.zhihu_answer) < 10000:
            continue
        if 'key' not in model.answer_word_cut:
            continue
        short_str_list = cut_str_by_length(model.zhihu_answer, 5000)
        for item in short_str_list:
            result_code, result, result_json = cutter.word_cut_baiduyun(item)
            long_str_list.append(result)
        result_str='\t'.join(long_str_list)
        print(result_str)
        DBConnector.update_zhihu_data_by_sid(model.sid, result_str)


def cut_str_by_length(process_str, length):
    ori_len = len(process_str)
    cut_str_list = []
    step = int(ori_len / length)
    for i in range(step):
        start_index = i * length
        end_index = (i + 1) * length - 1
        short_str = process_str[start_index:end_index]
        cut_str_list.append(short_str)
    cut_str_list.append(process_str[step * length:ori_len - 1])
    return cut_str_list


too_long_process()
