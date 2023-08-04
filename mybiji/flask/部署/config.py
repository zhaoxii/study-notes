import os


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flaskblog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    #  session 配置
    SECRET_KEY='ASDFAAGFAFDS'
    # 项目路径
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径配置
    STATIC_DIR=os.path.join(BASE_DIR,'static')
    TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')
    UPLOAD_ICON_DIR=os.path.join(STATIC_DIR,'upload/icon')  # 头像上传目录
    UPLOAD_PHOTO_DIR=os.path.join(STATIC_DIR,'upload/photo')  # 相册上传目录


class DevelopmentConfig(Config):
    ENV='development'
    DEBUG=True




if __name__=='__main__':
    print(Config.BASE_DIR)
    print(os.path.abspath(__file__))

