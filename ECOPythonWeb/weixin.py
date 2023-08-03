import requests
import json
from datetime import datetime
import pymysql
from threading import Timer
str_connection = ("127.0.0.1","admin","abc123xyz","prodict_database")
class Wechat_Info:
    def __init__(self):
        self.appid = 'wx326ea151e11df0a0'#'wxe086481c810c615e''Ecotech1661'
        self.secret = '6b401b050b73073ab113caf2d1beafb2'#'24ff8b175f7108e42d35ccf9f67bea8a'
        self.token = None
    def get_token(self,appid, secret):
        Url = "https://api.weixin.qq.com/cgi-bin/token"
        Data = {
            "grant_type": 'client_credential',
            "appid": appid,
            "secret": secret
        }
        r = requests.get(url=Url, params=Data)
        token = r.json()['access_token']
        return token
    def send_message(self, weixinID, message):
        #妯℃澘鍙戦€?
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send"
        data = {
            "touser":weixinID,#oJsNDw7R6SPKZKNo7pyki51ub6jg
            #"template_id":"0NeybOJ7-15dc3T1YXMxaISxdDoLuapHbEdhiDItrL4",
            #"template_id":"UFEXf7fI8imOI0z7fu3hpT-C9dCb0cMGoQqdOGp_hEY",
            #"template_id":"xsjMBT-YnM06d6FG8Av2OGLna8i_dFof06pLP13Oa4Y",
            #"template_id":"h3cENoPOH_dr-IEzrCx1aTTeNipKTiDDbvcR-Q0RuEQ",
            "template_id":"UFEXf7fI8imOI0z7fu3hpT-C9dCb0cMGoQqdOGp_hEY",
            #OPENTM411243208
            "url":"https://www.baidu.com",
            "topcolor":"#FF0000",
#{{first.DATA}}
#璁惧鍚嶇О锛歿{keyword1.DATA}}
#鎶ヨ鏃堕棿锛歿{keyword2.DATA}}
#鎶ヨ绫诲瀷锛歿{keyword3.DATA}}
#{{remark.DATA}}
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
                    "value":"鏁呴殰鐮?" + message['warning_setting'],
                    "color":"#173177"
                },
                "remark":{
                    "value":message['warning_status'],
                    "color":"#173177"
                },
                "keyword4":{
                    "value":message['warning_setting'] + message['warning_status'],
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
        print(result.text)
        return result
#class weixin_message:
#    def __init__(self, *args, **kwargs):
#        self.Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        self.SN = "1"
#        self.Content = "寰俊娴嬭瘯"
#        self.Number = 123.45
#        return super().__init__(*args, **kwargs)
def run_weixin(wechat_info):
    #str_connection = ("127.0.0.1","admin","abc123xyz","prodict_database")
    #wechat_info = Wechat_Info()
    message = {'Date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'warningcode':"XXX",'SN':"1", 'equipment': "寰俊娴嬭瘯", 'warning_setting':"XXX", 'warning_status':"XXX"}
    try:
        print("start run weixin!")
        db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        cursor = db.cursor()
        sqlcmd = "SELECT warningcode, SN, equipment, warning_setting, warning_status, user_list, log_time FROM warning_log, warning_setting WHERE warning_log.warning_ack IS NULL  AND warning_setting.ID = warning_log.warning_setting"
        cursor.execute(sqlcmd)
        data = cursor.fetchall()
        db.close()
        print("read mysql complete!")
        print(data)
        if (len(data)>=1):
            for row in data:
                message['Date'] = str(row[6])
                message['warningcode'] = row[0]#鏁呴殰鐮?
                message['SN'] = row[1]#妯″潡
                message['equipment'] = row[2]#璁惧
                message['warning_setting'] = str(row[3])#鎶ヨ璁剧疆
                message['warning_status'] = "鎶ヨ宸叉寔缁?" + row[4] + "鍒嗛挓,鏈纭"#鎶ヨ鐘舵€?
                if(row[5] != None):
                    userID_List = row[5].split(',')#鎶ヨ鐢ㄦ埛
                else:
                    userID_List = ""
                if(len(userID_List)>0):
                    userDB = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    user_cursor = userDB.cursor()
                    for userID in userID_List:
                        user_cmd = "select weixinID from table_user where user_ID = '" + userID + "'"
                        user_cursor.execute(user_cmd)
                        user_data = user_cursor.fetchall()
                        weixinID = user_data[0][0]
                        print("send message to:"+weixinID)
                        wechat_info.send_message(weixinID, message)
                    userDB.close()
    except Exception as Argment:
        print(Argment)
def repeat_weixin(wechat_info,count):
    #str_connection = ("127.0.0.1","admin","abc123xyz","prodict_database")
    #wechat_info = Wechat_Info()
    message = {'Date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'warningcode':"XXX",'SN':"1", 'equipment': "寰俊娴嬭瘯", 'warning_setting':"XXX", 'warning_status':"XXX"}
    try:
        db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        cursor = db.cursor()
        sqlcmd = "SELECT warningcode, SN, equipment, warning_setting, warning_status, user_list, table_user.user_name, log_time "\
            "FROM warning_log, warning_setting, table_user "\
            "WHERE (warning_log.warning_ack IS NOT NULL AND warning_log.warning_resolved IS NULL) AND warning_log.warning_status > " + str(count) + " AND "\
            "warning_setting.ID = warning_log.warning_setting AND table_user.user_ID = warning_log.ack_user"
        cursor.execute(sqlcmd)
        data = cursor.fetchall()
        db.close()
        if (len(data)>=1):
            for row in data:
                message['Date'] = str(row[7])
                message['warningcode'] = str(row[0])#鏁呴殰鐮?
                message['SN'] = str(row[1])#妯″潡
                message['equipment'] = str(row[2])#璁惧
                message['warning_setting'] = str(row[3])#鎶ヨ璁剧疆
                message['warning_status'] = "鎶ヨ宸叉寔缁?" + str(row[4]) + "鍒嗛挓锛屽凡琚?" + str(row[6]) + "纭"#鎶ヨ鐘舵€?
                if(row[5] != None):
                    userID_List = row[5].split(',')#鎶ヨ鐢ㄦ埛
                else:
                    userID_List = ""
                if(len(userID_List)>0):
                    userDB = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
                    user_cursor = userDB.cursor()
                    for userID in userID_List:
                        user_cmd = "select weixinID from table_user where user_ID = '" + userID + "'"
                        user_cursor.execute(user_cmd)
                        user_data = user_cursor.fetchall()
                        weixinID = user_data[0][0]
                        print("repeat send message to:"+weixinID)
                        wechat_info.send_message(weixinID, message)
                    userDB.close()
    except Exception as Argment:
        print(Argment)
def TimeCounter_run(wechat_info):
    run_weixin(wechat_info)
    global t_run
    t_run = Timer(600, TimeCounter_run,(wechat_info,))
    t_run.start()
def TimeCounter_repeat(wechat_info):
    repeat_weixin(wechat_info,0)
    global t_repeat
    t_repeat = Timer(28800, TimeCounter_repeat, (wechat_info,))
    t_repeat.start()
def TimeCounter_token(wechat_info):
    get_token(wechat_info)
    global t_token
    t_token = Timer(7200, TimeCounter_token,(wechat_info,))
    t_token.start()
def get_token(wechat_info):
    wechat_info.token = wechat_info.get_token(wechat_info.appid,wechat_info.secret)
    print(wechat_info.token)
def conn_weixin():
    wechat_info = Wechat_Info()
    print("wechat_info creat successfully!")
    TimeCounter_token(wechat_info)
    print("get token complete!")
    TimeCounter_run(wechat_info)
    
    TimeCounter_repeat(wechat_info)
if __name__ == '__main__':
    conn_weixin()
    #wechat_info = Wechat_Info()
    #run_weixin(wechat_info)
