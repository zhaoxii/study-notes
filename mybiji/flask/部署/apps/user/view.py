import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from apps.user.model import User, Photo, AboutMe, MessageBoard
from apps.artical.model import Article_type,Article
from apps.user.smssend import SmsSendAPIDemo
from apps.utils.util import upload_qiniu, del_qiniu
from exts.sql import db
import os
from config import DevelopmentConfig

user_bp = Blueprint('user', __name__, url_prefix='/user')  # url_prefix 是给该蓝图添加一个 拼接的路径，要访问该蓝图定义的route，要加上该路径，以 / 开头

required_login_list = ['/user/center',
                       '/user/change',
                       '/article/publish',
                       '/user/upload_photo',
                       '/user/photo_del',
                       '/article/add_comment',
                       '/user/aboutme',
                       '/user/showaboueme']


@user_bp.before_app_first_request
def first_request():
    print('before_app_first_request')


@user_bp.before_app_request
def before_request1():
    print('before_app_request', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html',)
        else:
            user = User.query.get(id)
            # g是一个对象，本次请求的一个对象，往这个对象里放入一个属性user
            # g 只存在于这次请求中  ，下次请求就没了
            g.user = user


@user_bp.after_app_request
def after_request1(response):  # 一般有需要再写，没啥需求不用写
    response.set_cookie('a', 'bbb', max_age=1800)
    print('after_app_request')
    return response


@user_bp.teardown_app_request
def teardown_request_test(response):
    print('teardown_request_test')
    return response


# 自定义过滤器
@user_bp.app_template_filter('cdecode')   # 因为article数据库中的comment字段类型为text时，不能显示表情或者小图标，所以改为blob类型(二进制类型)，然后在网页上显示的时候需要重新decode为str
def content_decode(content):
    content=content.decode('utf-8')
    return content[:100]

# 自定义过滤器
@user_bp.app_template_filter('cdecode1')
def content_decode(content):
    content=content.decode('utf-8')
    return content


# 首页
@user_bp.route('/')
def index():
    # uid=request.cookies.get('uid',None)  # 找到则返回uid，否则返回None
    # print(uid)
    #  session获取 字典的方式获取
    uid = session.get('uid')
    types=Article_type.query.all()

    page=int(request.args.get('page',1))  # 接收页码数 收不到默认是1

    pagination=Article.query.order_by(-Article.pdatetime).paginate(page=page,per_page=3)
    print(pagination.items)  # [<apps.artical.model.Article object at 0x0000027505344C88>, <apps.artical.model.Article object at 0x000002750534D1C8>, <apps.artical.model.Article object at 0x000002750534D248>]
    print(pagination.page)    # 当前页码数
    print(pagination.prev_num)  # 当前页的前一个页码数
    print(pagination.next_num)  #  当前页的后一页的页码数
    print(pagination.has_next)   # 当前页是否有下一页
    print(pagination.has_prev)   # 当前页 是否有上一页
    print(pagination.pages)      #  总页数
    print(pagination.total)      #  数据库中总条数

    if uid:  # 如果有这个cookie则 代表登录成功
        user = User.query.get(uid)
        return render_template('user/index.html', user=user,types=types,pagination=pagination)
    return render_template('user/index.html',types=types,pagination=pagination)


@user_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if password == repassword:
            user = User()
            user.username = username
            user.password = generate_password_hash(password)  # 使用自带的函数加密
            print(password)
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            # return redirect(url_for('user.index'))
            return redirect(url_for('user.index'))

    return render_template('user/register.html', )


# 手机号码验证
@user_bp.route('/checkphone', methods=['POST', 'GET'])
def check_phone():
    phone = request.args.get('phone')

    user = User.query.filter(User.phone == phone).all()
    print('====================', user, '==========================')
    #  code 400 不能用    200  可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')  # jsonify返回值也是Response对象
    else:
        return jsonify(code=200, msg='此号码可用')


# 用户登录
@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':  # 用户名密码登录
            username = request.form.get('username')
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()  # username 通常 做成 唯一的
            for user in users:
                flag = check_password_hash(user.password, password)
                if flag:
                    # cookie实现
                    # response=redirect(url_for('user.index'))
                    # response.set_cookie('uid',str(user.id),max_age=1800)  # max_age参数是 cookie的有效期, 以秒计算 ，默认是 尽可能长
                    # return response
                    # session机制  from flask import session  session当成字典使用
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))

            else:  # for ...else
                return render_template('user/login.html', msg='用户名或者密码有误')
        elif f == '2':  # 手机验证码登录
            phone = request.form.get('phone')
            code = request.form.get('code')
            vaild_code = session.get(phone)
            # 先比较验证码，再查数据库，否则没有意义
            if code == vaild_code:
                # 查询数据库
                user = User.query.filter(User.phone == phone).first()
                if user:
                    # 登陆成功
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user/login.html', msg='此号码未注册')
            else:
                return render_template('user/login.html', msg='验证码有误')

    return render_template('user/login.html')


