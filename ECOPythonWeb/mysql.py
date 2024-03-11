import pymysql
from datetime import datetime

#str_connection = ("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")

str_connection = ("127.0.0.1","admin","abc123xyz","prodict_database")

class MySQL(object):
    def tablelistSQL(self):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            print ("数据库连接成功！")
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            cursor.execute("SELECT TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = 'prodict_database'")
            print ("数据库查询完成！")
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            for name in data:
                print ("table_name:", name)
            # 关闭数据库连接
            db.close()
            return data
        except Exception as Argment:
            return Argment
    def tableSQL(self, tablename):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            cursor.execute("SELECT * from " + tablename + " LIMIT 1")
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            return data
        except Exception as Argment:
            return Argment
    def Get_Warning_Value(self):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句 #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_name, 7:settingID, 8:equipment_name, 9:SN_name
            # ,'-',table_equipment.num
            sql_cmd = "SELECT warning_setting.value_name, warning_setting.up_limit, warning_setting.down_limit, warning_setting.user_list, table_sn.SN_ID, "\
                      "table_warningcode.content, warning_setting.equipment_ID, warning_setting.ID, concat(table_equipment.name,'-',table_equipment.spec) as equipment_name, concat(table_sn.name,'-',table_sn.num) as SN_name "\
                      "FROM warning_setting, table_equipment, table_sn, table_warningcode "\
                      "WHERE table_warningcode.code_ID = warning_setting.warningcode_content AND "\
                      "warning_setting.equipment_ID = table_equipment.equipment_ID AND "\
                      "table_equipment.SN_ID = table_sn.SN_ID AND "\
                      "table_sn.location = 'HQ' and warning_setting.activated = '1' "
            cursor.execute(sql_cmd)
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            #print(data)
            return data
        except Exception as Argment:
            return Argment
    def Get_Warning_Value_HL(self):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句 #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_name, 7:settingID, 8:equipment_name, 9:SN_name
            # ,'-',table_equipment.num
            sql_cmd = "SELECT warning_setting.value_name, warning_setting.up_limit, warning_setting.down_limit, warning_setting.user_list, table_sn.SN_ID, "\
                      "table_warningcode.content, warning_setting.equipment_ID, warning_setting.ID, concat(table_equipment.name,'-',table_equipment.spec) as equipment_name, concat(table_sn.name,'-',table_sn.num) as SN_name "\
                      "FROM warning_setting, table_equipment, table_sn, table_warningcode "\
                      "WHERE table_warningcode.code_ID = warning_setting.warningcode_content AND "\
                      "warning_setting.equipment_ID = table_equipment.equipment_ID AND "\
                      "table_equipment.SN_ID = table_sn.SN_ID AND "\
                      "table_sn.location = 'HL' and warning_setting.activated = '1' "
            cursor.execute(sql_cmd)
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            #print(data)
            return data
        except Exception as Argment:
            return Argment
    def Get_Warning_Value_GQ(self):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句 #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_name, 7:settingID, 8:equipment_name, 9:SN_name
            # ,'-',table_equipment.num
            sql_cmd = "SELECT warning_setting.value_name, warning_setting.up_limit, warning_setting.down_limit, warning_setting.user_list, table_sn.SN_ID, "\
                      "table_warningcode.content, warning_setting.equipment_ID, warning_setting.ID, concat(table_equipment.name,'-',table_equipment.spec) as equipment_name, concat(table_sn.name,'-',table_sn.num) as SN_name "\
                      "FROM warning_setting, table_equipment, table_sn, table_warningcode "\
                      "WHERE table_warningcode.code_ID = warning_setting.warningcode_content AND "\
                      "warning_setting.equipment_ID = table_equipment.equipment_ID AND "\
                      "table_equipment.SN_ID = table_sn.SN_ID AND "\
                      "table_sn.location = 'GQ' and warning_setting.activated = '1' "
            cursor.execute(sql_cmd)
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            #print(data)
            return data
        except Exception as Argment:
            return Argment
    def Get_Value(self, value_name,lcation):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            sql_cmd = "SELECT "+value_name+" "\
                "FROM table_prodict, table_sn "\
                "WHERE table_prodict.SN = table_sn.SN_ID AND table_sn.location = 'HQ' "\
                "ORDER BY table_prodict.ID DESC LIMIT 1"
            cursor.execute(sql_cmd)
            data = cursor.fetchall()
            #sql_cmd = "SELECT warning_setting.value_name "\
            #    "FROM warning_setting, table_equipment, table_sn "\
            #    "WHERE warning_setting.equipment_ID = table_equipment.equipment_ID AND table_equipment.SN_ID = table_sn.SN_ID AND table_sn.location = 'HQ'"
            #cursor.execute(sql_cmd)
            ## 使用 fetchone() 方法获取一条数据
            #data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            return data
        except Exception as Argment:
            return Argment
    def Get_Value_HL(self, value_name):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            sql_cmd = "SELECT "+value_name+" "\
                "FROM table_prodict, table_sn "\
                "WHERE table_prodict.SN = table_sn.SN_ID AND table_sn.location = 'HL' "\
                "ORDER BY table_prodict.ID DESC LIMIT 1"
            cursor.execute(sql_cmd)
            data = cursor.fetchall()
            #sql_cmd = "SELECT warning_setting.value_name "\
            #    "FROM warning_setting, table_equipment, table_sn "\
            #    "WHERE warning_setting.equipment_ID = table_equipment.equipment_ID AND table_equipment.SN_ID = table_sn.SN_ID AND table_sn.location = 'HQ'"
            #cursor.execute(sql_cmd)
            ## 使用 fetchone() 方法获取一条数据
            #data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            return data
        except Exception as Argment:
            return Argment
    def Get_Value_GQ(self, value_name):
        # 打开数据库连接
        try:
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            sql_cmd = "SELECT "+value_name+" "\
                "FROM table_prodict, table_sn "\
                "WHERE table_prodict.SN = table_sn.SN_ID AND table_sn.location = 'GQ' "\
                "ORDER BY table_prodict.ID DESC LIMIT 1"
            cursor.execute(sql_cmd)
            data = cursor.fetchall()
            #sql_cmd = "SELECT warning_setting.value_name "\
            #    "FROM warning_setting, table_equipment, table_sn "\
            #    "WHERE warning_setting.equipment_ID = table_equipment.equipment_ID AND table_equipment.SN_ID = table_sn.SN_ID AND table_sn.location = 'HQ'"
            #cursor.execute(sql_cmd)
            ## 使用 fetchone() 方法获取一条数据
            #data = cursor.fetchall()
            # 关闭数据库连接
            db.close()
            return data
        except Exception as Argment:
            return Argment
