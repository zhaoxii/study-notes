from exts.sql import db


class Goods(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    gname=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Float,nullable=False)
    users=db.relationship("User",backref='goodslist',secondary='user_goods')  # secondary 是去第三方的表中去找 ，是表名  。 第一个参数是类名， backref是 反向查找

    def __str__(self):
        return self.gname


#  建表方式2
# tags=db.Table(
#     'tags',  #表名
#     db.Column("tag_id",db.Integer,db.ForeignKey("tag.id")),  # tag_id 字段名
#     db.Column("page_id",db.Integer,db.ForeignKey("page.id"))
# )

#  关系表，承接user与goods的关系 在数据库中存在的表
class User_goods(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    goods_id=db.Column(db.Integer,db.ForeignKey("goods.id"))
    num=db.Column(db.Integer,default=1)