@user_bp.route('logout')
def logout():
    # response=redirect(url_for('user.index'))
    # response.delete_cookie('uid')  # 删除cookie
    # return response
    #  删除 session
    # session.pop('uid')
    # del session['uid']
    session.clear()

    return redirect(url_for('user.index'))


@user_bp.route('/sendMsg')  # 发送验证码
def send_message():
    phone = request.args.get('phone')
    #  先查数据库手机号码是否注册，如果未注册则不用发验证码
    user = User.query.filter(User.phone == phone).first()
    if user:
        SECRET_ID = "a77f687582c280fe8fdbd8d364a25ebe"  # 产品密钥ID，产品标识
        SECRET_KEY = "aed71336ab9146066c6f41386a08c612"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
        BUSINESS_ID = "6bd15d1e4cbd4a38bf4f20914657addb"  # 业务ID，易盾根据产品业务特点分配
        api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
        params = {
            "mobile": phone,
            "templateId": "10084",
            "paramType": "json",
            "params": "{'a':'b'}"
        }

        ret = api.send(params)
        print(ret)
        session[phone] = '189075'  # 存储验证码
        # cache.set()
        return jsonify(code=200, msg='短信发送成功')

        # if ret is not None:
        #     if ret["code"] == 200:
        #         taskId = ret["data"]["taskId"]
        #         print("taskId = %s" % taskId)
        #         session[phone]='189075'  #   存储验证码
        #         return jsonify(code=200, msg='短信发送成功')
        #     else:
        #         print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
        #         return jsonify(code=400, msg='短信发送失败')
    else:
        return jsonify(code=400, msg='此号码未注册，请先注册')


# 用户中心
@user_bp.route('/center')
def user_center():
    types=Article_type.query.all()
    photos=Photo.query.filter(Photo.user_id==g.user.id).all()  # 获取当前登录用户的照片

    # 然后需要根据照片的名字去云存储上拿到照片的链接

    return render_template('user/center.html', user=g.user,types=types,photos=photos)


ALLOWED_EXTENSIONS = ['jpg','png','gif','bmp']  # 上传 图片的扩展名
# 用户信息修改
@user_bp.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        icon = request.files.get('icon')  # 获取文件或者图片上传的.  不局限于图片
        # print(icon)  # <FileStorage: 'gvt2tldntnj30u00u0ae8.jpg' ('image/jpeg')>
        # FileStorage 属性：    filename 文件名   方法：save() 参数传一个保存路径
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]  # 后缀
        if suffix in ALLOWED_EXTENSIONS:
            #  secure_filename 将文件名 转为一个安全的文件名。保证文件名是符合python的规则的
            #  比如上传的文件名中有一些空格，一些其他字符。需要转换文件名
            icon_name = secure_filename(icon_name)
            file_path= os.path.join(DevelopmentConfig.UPLOAD_ICON_DIR,icon_name)
            icon.save(file_path)  # 文件保存成功
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            # path=os.path.join('upload/icon',icon_name)  #
            # 用这种方式拼接路径保存在数据库中  是 upload/icon\xx.jpg，
            #   然后在模板中显示图片的时候，路径加载错误    \变成了%5C ，就显示不出来，所以我改成了下面的方式拼接路径
            path='upload/icon/'+icon_name
            user.icon=path
            db.session.commit()
            return redirect(url_for('user.user_center'))

        else:
            return render_template('user/center.html', user=g.user,msg='必须是扩展名是：jpg,png,gif,bmp格式')

        # users=User.query.all()
        # for user in users:
        #     if user.phone==phone:
        #         # 说明数据库中有该号码
        #         return render_template('user/center.html', user=g.user,msg='此号码已被注册')


    return render_template('user/center.html', user=g.user)




