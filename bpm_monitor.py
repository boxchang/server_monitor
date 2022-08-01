import datetime
from bases.database import bpm_database
from bases.settings import PROD_FLAG, bpm_group_token
from lineNotifyMessage import lineNotifyMessage

class BPM(object):

    def Check_flow_status(self):
        tonow = datetime.datetime.now()
        db = bpm_database(PROD_FLAG)

        sql = """select A.processInstanceName,A.workItemName,A.createdTime,B.subject,A.completedTime,A.currentState,A.serialNumber from (
                    SELECT distinct a.processInstanceName,c.workItemName,c.createdTime,c.completedTime,c.currentState,a.serialNumber FROM ProcessInstance a,WorkStep b,WorkItem c WHERE a.contextOID = b.contextOID
                            AND a.contextOID = c.contextOID
                            AND c.completedTime IS NULL
                            AND c.currentState = 2
                              AND b.currentState = 0
                    UNION 
                    SELECT distinct a.processInstanceName,c.workItemName,c.createdTime,c.completedTime,c.currentState,a.serialNumber FROM ProcessInstance a,WorkStep b,WorkItem c WHERE a.contextOID = b.contextOID
                            AND a.contextOID = c.contextOID
                            AND c.completedTime IS NULL
                            AND workItemName = '動態加簽') A, ProcessInstance B where A.serialNumber = B.serialNumber"""
        cursor = db.execute_select_sql(sql)

        for row in cursor.fetchall():
            if row[0] == "Fixed Asset Transfer(afat102)" and (tonow.day < 15 or tonow.day > 25):
                continue

            # 修改為你要傳送的訊息內容
            message = """{doc_type} {activity} {approve_time}單據卡住\nSubject:{subject}"""
            message = message.format(doc_type=row[0], activity=row[1], approve_time=row[2], subject=row[3])
            print(message)
            lineNotifyMessage(bpm_group_token, message)


bpm = BPM()
bpm.Check_flow_status()