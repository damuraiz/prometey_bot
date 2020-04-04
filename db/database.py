import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import json
import os.path

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.BigInteger, unique=True, nullable=False)
    telegram_chat_id = db.Column(db.BigInteger)
    test_col = db.Column(db.String(10))

    contents = relationship('Content')

    def __repr__(self):
        return "<User(id='%s', telegram_user_id='%s')>" % (self.id, self.telegram_user_id)

class Content(Base):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User")

    def __repr__(self):
        return "<Content(name='%s')>" % self.name




class Database:
    def __init__(self, config):
        self.engine = db.engine_from_config(config)

        declarative_base().metadata.create_all(self.engine)


    def test(self):
        #print('test')
        test = self.engine.execute("select 'hello'")
        for row in test:
            print(row)

if __name__ == "__main__":
    print(os.path.join('..', 'cfg', 'config.json'))
    with open(os.path.join('..', 'cfg', 'config.json')) as f:
        config = json.load(f)
        print(config)
        #print(config['database']['database'])
        database = Database(config['database'])

