# -*- coding: utf-8 -*-
# filename: settings.py
##### 公共配置 #####
COOKIE_EXPIRES = 3600 # 单位s
urls = (
    '/','login',
    '/logout','logout',
    '/historical','historical',
    '/wx', 'Handle',
    '/calendar', 'calendar',
)
allowed = (
    ('111','111'),
    ('222','222'),
    ('333','333'),
    ('444','444'),
)
auth = {
    "111":1,
    "222":1,
    "333":3,
    "444":4,
    }
# 本地环境下的MySQL配置
DBN = 'mysql'
HOST = '47.101.51.101'
PORT = 3306
DRIVER = 'MySQLdb'
DB = 'prodict_database'
MYSQL_USERNAME = 'admin'
MYSQL_PASSWORD = 'abc123xyz'

###### email服务器配置 #####
#import web
#web.config.smtp_server = 'smtp.gmail.com'
#web.config.smtp_port = 587
#web.config.smtp_username = 'your_gmail_address'
#web.config.smtp_password = 'your_gmail_password'
#web.config.smtp_starttls = True

###### 调试模式 #####
#web.config.debug = False
