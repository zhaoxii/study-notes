from flask import Blueprint, render_template, request

from apps.artical.model import Article
from apps.user.model import User
from exts.sql import db

article_bp = Blueprint('article', __name__)

@article_bp.route('/publish',methods=['POST','GET'])
def publish_article():
    if request.method=='POST':
        title = request.form.get("title")
        content=request.form.get("content")
        uid=request.form.get('uid')

        article=Article()
        article.title=title
        article.content=content
        article.user_id=uid
        db.session.add(article)
        db.session.commit()

        return '添加成g'
    else:
        users=User.query.filter(User.isdelete==False).all()


        return render_template('article/add_article.html',users=users)


@article_bp.route('/all')  # 根据文章找作者
def all_article():
    articles=Article.query.all()

    return render_template('article/all.html',articles=articles)


@article_bp.route('/all1')   # 根据用户获取该用户的文章
def all_article1():
    id=request.args.get('id')
    user=User.query.get(id)
    return render_template('article/all1.html',user=user)



