# coding=utf-8

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json
import os.path

with open(os.path.join('cfg', 'config.json')) as f:
    config = json.load(f)

engine = engine_from_config(config['database'])

Session = sessionmaker(bind=engine)

Base = declarative_base()