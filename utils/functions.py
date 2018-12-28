# !/usr/bin/env/python
# .*. encoding:utf-8 -*-
import functools

from flask import session, url_for
from werkzeug.utils import redirect


def  get_alchemy_uri(DATABASE):
    # mysql+pymysql://root:12345@127.0.0.1:3306/flask7
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine =DATABASE['ENGINE']
    driver =DATABASE['DRIVER']
    return '%s+%s://%s:%s@%s:%s/%s' %(engine,driver,
                                      user,password,
                                      host,port,name)





def is_login(func):
    @functools.wraps(func)
    def check_status(*args,**kwargs):
        try:
            session['user_id']
        except:
            return redirect(url_for('user.login'))
        return  func(*args,**kwargs)
    return check_status

