from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum, unique
import DataModel
import os

import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

localhost_str = 'mssql+pyodbc://sa:900807@localhost/OpenAcademicGraphDB?driver=ODBC+Driver+17+for+SQL+Server'
remotehost_str = 'mssql+pyodbc://sa:Alex19900807.@192.168.22.197/WangxiaoDB?driver=ODBC+Driver+17+for+SQL+Server'

DBMySQLEngine: str = 'mysql+pymysql://myuser:Mc2460022.@192.168.22.197:3306/mysql'
DBSQLServerEngine: str = remotehost_str


@unique
class DBName(Enum):
    MySQL = 0
    MSSQLSERVER = 1


DBNameDic = {0: 'mysql', 1: 'mssql'}


def create_db_session(db_name: DBName):
    connect_str: str
    if db_name == DBName.MSSQLSERVER:
        connect_str = DBSQLServerEngine
    elif db_name == DBName.MySQL:
        connect_str = DBMySQLEngine
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
    return new_session.query(DataModel.WeiboCut).filter(DataModel.WeiboCut.weibo_sid > min_weibo_sid,
                                                        DataModel.WeiboCut.weibo_sid < max_weibo_sid).all()


def query_all(model):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(model).all()


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


def update_zhihu_data_by_sid(sid, word_cut):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).update(
        {DataModel.ZhihuCut.answer_word_cut: word_cut})
    new_session.commit()
    new_session.close()


def query_zhihu_cut_by_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.ZhihuCut).filter(DataModel.ZhihuCut.sid == sid).one()
