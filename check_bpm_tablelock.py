import datetime
import os
import pyodbc
import time

from lineNotifyMessage import lineNotifyMessage

class BPM(object):

    cnxn = None

    def __init__(self):
        server = 'tcp:10.77.9.4'
        database = 'EFGP'
        username = 'sa'
        password = 'Sql#dsc2019'
        self.cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


    def Check_bpm_tablelock(self):
        result = False
        cursor = self.cnxn.cursor()

        sql = """select request_session_id lock_process,OBJECT_NAME(resource_associated_entity_id) lock_table  
                  from sys.dm_tran_locks where resource_type='OBJECT';"""
        cursor.execute(sql)

        for row in cursor.fetchall():
            result = True

        return result


token = 'kB5Gh2KDGLi8Te6nGgXYxXh5qoIlVLjepkQbi5sEVIS'
bpm = BPM()
while(True):
    count = 0
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Start Table Lock Check")
    result = True
    while(result):
        result = bpm.Check_bpm_tablelock()
        if result:
            count += 1
            time.sleep(2)

        if count > 5:
            # 修改為你要傳送的訊息內容
            message = "BPM發生鎖表"
            lineNotifyMessage(token, message)
            result = False


    print("Stop Table Lock Check")
    time.sleep(20)