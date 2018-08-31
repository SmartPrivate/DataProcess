from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum, unique
import DataModel
import os

import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

localhost_str = 'mssql+pyodbc://sa:900807@localhost/OpenAcademicGraphDB?driver=ODBC+Driver+17+for+SQL+Server'
remotehost_str = 'mssql+pyodbc://sa:Alex19900807.@192.168.22.197/WangxiaoDB?driver=ODBC+Driver+17+for+SQL+Server'

DBMySQLEngineRoot: str = 'mysql+pymysql://myuser:Mc2460022.@192.168.22.197:3306/mysql'
DBMySQLEngine: str = 'mysql+pymysql://wangxiao:xiao123123@192.168.22.197:3306/wangxiao_db'
DBSQLServerEngine: str = remotehost_str


@unique
class DBName(Enum):
    MySQL = 0
    MySQLRoot = 1
    MSSQLSERVER = 2


DBNameDic = {0: 'mysql', 1: 'mssql'}


def create_db_session(db_name: DBName):
    connect_str: str
    if db_name == DBName.MSSQLSERVER:
        connect_str = DBSQLServerEngine
    elif db_name == DBName.MySQL:
        connect_str = DBMySQLEngine
    elif db_name == DBName.MySQLRoot:
        connect_str = DBMySQLEngineRoot
    engine = create_engine(connect_str)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session


def db_writer(model: object):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.add(model)
    new_session.commit()
    new_session.close()


def db_list_writer(models):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.bulk_save_objects(models)
    new_session.commit()
    new_session.close()


def query_all_word2vec_within(min_weibo_sid, max_weibo_sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCut.weibo_sid >= min_weibo_sid,
                                                        DataModel.WeiboCut.weibo_sid < max_weibo_sid).all()


def query_all_zhihu_word2vec_within(min_sid, max_sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.zhihu_sid >= min_sid,
                                                        DataModel.ZhihuCut.zhihu_sid < max_sid).all()


def query_all(model):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(model).all()
    new_session.close()
    return models


def get_weibo_all():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.Weibo).all()


def update_weibo_end_with_at(sid, weibo):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.Weibo).filter(DataModel.Weibo.sid == sid).update({DataModel.Weibo.weibo_content: weibo})
    new_session.commit()
    new_session.close()


def delete_weibo_no_data(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.Weibo).filter(DataModel.Weibo.sid == sid).delete()
    new_session.commit()
    new_session.close()


def update_zhihu_cut_by_sid(sid, word_cut):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).update(
        {DataModel.ZhihuCut.answer_word_cut: word_cut})
    new_session.commit()
    new_session.close()


def update_zhihu_top_cut(model: DataModel.ZhihuCut):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == model.sid).update(
        {DataModel.ZhihuCut.top_word_cut: model.top_word_cut,
         DataModel.ZhihuCut.top_words_vector: model.top_words_vector})
    new_session.commit()
    new_session.close()


def update_zhihu_answer_by_sid(sid, answer):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).update(
        {DataModel.ZhihuCut.zhihu_answer: answer})
    new_session.commit()
    new_session.close()


def update_weibo_word_cut_vector_by_sid(weibo_sid, word_cut):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCut.weibo_sid == weibo_sid).update(
        {DataModel.WeiboCut.words_vector: word_cut})
    new_session.commit()
    new_session.close()


def query_weibo_word2vec_by_weibo_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(DataModel.WeiboWord2Vec).filter(DataModel.WeiboWord2Vec.weibo_sid == sid).all()
    new_session.close()
    return models


def query_weibo_word2vec_by_weibo_sid_within(min_index, max_index):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.WeiboWord2Vec).filter(DataModel.WeiboWord2Vec.weibo_sid >= min_index,
                                                             DataModel.WeiboWord2Vec.weibo_sid < max_index).all()


def query_zhihu_cut_by_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).one()


def query_zhihu_cut_by_zhihu_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.zhihu_sid == sid).one()
    new_session.close()
    return models


def query_zhihu_word2vec_by_zhihu_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQLRoot)
    new_session = db_session()
    models = new_session.query(DataModel.ZhihuWord2Vec).filter(DataModel.ZhihuWord2Vec.zhihu_sid == sid).all()
    new_session.close()
    return models


def query_weibo_cut_by_weibo_sid_within(min_index, max_index):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCut.weibo_sid >= min_index,
                                                        DataModel.WeiboCut.weibo_sid < max_index).all()


def get_zhihu_sid_in(sid_list):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    result = new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.zhihu_sid.in_(sid_list)).all()
    new_session.close()
    return result


def get_sid_in(sid_list, filename):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    if filename == 'zhihu':
        result = new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid.in_(sid_list)).all()
        new_session.close()
        return result
    elif filename == 'weibo':
        result = new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCutNoShort.weibo_sid.in_(sid_list)).all()
        new_session.close()
        return result


def get_zhihu_tf_idf_by_cut_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(DataModel.ZhihuTFIDF).filter(DataModel.ZhihuTFIDF.zhihu_cut_sid == sid).all()
    new_session.close()
    return models


def get_weibo_tf_idf_by_cut_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(DataModel.WeiboTFIDF).filter(DataModel.WeiboTFIDF.weibo_cut_sid == sid).all()
    new_session.close()
    return models


def delete_small_weibo_cut():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    models = new_session.query(DataModel.WeiboCut).all()
    new_session.close()
    model_list = []
    for model in models:
        model: DataModel.WeiboCut
        if model.words_vector is None:
            continue
        if len(model.word_cut.split('\t')) < 3:
            continue
        new_model = DataModel.WeiboCutNoShort()
        new_model.weibo_sid = model.weibo_sid
        new_model.weibo_content = model.weibo_content
        new_model.word_cut = model.word_cut
        new_model.words_vector = model.words_vector
        model_list.append(new_model)
    db_list_writer(model_list)


def get_zhihu_sid_by_cut_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    model: DataModel.ZhihuCut = new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).one()
    return model.zhihu_sid
