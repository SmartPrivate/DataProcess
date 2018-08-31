import logging
import json
import requests
import DataModel, DBConnector
import os

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

print(int(20121 / 5000))


def word_to_vec_baiduyun(process_str, token_index):
    process_str.encode('gbk')
    post_data_dict = dict(word=process_str)
    post_data = json.dumps(post_data_dict)
    token_json_lines = open('baiduyun_access_token.json', 'r').readlines()
    format_json = json.loads(token_json_lines[token_index].replace('\n', ''))
    post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec'
    post_params = dict(access_token=format_json['access_token'])
    r = requests.post(post_url, params=post_params, data=post_data)
    print(r.text)


def save_new_dict_to_db():
    filenames = os.listdir('new_dict')
    for filename in filenames:
        reader = open('new_dict/{0}'.format(filename), 'r', encoding='gbk')
        lines = reader.readlines()
        model_list = []
        for line in lines:
            if line == '\n':
                continue
            model = DataModel.Word2Vec()
            # model.zhihu_sid = line.split(':')[0]
            model.word = line.split(':')[0]
            model.vector = line.split(':')[1]
            model_list.append(model)
        DBConnector.db_list_writer(model_list)
        print('已完成新字典文件{0}'.format(filename))
        reader.close()


def save_new_zhihu_vec_to_db():
    filenames = os.listdir('new_vec')
    for filename in filenames:
        reader = open('new_vec/{0}'.format(filename), 'r', encoding='gbk')
        lines = reader.readlines()
        model_list = []
        for line in lines:
            if line == '\n':
                continue
            model = DataModel.ZhihuWord2Vec()
            model.zhihu_sid = line.split(':')[0]
            model.word = line.split(':')[1]
            model.vector = line.split(':')[2]
            model_list.append(model)
        DBConnector.db_list_writer(model_list)
        print('已完成新知乎向量文件{0}'.format(filename))
        reader.close()


def new_file():
    session_maker = DBConnector.create_db_session(DBConnector.DBName.MySQLRoot)
    db_session = session_maker()
    models = db_session.query(DataModel.ZhihuCut).all()
    db_session.close()
    new_model_list = []
    for model in models:
        model: DataModel.ZhihuCut
        new_model = DataModel.ZhihuCut()
        new_model.zhihu_sid = model.zhihu_sid
        new_model.answer_word_cut = model.answer_word_cut
        new_model.zhihu_answer = model.zhihu_answer
        new_model.words_vector = model.words_vector
        new_model_list.append(new_model)
