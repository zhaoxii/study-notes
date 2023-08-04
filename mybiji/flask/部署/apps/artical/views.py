from flask import Blueprint, request, g, redirect, url_for, render_template, session
from flask.json import jsonify

from apps.artical.model import Article, Article_type, Comment
from apps.user.model import User
from apps.utils.util import user_type
from exts.sql import db

article_bp1 = Blueprint("article1", __name__, url_prefix='/article')

# 自定义过滤器
@article_bp1.app_template_filter('cdecode')   # 因为article数据库中的comment字段类型为text时，不能显示表情或者小图标，所以改为blob类型(二进制类型)，然后在网页上显示的时候需要重新decode为str
def content_decode(content):
    content=content.decode('utf-8')
    return content


# 发表文章
@article_bp1.route('/publish', methods=['POST', 'GET'])
def publish():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content').encode('utf-8')
        print('------------->>>>>>>>>', title)
        print('===============>>>>>>>>>', type_id)
        print('+++++++++++++++++++.>>>>', content)
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id=g.user.id
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('user.index'))

    return 'okooo'


#  文章详情
@article_bp1.route('/detail')
def article_detail():
    aid=request.args.get('aid')    # 文章id
    article=Article.query.get(aid)  # 获取文章对象
    types=Article_type.query.all()  # 获取文章的分类


    user=None
    uid=session.get('uid',None)
    if uid:
        user=User.query.get(uid)

    page=int(request.args.get('page',1))  #  注意转为int型
    pagination=Comment.query.filter(Comment.article_id==aid).order_by(-Comment.cdatetime).paginate(page=page,per_page=5)  # 过滤，排序，分页

    return render_template('article/detail.html',article=article,types=types,user=user,comments=pagination)


# 点赞
@article_bp1.route('/love')
def love():
    article_id = request.args.get('aid')
    tag=request.args.get('tag')
    article=Article.query.get(article_id)

    if tag=='1':
        article.love_num -= 1
    else:
        article.love_num+=1

    db.session.commit()

    return jsonify(num=article.love_num)



# 发表文章评论
@article_bp1.route('/add_comment',methods=['POST','GET'])
def article_comment():

    if request.method=='POST':
        comment_content = request.form.get('comment')
        user_id=g.user.id
        article_id=request.form.get('aid')

        comment = Comment()
        comment.comment=comment_content
        comment.user_id=user_id
        comment.article_id=article_id
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('article1.article_detail')+'?aid='+article_id)

    return redirect(url_for('user.index'))






#  文章分类检索
@article_bp1.route('/type_search')
def type_search():

    user,types=user_type()   # 当前登录用户对象 和 所有类别
    #  tid 的获取,类别id  ,给个默认 1
    tid=request.args.get('tid',1)

    # 分页
    page=int(request.args.get('page',1))
    articles=Article.query.filter(Article.type_id==tid).paginate(page=page,per_page=3)  # 查找 该类别的文章

    params = {
        'user': user,
        'types': types,
        'articles': articles,
        'tid': tid,
    }

    return render_template('article/article_type.html',**params)









