import web
import datetime
import hashlib
import settings
import re
import datetime
#import util

# 连接MySQL数据库
db = web.database(dbn=settings.DBN, host=settings.HOST, port=settings.PORT,  db=settings.DB,
                  user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD, driver=settings.DRIVER,
                  buffered=True)
class Post:
    def count(self):
        '''获取文章总数'''
        return db.query("SELECT COUNT(*) AS count FROM posts")[0].count
    def list(self, page):
        '''获取第page页的所有文章'''
        per_page = settings.POSTS_PER_PAGE

        # 获取从offset开始共per_page个post
        offset = (page - 1) * per_page
        posts = db.query('''SELECT posts.id, title, posts.time, user_id, users.name AS username
                            FROM posts JOIN users
                            ON posts.user_id = users.id
                            ORDER BY posts.id DESC
                            LIMIT %d OFFSET %d''' % (per_page, offset))
        page_posts = []
        for p in posts:
            comment = Comment(p.id)
            last = comment.last()
            last_time = last.time if last else p.time
            page_posts.append({'id': p.id, 'title': p.title, 'userid': p.user_id, 'username': p.username,
            'comment_count': comment.count(), 'last_time': last_time})

        # 计算总页数
        post_count = self.count()
        page_count = post_count // per_page
        if post_count % per_page > 0:
            page_count += 1

        return (page_posts, page_count)
    def new(self, title, content, user_id):
        if user_id:
            return db.insert('posts', title=title, content=content, user_id=user_id)
        else:
            return 0
    def view(self, id):
        '''获取id对应的文章'''
        posts = db.query('''SELECT posts.id, title, content, posts.time, user_id, users.name AS username, users.picture AS user_face
                            FROM posts JOIN users
                            ON posts.user_id = users.id
                            WHERE posts.id = %d''' % id)
        if posts:
            return posts[0]

        return None       
    def digest_list(self, user_id):
        '''获取user_id对应作者的文章列表'''
        posts = db.query('''SELECT id, title, time FROM posts
                            WHERE user_id=%d
                            ORDER BY id DESC''' % user_id)
        return posts
    def update(self, id, title, content): 
        '''更新文章'''
        try:
            db.update('posts', where='id=$id', title=title, content=content, vars=locals())
            return True
        except Exception as e:
            print(e)
            return False
    def ddel(self, id):
        try:
            db.delete('posts', where='id=$id', vars=locals())          
        except Exception as e:
            print(e)
class User:
    def current_id(self):
        '''当前登录用户的id'''
        user_id = 0
        try:
            if web.cookies().get('user_id') != None:
                user_id = int(web.cookies().get('user_id'))
            else:
                user_id = 0
        except Exception as e:
            print(e)
        else:
            # 刷新cookie
            web.setcookie('user_id', str(user_id), settings.COOKIE_EXPIRES)
        finally:
            return user_id
    def new(self, email, username, password):
        pwdhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return db.insert('users', email=email, name=username, password=pwdhash,
                         picture='/static/img/user_normal.jpg', description='')
    def status(self, id):
        '''查询id对应的用户信息'''
        email = ''
        username = ''
        password_hash = ''
        picture = ''
        description = ''

        users = db.query('SELECT email, name, password, picture, description FROM users WHERE id=%d' % id)
        if users:
            u = users[0]
            email = u.email
            username = u.name
            password_hash = u.password
            picture = u.picture
            description = u.description

        return {'email': email, 'username': username, 'password_hash': password_hash,
                'picture': picture, 'description': description}
    
    def login(self, username, password):
        '''登录验证'''
        pwdhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        users = db.select('users', what='id', where='name=$username AND password=$pwdhash', vars=locals())
        for user in users:
            if user:               
                return user['id']            
            else:
                return 0
    def update(self, id, **kwd):
        try:
            if 'email' in kwd and kwd['email']:
                db.update('users', where='id=$id', email=kwd['email'], vars=locals())

            if 'password' in kwd and kwd['password']:
                pwdhash = hashlib.md5(kwd['password']).hexdigest()
                db.update('users', where='id=$id', password=pwdhash, vars=locals())

            if 'picture' in kwd and kwd['picture']:
                db.update('users', where='id=$id', picture=kwd['picture'], vars=locals())

            if 'description' in kwd and kwd['description']:
                db.update('users', where='id=$id', description=kwd['description'], vars=locals())

            return True
        except Exception as e:
            print(e)
            return False
    def matched_id(self, **kwd):
        '''根据kwd指定的查询条件，搜索数据库'''
        users = db.select('users', what='id', where=web.db.sqlwhere(kwd, grouping='OR'))
        if users:
            # 目前只用于单条记录查询，因此只取第一个
            u = users[0]
            return u.id
        else:
            return 0
