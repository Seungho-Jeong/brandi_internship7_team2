import pymysql
import boto3

from config import db, AWS_ACCESS_KEY, AWS_SECRET_KEY


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


def s3_connection():
    s3 = boto3.client('s3',
                      aws_access_key_id = AWS_ACCESS_KEY,
                      aws_secret_access_key = AWS_SECRET_KEY)

    return s3