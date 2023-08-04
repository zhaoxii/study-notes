from datetime import datetime

from apps.user.model import User
from exts.sql import db


class Article_type(db.Model):  # 文章类型表
    # __tablename__='type'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type_name=db.Column(db.String(20),nullable=False)
    articles =db.relationship('Article',backref='articletype')  # 根据类型找文章



class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.BLOB,nullable=False)   # BLOB 二进制类型
    pdatetime=db.Column(db.DateTime,default=datetime.now)# 发布时间
    click_num=db.Column(db.Integer,default=0)#浏览量，阅读数量
    save_num=db.Column(db.Integer,default=0)# 收藏
    love_num=db.Column(db.Integer,default=0) # 点赞
    # 建立外键
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    type_id=db.Column(db.Integer,db.ForeignKey('article_type.id'),nullable=False,default=1)
    comments=db.relationship('Comment',backref='article')  # 通过文章找 评论





class Comment(db.Model):
    __tablename__="comment"  # 自定义表名
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment=db.Column(db.String(255),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    article_id=db.Column(db.Integer,db.ForeignKey('article.id'))
    cdatetime=db.Column(db.DateTime,default=datetime.now)


    def __str__(self):
        return self.comment








