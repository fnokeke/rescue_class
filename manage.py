#!/usr/bin/env python

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from rescue_class import app
from rescue_class.models import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
