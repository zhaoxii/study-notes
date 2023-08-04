from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.user.model import *
from apps.artical.model import *
from apps.goods.model import *
from apps import create_app
from exts.sql import db

app=create_app()
manager=Manager(app=app)
migrate=Migrate(app=app,db=db)
manager.add_command('db',MigrateCommand)





if __name__=="__main__":
    manager.run()


