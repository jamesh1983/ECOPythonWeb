##### 公共配置 #####
COOKIE_EXPIRES = 3600 # 单位s
urls = (
    '/','login',
    '/logout','logout',
    '/data','data',
    '/historical','historical',
    '/wx', 'Handle',
)
allowed = (
    ('admin','admin'),
    ('user','user'),
    ('111','111'),
    ('222','222'),
    ('123','123'),
)
# 本地环境下的MySQL配置
DBN = 'mysql'
HOST = '127.0.0.1'
PORT = 3306
DRIVER = 'mysql.connector'
DB = 'world'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'admin'

###### email服务器配置 #####
#import web
#web.config.smtp_server = 'smtp.gmail.com'
#web.config.smtp_port = 587
#web.config.smtp_username = 'your_gmail_address'
#web.config.smtp_password = 'your_gmail_password'
#web.config.smtp_starttls = True

###### 调试模式 #####
#web.config.debug = False
