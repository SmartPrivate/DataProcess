import logging
import DBConnector, DataModel
import json
import requests
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class WordCut(object):

    def __init__(self, stop_word_list: str = None):
        if not stop_word_list:
            self.__stop_word_list = None
        else:
            self.__stop_word_list = self.load_stop_word_list(stop_word_list)

    def word_cut_baiduyun(self, process_str: str):
        # process_str.encode('gbk')
        post_data_dict = dict(text=process_str)
        post_data = json.dumps(post_data_dict)
        token_json_line = open('baiduyun_access_token.json', 'r').readline()
        format_json = json.loads(token_json_line)
        post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer'
        post_params = dict(access_token=format_json['access_token'])
        try:
            r = requests.post(post_url, params=post_params, data=post_data)
            time.sleep(0.1)
            result_json = json.loads(r.text)
            if 'error_code' in result_json.keys():
                return result_json['error_code'], result_json['error_msg'], result_json
            result_str_list = []
            for item in result_json['items']:
                if self.__stop_word_list:
                    if item['item'] in self.__stop_word_list:
                        continue
                result_str_list.append(item['item'])
            return 0, '\t'.join(result_str_list), result_json
        except requests.exceptions.ConnectionError:
            return 1, '连接超时！请检查你的网络连接...', None

    @staticmethod
    def load_stop_word_list(stop_word_list_dir):
        words = open(stop_word_list_dir, 'r', encoding='utf-8').readlines()
        stop_words = []
        for word in words:
            stop_words.append(word.replace('\n', ''))
        return stop_words


def word_cut_jieba():
    return
