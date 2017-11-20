# coding:utf-8

from config import MYSQL_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, TIMESTAMP, Integer, Text
from sqlalchemy.sql import func


Base = declarative_base()


class UserInfo(Base):
    """用户信息表"""
    __tablename__ = "t_zhihu_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), unique=True)   # 用户id
    url_token = Column(String(100), unique=True)    # 用户token

    name = Column(String(100), index=True)      # 用户名
    headline = Column(String(100))              # 简介
    location = Column(String(100))              # 地址
    industry = Column(String(100))              # 行业
    school = Column(String(100))                # 学校
    major = Column(String(100))                 # 专业

    answer_count = Column(Integer)               # 回答总数
    question_count = Column(Integer)             # 数量
    articles_count = Column(Integer)                 # 文章数量
    columns_count = Column(Integer)               # 专栏数量

    voteup_count = Column(Integer)               # 个人成就-赞同
    thanked_count = Column(Integer)              # 个人成就-感谢
    favorited_count = Column(Integer)            # 个人成就-收藏
    following_count = Column(Integer)             # 关注
    follower_count = Column(Integer, index=True)              # 关注者
    gender = Column(Integer)    # 性别
    text = Column(Text)     # json值
    create_time = Column(TIMESTAMP, server_default=func.now())



class UpdateUserInfo(Base):
    """更新表"""
    __tablename__ = "t_zhihu_update"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), index=True)   # 用户id
    url_token = Column(String(100), index=True)    # 用户token
    name = Column(String(100), index=True)      # 用户名
    answer_count = Column(Integer)               # 回答总数
    question_count = Column(Integer)             # 数量
    articles_count = Column(Integer)                 # 文章数量
    columns_count = Column(Integer)               # 专栏数量

    voteup_count = Column(Integer)               # 个人成就-赞同
    thanked_count = Column(Integer)              # 个人成就-感谢
    favorited_count = Column(Integer)            # 个人成就-收藏
    following_count = Column(Integer)             # 关注
    follower_count = Column(Integer, index=True)              # 关注者
    text = Column(Text)     # json值
    create_time = Column(TIMESTAMP, server_default=func.now())


class Relation(Base):
    """用户关系表"""
    __tablename__ = "t_zhihu_relation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_url_token = Column(String(100), index=True)
    children_url_token = Column(String(100), index=True)
    md5 = Column(String(32), unique=True)
    create_time = Column(TIMESTAMP, server_default=func.now())


engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8".format(**MYSQL_CONFIG))
# 创建表
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
