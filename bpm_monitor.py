import datetime
import os
import pyodbc

from lineNotifyMessage import lineNotifyMessage

class BPM(object):
    token = 'kB5Gh2KDGLi8Te6nGgXYxXh5qoIlVLjepkQbi5sEVIS'

    def Check_flow_status(self):

        server = 'tcp:10.77.9.4'
        database = 'EFGP'
        username = 'sa'
        password = 'Sql#dsc2019'
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()

        sql = """SELECT a.processInstanceName,c.workItemName,c.createdTime FROM ProcessInstance a,WorkStep b,WorkItem c WHERE a.contextOID = b.contextOID
        AND a.contextOID = c.contextOID
        AND c.completedTime IS NULL
        AND c.currentState=2 AND b.currentState = 0"""
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(row[0] + " " + row[1] + " " + str(row[2]) + "單據卡住")

            # 修改為你要傳送的訊息內容
            message = row[0] + " " + row[1] + " " + str(row[2]) + "單據卡住"
            lineNotifyMessage(self.token, message)


bpm = BPM()
bpm.Check_flow_status()