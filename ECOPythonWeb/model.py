# -*- coding: utf-8 -*-
# filename: main.py
import web
import time
import hashlib
import settings
import re
import xml.etree.ElementTree as ET
import requests
import json
import random
from threading import Timer
from datetime import datetime
# 连接MySQL数据库
db = web.database(dbn=settings.DBN, host=settings.HOST, port=settings.PORT,  db=settings.DB, user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD, driver=settings.DRIVER)
class CurrentData:
    def getColumnList():
        try:
            cmd = 'SELECT column_name, comments, comments_for_HL FROM column_list'
            list = db.query(cmd)
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
            cmd = 'SELECT * FROM table_current WHERE SN = ' + str(sn) + ' ORDER BY ID DESC LIMIT 1'
            result = db.query(cmd)
            return dict(result[0])
        except Exception as e:
            print(e)
            return None
    def getHisData(sn, column, starttime, endtime):
        resultdata = {"TIMETAG":[],"result":[]}
        try:
            cmd = 'SELECT TIMETAG, ' + column + ' as result FROM table_prodict WHERE SN = ' + str(sn) + ' AND TIMETAG BETWEEN "' + starttime + '" AND "' + endtime + '"'
            results = db.query(cmd)
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
                datetime_inf = int(result.TIMETAG.strftime('%Y%m%d%H'))
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
class Msg_RLY(object):
    def __init__(self):
        pass
    def send(self):
        return "success"
