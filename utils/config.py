# !/usr/bin/env/python
# .*. encoding:utf-8 -*-
from utils.functions import get_alchemy_uri
from utils.settings import DATABASE


class Conf():
    SQLALCHEMY_DATABASE_URI = get_alchemy_uri(DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = '1212'