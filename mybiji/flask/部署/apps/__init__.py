from flask import Flask
import config
from apps.artical.view import article_bp
from apps.artical.views import article_bp1
from apps.goods.view import goods_bp
from apps.user.view import user_bp
from exts import bootstrap, cache
from exts.sql import db
cache_config={
    'CACHE_TYPE':'redis',
    'CACHE_REDIS_HOST':'127.0.0.1',
    'CACHE_REDIS_PORT':6379
}



def create_app():
    app=Flask(__name__,template_folder='../templates',static_folder='../static')
    app.config.from_object(config.DevelopmentConfig)
    db.init_app(app)
    app.register_blueprint(article_bp)
    app.register_blueprint(goods_bp)
    bootstrap(app=app)
    # bootstrap.init_app(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp1)

    # 初始化缓存文件
    cache.init_app(app=app,config=cache_config)

    # print(app.url_map)
    return app