class Comment:
    def __init__(self, post_id):
        '''一个Comment实例只对应一篇文章'''
        self.__parent_id = post_id

    def quote(self, comments):
        '''为每个评论获取父评论（即引用，只处理一级）'''
        comments_with_quote = []
        for c in comments:
            quote_content = ''
            quote_username = ''
            quote_user_id = 0
            if c.quote_id:
                quotes = db.query('''SELECT content, users.name AS username, user_id
                                       FROM comments JOIN users
                                       ON comments.user_id = users.id
                                       WHERE comments.id=%d''' % c.quote_id)
                if quotes:
                    q = quotes[0]
                    quote_content = q.content
                    quote_username = q.username
                    quote_user_id = q.user_id
            comments_with_quote.append({'id': c.id, 'content': c.content, 'user_id': c.user_id, 'username': c.username,
                                        'user_face': c.user_face, 'time': c.time, 'quote_content': quote_content,
                                        'quote_username': quote_username, 'quote_user_id': quote_user_id})
        return comments_with_quote

    def new(self, content, user_id, quote_id):
        try:
            return db.insert('comments', content=content, user_id=user_id, parent_id=self.__parent_id, quote_id=quote_id)
        except Exception as e:
            print(e)
            return 0

    def ddel(self):
        try:
            #db.delete('comments', where='parent_id=$self.__parent_id', vars=locals())
            db.query('DELETE FROM comments WHERE parent_id=%d' % self.__parent_id)
        except Exception as e:
            print(e)

    def list(self):
        '''获取当前文章（创建Comment实例时指定了post_id）下面的所有评论'''
        comments = db.query('''SELECT comments.id, content, comments.time, users.name AS username, user_id, quote_id, users.picture AS user_face
                               FROM comments JOIN users
                               ON comments.user_id = users.id
                               WHERE comments.parent_id=%d
                               ORDER BY comments.id''' % self.__parent_id)
        return comments

    def last(self):
        '''获取当前文章下面的最新评论'''
        last_comments = db.query('''SELECT comments.id, content, comments.time, users.name AS username, user_id, quote_id, users.picture AS user_face
                                    FROM comments JOIN users
                                    ON comments.user_id = users.id
                                    WHERE comments.id=(SELECT MAX(id) FROM comments WHERE parent_id=%d)''' % self.__parent_id)
        if last_comments:
            return last_comments[0]

        return None

    def count(self):
        '''获取当前文章下面的评论总数'''
        result = db.query("SELECT COUNT(*) AS count FROM comments WHERE parent_id=%d" % self.__parent_id)
        for i in result:
                return i.count
        return 0
class CurrentData:
    def getColumnList():
        try:
            list = db.query('SELECT column_name, comments, comments_for_HL FROM column_list')
            columnlist = {}
            column_name = []
            comments = []
            comments_for_HL = []
            for row in list:
                column_name.append(row.column_name)
                comments.append(row.comments)
                comments_for_HL.append(row.comments_for_HL)
            columnlist["column_name"] = column_name
            columnlist["comments"] = comments
            columnlist["comments_for_HL"] = comments_for_HL
            return columnlist
            #return list
        except Exception as e:
            print(e)
            return None
    def getCurrentData(sn):
        try:
            result = db.query('SELECT * FROM table_current WHERE SN = ' + str(sn) + ' ORDER BY ID DESC LIMIT 1')
            return dict(result[0])
        except Exception as e:
            print(e)
            return None
    def getHisData(sn, column, starttime, endtime):
        resultdata = {"TIMETAG":[],"result":[]}
        try:
            results = db.query('SELECT TIMETAG, ' + column + ' as result FROM table_prodict WHERE SN = ' + str(sn) + ' AND TIMETAG BETWEEN "' + starttime + '" AND "' + endtime + '"')
            for result in results:
                datetime_inf = int(result.TIMETAG.strftime('%Y%m%d%H%M'))
                num_value = result.result
                resultdata["TIMETAG"].append(datetime_inf)
                resultdata["result"].append(num_value)
            return resultdata
        except Exception as e:
            print(e)
            return None
    def getPreData(sn):
        resultdata = {"TIMETAG":[],"result1":[],"result2":[],"result3":[],"warningvalue":[],"num":[]}
        try:
            if (sn == 1) | (sn == 2):
                results = db.query('SELECT TIMETAG, result1, result2, round((kvalue*@num1+ bvalue), 2) as result3, warningvalue, (@num1:= @num1+ 1) as num FROM (SELECT TIMETAG,round(avg(Value5), 2) as result1, round(avg(Value3), 2) as result2 FROM table_prodict WHERE SN= ' + str(sn) + ' AND Value5 > 200 AND date_sub(CURDATE(), INTERVAL 7 DAY) <= date(TIMETAG) Group BY year(TIMETAG), month(TIMETAG), date(TIMETAG), hour(TIMETAG)) a, (SELECT kvalue, bvalue, warningvalue FROM table_result WHERE SN= ' + str(sn) + ' AND MD= 1 And period= 7 ORDER BY ID DESC LIMIT 1) b, (SELECT(@num1:= 0)) c')
            elif sn == 3:
                results = db.query('SELECT TIMETAG, result1, result2, round((kvalue*@num1+ bvalue), 2) as result3, warningvalue, (@num1:= @num1+ 1) as num FROM (SELECT TIMETAG,round(avg(Value4), 2) as result1, round(avg(Value5-Value6), 2) as result2 FROM table_prodict WHERE SN= ' + str(sn) + ' AND Value4 > 0.1 AND date_sub(CURDATE(), INTERVAL 7 DAY) <= date(TIMETAG) Group BY year(TIMETAG), month(TIMETAG), date(TIMETAG), hour(TIMETAG)) a, (SELECT kvalue, bvalue, warningvalue FROM table_result WHERE SN= ' + str(sn) + ' AND MD= 1 And period= 7 ORDER BY ID DESC LIMIT 1) b, (SELECT(@num1:= 0)) c')
            else:
                results = None
            for result in results:
                datetime_inf = int(result.TIMETAG.strftime('%Y%m%d%H%M'))
                FH_value = result.result1
                DX_value = result.result2
                k_value = result.result3
                warning = result.warningvalue
                num_value = result.num
                resultdata["TIMETAG"].append(datetime_inf)
                resultdata["result1"].append(FH_value)
                resultdata["result2"].append(DX_value)
                resultdata["result3"].append(k_value)
                resultdata["warningvalue"].append(warning)
                resultdata["num"].append(num_value)
            return resultdata
        except Exception as e:
            print(e)
            return None
