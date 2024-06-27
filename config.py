#==================================
#設定
#==================================

class Config(object):
    #debug
    DEBUG = True
    #CSRFやセッションで使用
    SECRET_KEY='secret-key'
    #警告対策
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #DB setting
    SQLALCHEMY_DATABASE_URI = 'sqlite:///regidb.sqlite'