# 上传照片
@user_bp.route('/upload_photo',methods=['POST','GET'])
def upload_photo():
    # 获取上传的内容
    photo = request.files.get('photo')  # 返回FileStorage对象
    # photo.filename   photo.save(path)
    ret,info=upload_qiniu(photo)    # 调用自己封装的工具模块

    if info.status_code==200:
        p = Photo()
        p.photo_name=ret['key']
        p.user_id=g.user.id

        db.session.add(p)
        db.session.commit()

        return '上传成功'

    else:
        return '上传失败'




@user_bp.route('/myphoto')
def myphoto():

    # 分页
    page=int(request.args.get('page',1))
    photos=Photo.query.paginate(page=page,per_page=2)    # 所有用户的 相片
    types=Article_type.query.all()


    user_id=session.get('uid',None)
    user=None
    if user_id:
        user=User.query.get(user_id)

    return render_template('user/myphoto.html',photos=photos,user=user,types=types)



@user_bp.route('/photo_del')
def photo_del():

    photo_id=request.args.get('pid')
    photo=Photo.query.get(photo_id)

    info=del_qiniu(photo.photo_name)  # 自己封装的一个删除云存储上文件的方法

    if info.status_code==200:
        db.session.delete(photo)
        db.session.commit()

        return redirect(url_for('user.user_center'))

    else:
        return render_template('500.html',err_msg='删除相册图片失败')


#关于我模块 -------->>>> 添加
@user_bp.route('/aboutme',methods=['POST','GET'])
def about_me():

    types=Article_type.query.all()
    aboutme_content=request.form.get('aboutme').encode('utf-8')
    try:
        aboutme=AboutMe()
        aboutme.content=aboutme_content
        aboutme.user_id=g.user.id
        db.session.add(aboutme)
        db.session.commit()
    except Exception as err:
        return redirect(url_for('user.user_center'))
    else:
        return render_template('user/aboutme.html', user=g.user,types=types)


#  展示关于我
@user_bp.route('/showaboueme')
def show_aboutme():

    types=Article_type.query.all()


    return render_template('user/aboutme.html',user=g.user,types=types)



#  留言板
@user_bp.route('/board',methods=['POST','GET'])
def show_board():
    # 获取登录用户的信息部分
    uid = session.get('uid', None)
    user = None
    if uid:
        user = User.query.get(uid)

    page=int(request.args.get('page',1))
    boards=MessageBoard.query.order_by(-MessageBoard.mdatetime).paginate(page=page,per_page=5)


    if request.method=='POST':
        board=request.form.get('board')
        # 添加留言
        messageboard=MessageBoard()
        messageboard.content=board
        if uid:
            messageboard.user_id=uid
        db.session.add(messageboard)
        db.session.commit()
        return redirect(url_for('user.show_board'))

    return render_template('user/board.html',user=user,boards=boards)



# 留言删除
@user_bp.route('/board_del')
def delete_board():
    bid=request.args.get('bid')  # 留言id
    if bid:
        msgboard = MessageBoard.query.get(bid)
        db.session.delete(msgboard)
        db.session.commit()
        return redirect(url_for('user.user_center'))





@user_bp.route('/error')   # 测试 request请求中的  referer ，不属于项目的模块
def test_error():
    print(request.headers)
    print('------------')
    print(request.headers.get('Accept-Encoding'))
    referer=request.headers.get('Referer')
    return render_template('500.html',err_msg='有误',referer=referer)










