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

        sql = """select A.processInstanceName,A.workItemName,A.createdTime,B.subject,A.completedTime,A.currentState,A.serialNumber from (
SELECT distinct a.processInstanceName,c.workItemName,c.createdTime,c.completedTime,c.currentState,a.serialNumber FROM ProcessInstance a,WorkStep b,WorkItem c WHERE a.contextOID = b.contextOID
        AND a.contextOID = c.contextOID
        AND c.completedTime IS NULL
        AND c.currentState = 2
		  AND b.currentState = 0 AND a.processInstanceName not in ('Fixed Asset Transfer(afat102)')
UNION 
SELECT distinct a.processInstanceName,c.workItemName,c.createdTime,c.completedTime,c.currentState,a.serialNumber FROM ProcessInstance a,WorkStep b,WorkItem c WHERE a.contextOID = b.contextOID
        AND a.contextOID = c.contextOID
        AND c.completedTime IS NULL
        AND workItemName = '動態加簽') A, ProcessInstance B where A.serialNumber = B.serialNumber"""
        cursor.execute(sql)

        for row in cursor.fetchall():
            # 修改為你要傳送的訊息內容
            message = """{doc_type} {activity} {approve_time}單據卡住\nSubject:{subject}"""
            message = message.format(doc_type=row[0], activity=row[1], approve_time=row[2], subject=row[3])
            print(message)
            lineNotifyMessage(self.token, message)


bpm = BPM()
bpm.Check_flow_status()