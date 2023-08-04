import flask_sqlalchemy
from flask_caching import Cache
from flask_cors import CORS

db=flask_sqlalchemy.SQLAlchemy()

cors=CORS()   # 跨域处理

cache = Cache()