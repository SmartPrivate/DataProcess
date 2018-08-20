import logging
import DataModel
import DBConnector
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

weibo_vec_models=DBConnector.query_all_word2vec_within(0,5000)
print(len(weibo_vec_models))
for model in weibo_vec_models:
    model: DataModel.WeiboWord2Vec