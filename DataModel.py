import logging
from sqlalchemy import Column, NVARCHAR, Integer, TEXT, DATETIME, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

Base = declarative_base()


class AMiner(Base):
    __tablename__ = 'T_AMiner'

    sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(24))
    title = Column(TEXT)
    venue = Column(TEXT)
    year = Column(Integer)
    keywords = Column(TEXT)
    fos = Column(NVARCHAR(100))
    n_citation = Column(Integer)
    page_start = Column(TEXT)
    page_end = Column(TEXT)
    doc_type = Column(TEXT)
    lang = Column(TEXT)
    publisher = Column(TEXT)
    volume = Column(TEXT)
    issue = Column(TEXT)
    issn = Column(TEXT)
    isbn = Column(TEXT)
    doi = Column(TEXT)
    pdf = Column(TEXT)
    url = Column(TEXT)
    abstract = Column(TEXT)


class AMinerAuthor(Base):
    __tablename__ = 'T_AMinerAuthor'

    author_sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(24))
    name = Column(NVARCHAR(50))
    org = Column(TEXT)


class AMinerReference(Base):
    __tablename__ = 'T_AMinerReference'

    reference_sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(24))
    reference = Column(NVARCHAR(24))


class MAG(Base):
    __tablename__ = 'T_MAG'

    sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(36))
    title = Column(TEXT)
    venue = Column(TEXT)
    year = Column(Integer)
    keywords = Column(TEXT)
    fos = Column(TEXT)
    n_citation = Column(Integer)
    page_start = Column(TEXT)
    page_end = Column(TEXT)
    doc_type = Column(TEXT)
    lang = Column(TEXT)
    publisher = Column(TEXT)
    volume = Column(TEXT)
    issue = Column(TEXT)
    issn = Column(TEXT)
    isbn = Column(TEXT)
    doi = Column(TEXT)
    pdf = Column(TEXT)
    url = Column(TEXT)
    abstract = Column(TEXT)


class MAGAuthor(Base):
    __tablename__ = 'T_MAGAuthor'

    author_sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(36))
    name = Column(TEXT)
    org = Column(TEXT)
    year = Column(Integer)


class MAGReference(Base):
    __tablename__ = 'T_MAGReference'

    reference_sid = Column(Integer, primary_key=True)
    id = Column(NVARCHAR(36))
    reference = Column(NVARCHAR(36))
    year = Column(Integer)


class Zhihu(Base):
    __tablename__ = 'T_Zhihu'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(100))
    author = Column(NVARCHAR(50))
    question = Column(TEXT)
    answer = Column(TEXT)
    post_date = Column(DATETIME)
    like_num = Column(Integer)
    comment_num = Column(Integer)


class Weibo(Base):
    __tablename__ = 'T_Weibo'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(255))
    author = Column(NVARCHAR(100))
    content = Column(TEXT)
    publish_time = Column(DATETIME)
    retweet = Column(Integer)
    comment = Column(Integer)
    like = Column(Integer)
    emoji = Column(NVARCHAR(20))
