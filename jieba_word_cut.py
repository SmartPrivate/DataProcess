import logging
import jieba
import os
import DataModel,DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def init_user_word_list():
    word_list_dir = os.listdir('wordlist')
    for file_name in word_list_dir:
        user_word_file_name = 'wordlist/{0}'.format(file_name)
        words = open(user_word_file_name, 'r', encoding='utf-8').readlines()
        open('user_dict.txt', 'a', encoding='utf-8').writelines(words)


def get_stop_word_list():
    words = open('stoplist_最终使用版.txt', 'r', encoding='utf-8').readlines()
    stop_words = []
    for word in words:
        stop_words.append(word.replace('\n', ''))
    return stop_words


stop_list = get_stop_word_list()
jieba.load_userdict('user_dict.txt')
weibo_models=DBConnector.get_weibo_all()
for model in weibo_models:
    model: DataModel.Weibo
    model.weibo_content