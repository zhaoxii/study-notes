from datetime import datetime

from exts.sql import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(30), )
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)

    articles = db.relationship('Article', backref='user')  # 这个字段不会在数据库中体现，是用在view和template中的
    # Article是文章类的类名  backref参数是反向
    # relationship 定义的字段，不是Column定义的，不往数据库中插入，但是也可以通过对象获取
    comments = db.relationship('Comment', backref='user')

    def __str__(self):
        return self.username




class Photo(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    photo_name=db.Column(db.String(100),nullable=False,)  #
    photo_datatime=db.Column(db.DateTime,default=datetime.now)  # 上传时间


    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __str__(self):
        return self.photo_name



class AboutMe(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    content=db.Column(db.BLOB,nullable=False)
    pdatetime=db.Column(db.DateTime,default=datetime.now)

    #要与用户建立联系
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),unique=True)
    user=db.relationship('User',backref='aboutme')




class MessageBoard(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    content=db.Column(db.String(255),nullable=False)
    mdatetime=db.Column(db.DateTime,default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))  # 规定  0为匿名用户


    user=db.relationship('User',backref='messages')


