class TextMsg_RLY(Msg_RLY):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
class LinkMsg_RLY(Msg_RLY):
    def __init__(self, toUserName, fromUserName, title, description, url):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Title'] = title
        self.__dict['Description '] = description
        self.__dict['Url'] = url
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <Url><![CDATA[{url}]]></Url>
        </xml>
        """
        return XmlForm.format(**self.__dict)
class ImageMsg_RLY(Msg_RLY):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)
class Msg_REC(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
class TextMsg_REC(Msg_REC):
    def __init__(self, xmlData):
        Msg_REC.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.recText = xmlData.find('Content').text
class ImageMsg_REC(Msg_REC):
    def __init__(self, xmlData):
        Msg_REC.__init__(self, xmlData)
class EventMsg_REC(Msg_REC):
    def __init__(self, xmlData):
        Msg_REC.__init__(self, xmlData)
        self.Event = xmlData.find('Event').text
        self.EventKey = xmlData.find('EventKey').text
class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            return data
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            #print (data)
            token = "Ecotech1661"
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode("utf-8"))
            sha1.update(list[1].encode("utf-8"))
            sha1.update(list[2].encode("utf-8"))
            hashcode = sha1.hexdigest()
            #print ("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return ""
            else:
                return "success"
        except Exception as Argument:
            print(Argment)
            return None
    def POST(self):
        try:
            webData = web.data()
            #print ("Handle Post webdata is ", webData)
   #后台打日志
            recMsg = parse_xml(webData)
            if isinstance(recMsg, Msg_REC) and recMsg.MsgType == 'text':
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
                    #db_connect = pymysql.connect("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_ack = CURRENT_TIMESTAMP, warning_log.ack_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' and table_user.weixinID = '" + toUser + "'"
                    #result = cursor.execute(cmd)
                    result = db.query(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    #print (result)
                    content = "确认成功！"
                elif(len(keyword)>1 and keyword[0] == "消除"):
                    settingID = keyword[1]
                    #db_connect = pymysql.connect("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_resolved = CURRENT_TIMESTAMP, warning_log.resloved_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' and table_user.weixinID = '" + toUser + "'"
                    #result = cursor.execute(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    result = db.query(cmd)
                    #print (result)
                    content = "消除成功！"
                elif(recContent.isdigit()):
                    settingID = recContent
                    #db_connect = pymysql.connect("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
                    #cursor = db_connect.cursor()
                    cmd = "UPDATE warning_log, table_user SET warning_ack = CURRENT_TIMESTAMP, warning_log.ack_user = table_user.user_ID "\
                        "WHERE warning_log.warning_setting = '" + settingID + "' and table_user.weixinID = '" + toUser + "'"
                    #result = cursor.execute(cmd)
                    #db_connect.commit()
                    #db_connect.close()
                    result = db.query(cmd)
                    #print (result)
                    content = "确认成功！"
                else:
                    content = "点击按钮'绑定账号'确认绑定操作，并生成报警ID"
                replyMsg = TextMsg_RLY(toUser, fromUser, content)
                return replyMsg.send()
            elif isinstance(recMsg, Msg_REC) and recMsg.MsgType == 'event':
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
                    content = "用户已经绑定！ID为：" + result
                #content = "回复文字'绑定账号'确认绑定操作，并生成报警ID"
                replyMsg = TextMsg_RLY(toUser, fromUser, content)
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
            return None
class Wechat_Info:
    def __init__(self):
        self.appid = 'wx326ea151e11df0a0'
        self.secret = '6b401b050b73073ab113caf2d1beafb2'
        self.token = None
    def get_token(self,appid, secret):
        Url = "https://api.weixin.qq.com/cgi-bin/token"
        Data = {
            "grant_type": 'client_credential',
            "appid": appid,
            "secret": secret
        }
        r = requests.get(url=Url, params=Data)
        try:
            token = r.json()['access_token']
            #print("the token return as: " + token)
            return token
        except Exception as Argment:
            print(Argment)
            return None
    def send_message(self, weixinID, message):
        #模板发送
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send"
        data = {
            "touser":weixinID,#oJsNDw7R6SPKZKNo7pyki51ub6jg
            #"template_id":"0NeybOJ7-15dc3T1YXMxaISxdDoLuapHbEdhiDItrL4",
            #"template_id":"9sqHT3HSLuJdESQ5rPi9rErb-tiE60sSJp7Kpoj6oAY",
            #"UFEXf7fI8imOI0z7fu3hpT-C9dCb0cMGoQqdOGp_hEY"
            "template_id":"UFEXf7fI8imOI0z7fu3hpT-C9dCb0cMGoQqdOGp_hEY",
            "url":" ",
            "topcolor":"#FF0000",
            "data":{
                "keyword3": {
                    "value":message['Date'],
                    "color":"#173177"
                },
                "keyword2":{
                    "value":message['warningcode'],
                    "color":"#173177"
                },
                "keyword1":{
                    "value":message['SN'] + message['equipment'],
                    "color":"#173177"
                },
                "first":{
                    "value":"故障码" + message['warning_setting'],
                    "color":"#173177"
                },
                "remark":{
                    "value":message['warning_status'],
                    "color":"#173177"
                },
                "keyword4":{
                    "value":"故障码:" + message['warning_setting'] + "-" + message['warning_status'],
                    "color":"#173177"
                }
            }
        }
        #result = requests.post(url=url, 
        #                       params={'access_token':self.__get_token(self.appid, self.secret)},
        #                       data=json.dumps(data))
        result = requests.post(url=url, 
                               params={'access_token': self.token},
                               data=json.dumps(data))
        #json.JSONEncoder().encode(data)
        return result
class MySQL(object):
    def tablelistSQL(self):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #print ("数据库连接成功！")
            # 使用cursor()方法获取操作游标 
            #cursor = db.cursor()
            # 使用execute方法执行SQL语句
            #cursor.execute("SELECT TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = 'prodict_database'")
            #print ("数据库查询完成！")
            ## 使用 fetchone() 方法获取一条数据
            #data = cursor.fetchall()
            cmd = "SELECT TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = 'prodict_database'"
            data = db.query(cmd)
            #for name in data:
                #print ("table_name:", name)
            # 关闭数据库连接
            #db.close()
            return data
        except Exception as Argment:
            print(Argment)
            return None
    def tableSQL(self, tablename):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            #cursor.execute("SELECT * from " + tablename + " LIMIT 1")
            #data = cursor.fetchall()
            #db.close()
            cmd = "SELECT * from " + tablename + " LIMIT 1"
            data = db.query(cmd)
            return data
        except Exception as Argment:
            print(Argment)
            return None
    def Get_Warning_Value(self):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            # 使用execute方法执行SQL语句 #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_name, 7:settingID, 8:equipment_name, 9:SN_name
            sql_cmd = "SELECT warning_setting.value_name, warning_setting.up_limit, warning_setting.down_limit, warning_setting.user_list, table_sn.SN_ID, "\
                      "table_warningcode.content, warning_setting.equipment_ID, warning_setting.ID, concat(table_equipment.name,'-',table_equipment.spec) as equipment_name, table_sn.name as SN_name "\
                      "FROM warning_setting, table_equipment, table_sn, table_warningcode "\
                      "WHERE table_warningcode.code_ID = warning_setting.warningcode_content AND "\
                      "warning_setting.equipment_ID = table_equipment.equipment_ID AND "\
                      "table_equipment.SN_ID = table_sn.SN_ID AND "\
                      "table_sn.location = 'HQ' and warning_setting.activated = '1' "
            #cursor.execute(sql_cmd)
            #data = cursor.fetchall()
            #db.close()
            data = db.query(sql_cmd)
            return data
        except Exception as Argment:
            print(Argment)
            return None
    def Get_Value(self, value_name):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            # 使用execute方法执行SQL语句
            sql_cmd = "SELECT "+value_name+" "\
                "FROM table_prodict, table_sn "\
                "WHERE table_prodict.SN = table_sn.SN_ID AND table_sn.location = 'HQ' "\
                "ORDER BY table_prodict.ID DESC LIMIT 1"
            #cursor.execute(sql_cmd)
            #data = cursor.fetchall()
            #db.close()
            data = db.query(sql_cmd)
            return data
        except Exception as Argment:
            print(Argment)
            return None
    def Get_Warning_Value_HL(self):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            # 使用execute方法执行SQL语句 #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_name, 7:settingID, 8:equipment_name, 9:SN_name
            sql_cmd = "SELECT warning_setting.value_name, warning_setting.up_limit, warning_setting.down_limit, warning_setting.user_list, table_sn.SN_ID, "\
                      "table_warningcode.content, warning_setting.equipment_ID, warning_setting.ID, concat(table_equipment.name,'-',table_equipment.spec) as equipment_name, table_sn.name as SN_name "\
                      "FROM warning_setting, table_equipment, table_sn, table_warningcode "\
                      "WHERE table_warningcode.code_ID = warning_setting.warningcode_content AND "\
                      "warning_setting.equipment_ID = table_equipment.equipment_ID AND "\
                      "table_equipment.SN_ID = table_sn.SN_ID AND "\
                      "table_sn.location = 'HL' and warning_setting.activated = '1' "
            #cursor.execute(sql_cmd)
            #data = cursor.fetchall()
            #db.close()
            data = db.query(sql_cmd)
            return data
        except Exception as Argment:
            print(Argment)
            return None
    def Get_Value_HL(self, value_name):
        # 打开数据库连接
        try:
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            # 使用execute方法执行SQL语句
            sql_cmd = "SELECT "+value_name+" "\
                "FROM table_prodict, table_sn "\
                "WHERE table_prodict.SN = table_sn.SN_ID AND table_sn.location = 'HL' "\
                "ORDER BY table_prodict.ID DESC LIMIT 1"
            #cursor.execute(sql_cmd)
            #data = cursor.fetchall()
            #db.close()
            data = db.query(sql_cmd)
            return data
        except Exception as Argment:
            print(Argment)
            return None
def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg_REC(xmlData)
    elif msg_type == 'image':
        return ImageMsg_REC(xmlData)
    elif msg_type == 'event':
        return EventMsg_REC(xmlData)
def run_weixin(wechat_info):
    #str_connection = ("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
    #wechat_info = Wechat_Info()
    message = {'Date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'warningcode':"XXX",'SN':"1", 'equipment': "微信测试", 'warning_setting':"XXX", 'warning_status':"XXX"}
    try:
        #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        #cursor = db.cursor()
        sqlcmd = "SELECT warningcode, SN, equipment, warning_setting, warning_status, user_list FROM warning_log, warning_setting WHERE warning_log.warning_ack IS NULL  AND warning_setting.ID = warning_log.warning_setting"
        #cursor.execute(sqlcmd)
        #data = cursor.fetchall()
        #db.close()
        data = db.query(sqlcmd)
        if (len(data)>=1):
            for row in data:
                message['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message['warningcode'] = str(row["warningcode"])#故障码
                message['SN'] = str(row["SN"])#模块
                message['equipment'] = str(row["equipment"])#设备
                message['warning_setting'] = str(row["warning_setting"])#报警设置
                message['warning_status'] = "报警已持续" + str(row["warning_status"]) + "分钟,未被确认"#报警状态
                if(row["user_list"] != None):
                    userID_List = row["user_list"].split(',')#报警用户
                else:
                    userID_List = ""
                if(len(userID_List)>0):
                    #userDB = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    #user_cursor = userDB.cursor()
                    for userID in userID_List:
                        user_cmd = "select weixinID from table_user where user_ID = '" + userID + "'"
                        #user_cursor.execute(user_cmd)
                        #user_data = user_cursor.fetchall()
                        result = db.query(user_cmd)
                        for user_data in result:
                            weixin = user_data["weixinID"]
                            wechat_info.send_message(weixin, message)
                    #userDB.close()
    except Exception as Argment:
        print(Argment)
        return None
def repeat_weixin(wechat_info,count):
    #str_connection = ("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
    #wechat_info = Wechat_Info()
    message = {'Date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'warningcode':"XXX",'SN':"1", 'equipment': "微信测试", 'warning_setting':"XXX", 'warning_status':"XXX"}
    try:
        #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        #cursor = db.cursor()
        sqlcmd = "SELECT warningcode, SN, equipment, warning_setting, warning_status, user_list, table_user.user_name, log_time "\
            "FROM warning_log, warning_setting, table_user "\
            "WHERE (warning_log.warning_ack IS NOT NULL AND warning_log.warning_resolved IS NULL) AND warning_log.warning_status > " + str(count) + " AND "\
            "warning_setting.ID = warning_log.warning_setting AND table_user.user_ID = warning_log.ack_user"
        #cursor.execute(sqlcmd)
        #data = cursor.fetchall()
        #db.close()
        data = db.query(sqlcmd)
        if (len(data)>=1):
            for row in data:
                message['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message['warningcode'] = str(row["warningcode"])#故障码
                message['SN'] = str(row["SN"])#模块
                message['equipment'] = str(row["equipment"])#设备
                message['warning_setting'] = str(row["warning_setting"])#报警设置
                message['warning_status'] = "报警已持续" + str(row["warning_status"]) + "分钟，已被" + str(row["user_name"]) + "确认"#报警状态
                if(row["user_list"] != None):
                    userID_List = row["user_list"].split(',')#报警用户
                else:
                    userID_List = ""
                if(len(userID_List)>0):
                    #userDB = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    #user_cursor = userDB.cursor()
                    for userID in userID_List:
                        user_cmd = "select weixinID from table_user where user_ID = '" + userID + "'"
                        #user_cursor.execute(user_cmd)
                        #user_data = user_cursor.fetchall()
                        result = db.query(user_cmd)
                        for user_data in result:
                            weixin = user_data["weixinID"]
                            wechat_info.send_message(weixin, message)
                    #userDB.close()
    except Exception as Argment:
        print(Argment)
        return None
def TimeCounter_run(wechat_info):
    run_weixin(wechat_info)
    global t_run
    t_run = Timer(600, TimeCounter_run,(wechat_info,))
    t_run.start()
def TimeCounter_repeat(wechat_info):
    repeat_weixin(wechat_info,1440)
    global t_repeat
    t_repeat = Timer(600, TimeCounter_repeat, (wechat_info,))
    t_repeat.start()
def TimeCounter_token(wechat_info):
    get_token(wechat_info)
    global t_token
    t_token = Timer(7200, TimeCounter_token,(wechat_info,))
    t_token.start()
def get_token(wechat_info):
    wechat_info.token = wechat_info.get_token(wechat_info.appid,wechat_info.secret)
    #print(wechat_info.token)
def insert_user(userID, weixinID):
# 打开数据库连接
    try:
        #db = pymysql.connect("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
        #cursor = db.cursor()
        #cursor.execute("SELECT user_ID FROM table_user WHERE weixinID = '" + weixinID + "'")
        #exist_id_list = cursor.fetchone()
        cmd = "SELECT user_ID FROM table_user WHERE weixinID = '" + weixinID + "'"
        exist_id_list = db.query(cmd)
        if exist_id_list == None:
            # 使用execute方法执行SQL语句 replace into table( col1, col2, col3 ) values ( val1, val2, val3 )
            result = cursor.execute("REPLACE INTO table_user (user_ID, weixinID) VALUE (" + userID + ", '" + weixinID + "')")
            #print (result)
            #db.commit()
            return "success"
        else:
            exist_id = exist_id_list[0]
            return str(exist_id)
# 关闭数据库连接
        #db.close()
    except Exception as Argment:
        print (Argment)
        #db.rollback()
        return "fault"
def conn_weixin():
    wechat_info = Wechat_Info()
    TimeCounter_token(wechat_info)
    TimeCounter_run(wechat_info)
    TimeCounter_repeat(wechat_info)
def run_mysql():
    mysql = MySQL()
    warning_table = mysql.Get_Warning_Value()
    #print(warning_table)
    for setting_row in warning_table:
        #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        #cursor = db.cursor()
        #print(setting_row)
        #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
        col = setting_row["value_name"]
        uplimit = float(setting_row["up_limit"])
        downlimit = float(setting_row["down_limit"])
        #
        sql_cmd = "SELECT " + col + " "\
            "FROM table_current, table_sn "\
            "WHERE table_current.SN = "+str(setting_row["SN_ID"])+" AND table_sn.location = 'HQ' "\
            "ORDER BY table_current.ID DESC LIMIT 1"
        #cursor.execute(sql_cmd)
        #data = cursor.fetchone()
        #db.close()
        #print(data)
        data = db.query(sql_cmd)
        v = float(data[0][col])
        if (v > uplimit or v < downlimit):
            print(col, ":", v, "不在范围内")
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            sql_cmd = "SELECT * FROM warning_log WHERE resolved_user IS NULL AND warning_setting = '" + str(setting_row["ID"]) + "'"
            #cursor.execute(sql_cmd)
            #result = cursor.fetchone()
            #data_len = result.__len__()
            results = db.query(sql_cmd)
            if (results.cursor.rowcount != 0):
                sql_cmd = "UPDATE warning_log "\
                    "SET warning_status = warning_status+1 "\
                    "WHERE warning_setting = '" + str(setting_row["ID"]) + "'"
                #cursor.execute(sql_cmd)
                db.query(sql_cmd)
            else:
                sql_cmd = "INSERT INTO warning_log "\
                    "(`warningcode`, `SN`, `equipment`, `warning_setting`, `warning_status`) "\
                    "VALUES "\
                    "('" + str(setting_row["content"]) + "', '" + str(setting_row["SN_name"]) + "-" + str(setting_row["SN_ID"]) + "', '" + str(setting_row["equipment_name"]) + "', '" + str(setting_row["ID"]) + "', '0')"
                #cursor.execute(sql_cmd)
                db.query(sql_cmd)
                #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
            #db.commit()
            #db.close()
        else:
            print(col, ":", v, "正常！")
def run_mysql_HL():
    mysql = MySQL()
    warning_table = mysql.Get_Warning_Value_HL()
    #print(warning_table)
    for setting_row in warning_table:
        #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        #cursor = db.cursor()
        #print(setting_row)
        #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
        col = setting_row["value_name"]
        uplimit = float(setting_row["up_limit"])
        downlimit = float(setting_row["down_limit"])
        #
        sql_cmd = "SELECT " + col + " "\
            "FROM table_current, table_sn "\
            "WHERE table_current.SN = "+str(setting_row["SN_ID"])+" AND table_sn.location = 'HL' "\
            "ORDER BY table_current.ID DESC LIMIT 1"
        #cursor.execute(sql_cmd)
        #data = cursor.fetchone()
        #db.close()
        #print(data)
        data = db.query(sql_cmd)
        v = float(data[0][col])
        if (v > uplimit or v < downlimit):
            print(col, ":", v, "不在范围内")
            #db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            #cursor = db.cursor()
            sql_cmd = "SELECT * FROM warning_log WHERE resolved_user IS NULL AND warning_setting = '" + str(setting_row["ID"]) + "'"
            #cursor.execute(sql_cmd)
            #result = cursor.fetchone()
            #data_len = result.__len__()
            results = db.query(sql_cmd)
            if (results.cursor.rowcount != 0):
                sql_cmd = "UPDATE warning_log "\
                    "SET warning_status = warning_status+1 "\
                    "WHERE warning_setting = '" + str(setting_row["ID"]) + "'"
                #cursor.execute(sql_cmd)
                result = db.query(sql_cmd)
            else:
                sql_cmd = "INSERT INTO warning_log "\
                    "(`warningcode`, `SN`, `equipment`, `warning_setting`, `warning_status`) "\
                    "VALUES "\
                    "('" + str(setting_row["content"]) + "', '" + str(setting_row["SN_name"]) + "', '" + str(setting_row["equipment_name"]) + "', '" + str(setting_row["ID"]) + "', '0')"
                #cursor.execute(sql_cmd)
                result = db.query(sql_cmd)
            #db.commit()
            #db.close()
        else:
            print(col, ":", v, "正常！")


