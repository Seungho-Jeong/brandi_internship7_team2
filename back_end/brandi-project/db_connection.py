import pymysql

from config import db


def db_connection():
    connection = pymysql.connect(
        user        = db['user'],
        passwd      = db['password'],
        host        = db['host'],
        port        = db['port'],
        db          = db['database'],
        charset     = 'utf8',
        cursorclass = pymysql.cursors.DictCursor,
    )
    return connection
