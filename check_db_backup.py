import datetime
import os
import time
import win32net

from lineNotifyMessage import lineNotifyMessage


def Check_Mapping_Network_Driver_File(word):
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
        else:
            return False

    try:
        win32net.NetUseDel(None, data['local'], 0)
    except:
        print("解開Mapping 出錯")


yesterday = datetime.date.today() + datetime.timedelta(-1)
yesterday = yesterday.strftime("%Y_%m_%d")

if not Check_Mapping_Network_Driver_File(yesterday):
    token = 'kB5Gh2KDGLi8Te6nGgXYxXh5qoIlVLjepkQbi5sEVIS'
    message = "BPM DB Backup少檔案"+yesterday
    lineNotifyMessage(token, message)