def run_mysql():
    mysql = MySQL()
    warning_table = mysql.Get_Warning_Value()
    #print(warning_table)
    for setting_row in warning_table:
        db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        cursor = db.cursor()
        #print(setting_row)
        #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
        col = setting_row[0]
        uplimit = float(setting_row[1])
        downlimit = float(setting_row[2])
        #
        sql_cmd = "SELECT " + col + " "\
            "FROM table_current, table_sn "\
            "WHERE table_current.SN = "+str(setting_row[4])+" AND table_sn.location = 'HQ' "\
            "ORDER BY table_current.ID DESC LIMIT 1"
        cursor.execute(sql_cmd)
        data = cursor.fetchone()
        db.close()
        #print(data)
        v = float(data[0])
        if (v > uplimit or v < downlimit):
            print(col, ":", data, "不在范围内")
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            cursor = db.cursor()
            sql_cmd = "SELECT * FROM warning_log WHERE resolved_user IS NULL AND warning_setting = '" + str(setting_row[7]) + "'"
            cursor.execute(sql_cmd)
            result = cursor.fetchone()
            #data_len = result.__len__()
            if (result != None):
                sql_cmd = "UPDATE warning_log "\
                    "SET warning_status = warning_status+1 "\
                    "WHERE warning_setting = '" + str(setting_row[7]) + "'"
                cursor.execute(sql_cmd)
            else:
                sql_cmd = "INSERT INTO warning_log "\
                    "(`warningcode`, `SN`, `equipment`, `warning_setting`, `warning_status`, log_time) "\
                    "VALUES "\
                    "('" + str(setting_row[5]) + "', '" + str(setting_row[9]) + "', '" + str(setting_row[8]) + "', '" + str(setting_row[7]) + "', '0' , '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"')"
                cursor.execute(sql_cmd)
            db.commit()
            db.close()
        else:
            print(col, ":", data, "正常！")
