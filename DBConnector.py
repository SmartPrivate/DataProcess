from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum, unique

import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

localhost_str = 'mssql+pyodbc://sa:900807@localhost/OpenAcademicGraphDB?driver=ODBC+Driver+17+for+SQL+Server'
remotehost_str = 'mssql+pyodbc://sa:Alex19900807.@192.168.22.197/WangXiaoDB?driver=ODBC+Driver+17+for+SQL+Server'

DBMySQLEngine: str = 'mysql+pymysql://myuser:Mc2460022.@192.168.22.197:3306/mysql'
DBSQLServerEngine: str = localhost_str


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
    db_session: sessionmaker = create_db_session(DBName.MSSQLSERVER)
    new_session = db_session()
    new_session.add(model)
    new_session.commit()
    new_session.close()


def db_list_writer(models):
    db_session: sessionmaker = create_db_session(DBName.MSSQLSERVER)
    new_session = db_session()
    new_session.bulk_save_objects(models)
    new_session.commit()
    new_session.close()
