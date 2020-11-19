import datetime
import os
import pyodbc

from lineNotifyMessage import lineNotifyMessage

class BPM(object):
    token = 'kB5Gh2KDGLi8Te6nGgXYxXh5qoIlVLjepkQbi5sEVIS'

    def Check_Mapping_Network_Driver_File(self, word):
        global NetDriver
        NetDriver = "j:"
        data = {}
        data['remote'] = r'\\10.77.9.50\bpm_backup\Prod_db_backup'  # 對應到的路徑
        data['local'] = 'j:'
        data['passwd'] = 'admin#DSC2018'
        data['user'] = 'erp'
        data['asg_type'] = 0
        try:
            win32net.NetUseAdd(None, 1, data)
        except:
            print("win32net.NetUseAdd(None, 1, data) Fail")

        Lst_Folder = os.listdir(NetDriver)
        for x in Lst_Folder:
            #Method_of_Do_Something(NetDriver + x)  # 這裡就拿到對應的路徑而且也把檔案都列出來的說
            if x.find(word) > 0:
                return True

        return False

        try:
            win32net.NetUseDel(None, data['local'], 0)
        except:
            print("解開Mapping 出錯")


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

    def Check_DB_File(self):
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        yesterday = yesterday.strftime("%Y_%m_%d")

        if not bpm.Check_Mapping_Network_Driver_File(yesterday):
            message = "BPM DB Backup少檔案" + yesterday
            lineNotifyMessage(self.token, message)


bpm = BPM()
#bpm.Check_DB_File()
bpm.Check_flow_status()