def run_mysql_HL():
    mysql = MySQL()
    warning_table = mysql.Get_Warning_Value_HL()
    #print(warning_table)
    for setting_row in warning_table:
        db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        cursor = db.cursor()
        #print(setting_row)
        #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
        col = setting_row[0]
        uplimit = float(setting_row[1])
        downlimit = float(setting_row[2])
        #
        sql_cmd = "SELECT " + col + " "\
            "FROM table_current, table_sn "\
            "WHERE table_current.SN = "+str(setting_row[4])+" AND table_sn.location = 'HL' "\
            "ORDER BY table_current.ID DESC LIMIT 1"
        cursor.execute(sql_cmd)
        data = cursor.fetchone()
        db.close()
        #print(data)
        v = float(data[0])
        if (v > uplimit or v < downlimit):
            print(col, ":", data, "不在范围内")
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            cursor = db.cursor()
            sql_cmd = "SELECT * FROM warning_log WHERE resolved_user IS NULL AND warning_setting = '" + str(setting_row[7]) + "'"
            cursor.execute(sql_cmd)
            result = cursor.fetchone()
            #data_len = result.__len__()
            if (result != None):
                sql_cmd = "UPDATE warning_log "\
                    "SET warning_status = warning_status+1 "\
                    "WHERE warning_setting = '" + str(setting_row[7]) + "'"
                cursor.execute(sql_cmd)
            else:
                sql_cmd = "INSERT INTO warning_log "\
                    "(`warningcode`, `SN`, `equipment`, `warning_setting`, `warning_status`, log_time) "\
                    "VALUES "\
                    "('" + str(setting_row[5]) + "', '" + str(setting_row[9]) + "', '" + str(setting_row[8]) + "', '" + str(setting_row[7]) + "', '0' , '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"')"
                cursor.execute(sql_cmd)
            db.commit()
            db.close()
        else:
            print(col, ":", data, "正常！")
def run_mysql_GQ():
    mysql = MySQL()
    warning_table = mysql.Get_Warning_Value_GQ()
    #print(warning_table)
    for setting_row in warning_table:
        db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
        cursor = db.cursor()
        #print(setting_row)
        #0:value, 1:uplimit, 2:downlimit, 3:userlist, 4:SN_ID, 5:warningcode_content, 6:equipment_ID, 7:settingID, 8:equipment_name, 9:SN_name
        col = setting_row[0]
        uplimit = float(setting_row[1])
        downlimit = float(setting_row[2])
        #
        sql_cmd = "SELECT " + col + " "\
            "FROM table_current, table_sn "\
            "WHERE table_current.SN = "+str(setting_row[4])+" AND table_sn.location = 'GQ' "\
            "ORDER BY table_current.ID DESC LIMIT 1"
        cursor.execute(sql_cmd)
        data = cursor.fetchone()
        db.close()
        #print(data)
        v = float(data[0])
        if (v > uplimit or v < downlimit):
            print(col, ":", data, "不在范围内")
            db = pymysql.connect(str_connection[0], str_connection[1], str_connection[2], str_connection[3])
            cursor = db.cursor()
            sql_cmd = "SELECT * FROM warning_log WHERE resolved_user IS NULL AND warning_setting = '" + str(setting_row[7]) + "'"
            cursor.execute(sql_cmd)
            result = cursor.fetchone()
            #data_len = result.__len__()
            if (result != None):
                sql_cmd = "UPDATE warning_log "\
                    "SET warning_status = warning_status+1 "\
                    "WHERE warning_setting = '" + str(setting_row[7]) + "'"
                cursor.execute(sql_cmd)
            else:
                sql_cmd = "INSERT INTO warning_log "\
                    "(`warningcode`, `SN`, `equipment`, `warning_setting`, `warning_status`, log_time) "\
                    "VALUES "\
                    "('" + str(setting_row[5]) + "', '" + str(setting_row[9]) + "', '" + str(setting_row[8]) + "', '" + str(setting_row[7]) + "', '0' , '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"')"
                cursor.execute(sql_cmd)
            db.commit()
            db.close()
        else:
            print(col, ":", data, "正常！")
if __name__ == '__main__':
    run_mysql()
    run_mysql_HL()
    run_mysql_GQ()
    #for value_list in value_name_table:
    #    for value_name in value_list:
    #        print(mysql.Get_Value(value_name))
