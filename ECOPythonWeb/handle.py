# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import random
#import pymysql
#str_connection = ("127.0.0.1","admin","abc123xyz","prodict_database")
# 连接MySQL数据库
db = web.database(dbn=settings.DBN, host=settings.HOST, port=settings.PORT,  db=settings.DB,
                  user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD, driver=settings.DRIVER,
                  buffered=True)
class Handle(object):
    def GET(self):
        try:
            data = web.input()
            print (data)
            if len(data) == 0:
                return "hello, this is handle view"
            #return data
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr

            print (data)
            token = "Ecotech1661"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()

            sha1.update(list[0].encode("utf-8"))
            sha1.update(list[1].encode("utf-8"))
            sha1.update(list[2].encode("utf-8"))
            #map(sha1.update, list)
            
            hashcode = sha1.hexdigest()
            print ("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""#success
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            #print ("Handle Post webdata is ", webData)
   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                recContent = recMsg.recText
                keyword = recContent.split('-')
                if (recContent == "绑定账号"):
                    weixinID = recMsg.FromUserName
                    userID = str(random.randint(1000000000, 1999999999))
                    result = insert_user(userID,weixinID)
                    if result == "success":
                        content = "绑定成功！报警ID为：" + userID
                    elif result == "fault":
                        content = "出错啦！"
                    else:
                        content = "用户已经绑定！ID为：" + result
                elif(len(keyword)>1 and keyword[0] == "确认"):
                    settingID = keyword[1]
                    #db_connect = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_ack = CURRENT_TIMESTAMP, warning_log.ack_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' AND table_user.weixinID = '" + toUser + "' "\
                        "AND warning_log.ack_user IS NULL"
                    #result = cursor.execute(cmd)
                    result = db.query(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    #print (result)
                    if result == None:
                        content = "报警确认失败！无此报警或报警已被确认！"
                    else:
                        content = "报警确认成功！"
                elif(len(keyword)>1 and keyword[0] == "消除"):
                    settingID = keyword[1]
                    #db_connect = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_resolved = CURRENT_TIMESTAMP, warning_log.resolved_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' and table_user.weixinID = '" + toUser + "' AND "\
                        "warning_log.resolved_user IS NULL AND warning_log.ack_user IS NOT NULL"
                    #result = cursor.execute(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    #print (result)
                    result = db.query(cmd)
                    if result == None:
                        content = "报警消除失败！无此报警或报警未确认或报警已被消除！"
                    else:
                        content = "报警消除成功！"
                elif(recContent.isdigit()):
                    settingID = recContent
                    #db_connect = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_ack = CURRENT_TIMESTAMP, warning_log.ack_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' and table_user.weixinID = '" + toUser + "' AND "\
                        "warning_log.ack_user IS NULL"
                    result = db.query(cmd)
                    #result = cursor.execute(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    #print (result)
                    content = "确认成功！"
                else:
                    content = "点击按钮'绑定账号'确认绑定操作，并生成报警ID"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'event':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                weixinID = recMsg.FromUserName
                userID = str(random.randint(1000000000, 1999999999))
                result = insert_user(userID,weixinID)
                if result == "success":
                    content = "绑定成功！报警ID为：" + userID
                elif result == "fault":
                    content = "出错啦！"
                else:
                    content = "报警处理指令错误,请重新尝试"
                #content = "回复文字'绑定账号'确认绑定操作，并生成报警ID"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            #elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'link':
            #    toUser = recMsg.FromUserName
            #    fromUser = recMsg.ToUserName
            #    content = "您发送的连接已经收到！正在调试，尽情谅解！"
            #    replyMsg = reply.TextMsg(toUser, fromUser, content)
            #    return replyMsg.send()
            else:
                print ("暂且不处理")
                return "success"
        except Exception as Argment:
            print(Argment)
            return Argment
def insert_user(userID, weixinID):
# 打开数据库连接
    try:
        # 使用cursor()方法获取操作游标 
        #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        #cursor = db.cursor()
        #cursor.execute("SELECT user_ID FROM table_user WHERE weixinID = '" + weixinID + "'")
        #exist_id_list = cursor.fetchone()
        cmd = "SELECT user_ID FROM table_user WHERE weixinID = '" + weixinID + "'"
        exist_id_list = db.query(cmd)
        if exist_id_list == None:
            # 使用execute方法执行SQL语句 replace into table( col1, col2, col3 ) values ( val1, val2, val3 )
            #result = cursor.execute("REPLACE INTO table_user (user_ID, weixinID) VALUE (" + userID + ", '" + weixinID + "')")
            #print (result)
            #db.commit()
            cmd = "REPLACE INTO table_user (user_ID, weixinID) VALUE (" + userID + ", '" + weixinID + "')"
            db.query(cmd)
            return "success"
        else:
            exist_id = exist_id_list[0]
            print (exist_id)
            return str(exist_id)
# 关闭数据库连接
        #db.close()
    except Exception as Argment:
        print (Argment)
        db.rollback()
        return "fault"
