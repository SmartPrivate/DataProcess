import logging
from sqlalchemy import Column, NVARCHAR, Integer, TEXT, DATETIME, BOOLEAN, VARCHAR
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


class ZhihuClean(Base):
    __tablename__ = 'T_Zhihu_cleanfinish'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(100))
    author = Column(NVARCHAR(50))
    question = Column(TEXT)
    answer = Column(TEXT)
    post_date = Column(DATETIME)
    like_num = Column(Integer)
    comment_num = Column(Integer)


class ZhihuCleanCopy(Base):
    __tablename__ = 'T_Zhihu_cleanfinish_copy1'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(100))
    author = Column(NVARCHAR(50))
    question = Column(TEXT)
    answer = Column(TEXT)
    post_date = Column(DATETIME)
    like_num = Column(Integer)
    comment_num = Column(Integer)


class ZhihuCut(Base):
    __tablename__ = 'T_Zhihu_Cut'
    sid = Column(Integer, primary_key=True)
    zhihu_sid = Column(Integer)
    zhihu_answer = Column(TEXT)
    answer_word_cut = Column(TEXT)
    words_vector = Column(TEXT)


class ZhihuWord2Vec(Base):
    __tablename__ = 'T_Zhihu_Word2Vec'
    sid = Column(Integer, primary_key=True)
    zhihu_sid = Column(Integer)
    word = Column(VARCHAR(255))
    vector = Column(TEXT)


class Weibo(Base):
    __tablename__ = 'T_Weibo'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(255))
    author = Column(NVARCHAR(100))
    weibo_content = Column(TEXT)
    publish_time = Column(DATETIME)
    device = Column(NVARCHAR(255))
    retweet = Column(Integer)
    comment = Column(Integer)
    weibo_like = Column(Integer)
    emoji = Column(NVARCHAR(50))


class WeiboClean(Base):
    __tablename__ = 'T_Weibo_cleanfinish'

    sid = Column(Integer, primary_key=True)
    url = Column(NVARCHAR(255))
    author = Column(NVARCHAR(100))
    weibo_content = Column(TEXT)
    publish_time = Column(DATETIME)
    device = Column(NVARCHAR(255))
    retweet = Column(Integer)
    comment = Column(Integer)
    weibo_like = Column(Integer)
    emoji = Column(NVARCHAR(50))


class WeiboCut(Base):
    __tablename__ = 'T_Weibo_Cut'
    sid = Column(Integer, primary_key=True)
    weibo_sid = Column(Integer)
    weibo_content = Column(TEXT)
    word_cut = Column(TEXT)
    words_vector = Column(TEXT)


class WeiboWord2Vec(Base):
    __tablename__ = 'T_Weibo_Word2Vec'
    sid = Column(Integer, primary_key=True)
    weibo_sid = Column(Integer)
    word = Column(VARCHAR(255))
    vector = Column(TEXT)


class Word2VecBaidu(Base):
    __tablename__ = 'D_Word2Vec_Baidu'
    sid = Column(Integer, primary_key=True)
    word = Column(VARCHAR(100))
    vector = Column(TEXT)


class Word2Vec(Base):
    __tablename__ = 'D_Word2Vec'
    sid = Column(Integer, primary_key=True)
    word = Column(VARCHAR(100))
    vector = Column(TEXT)


class DBLP(Base):
    __tablename__ = 'T_DBLP'

    sid = Column(Integer, primary_key=True)
    title = Column(TEXT)
    author = Column(TEXT)
    pages = Column(NVARCHAR(50))
    year = Column(Integer)
    volume = Column(NVARCHAR(50))
    journal = Column(TEXT)
    number = Column(NVARCHAR(50))
    url = Column(TEXT)
    ee = Column(TEXT)
