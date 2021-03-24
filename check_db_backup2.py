import socket
from smb.SMBConnection import SMBConnection
import datetime
from lineNotifyMessage import lineNotifyMessage

def Check_Mapping_Network_Driver_File():
    bpm_result = False
    tiptop_result = False
    msg = ""

    ip = '10.77.9.50'

    name = socket.gethostbyaddr(ip)
    #ipGet = socket.gethostbyname(name[0])
    #print(name, ipGet, sep='\n')

    remote_name = name[0]
    conn = SMBConnection('erp', 'admin#DSC2018', 'BPM_DB_BACKUP', remote_name)
    assert conn.connect(ip, timeout=3)

    for s in conn.listShares():
        print('------------------------------------')
        print('name', s.name)
        print('comments', s.comments)
        print('isSpecial', s.isSpecial)
        print('isTemporary', s.isTemporary)

        ''' 
        SharedDevice.DISK_TREE      0x00
        SharedDevice.PRINT_QUEUE    0x01
        SharedDevice.COMM_DEVICE    0x02
        SharedDevice.IPC            0x03
        '''
        print('type', s.type)
        print('')
        print('### FileList ###')

        try:
            yesterday = datetime.date.today() + datetime.timedelta(-1)

            if s.name == "BPM_BACKUP":
                for f in conn.listPath(s.name, '/Prod_db_backup'):
                    word = yesterday.strftime("%Y_%m_%d")
                    if f.filename.find(word) > 0:
                        print(f.filename)
                        bpm_result = True

                if not bpm_result:
                    msg += "BPM DB Backup少檔案" + word + "\n"

            if s.name == "TIPTOP_BACKUP":
                for f in conn.listPath(s.name, '/Prod_db_backup'):
                    word = yesterday.strftime("%Y%m%d")
                    if f.filename == word:
                        print(f.filename)
                        tiptop_result = True

                if not tiptop_result:
                    msg += "TIPTOP DB Backup少檔案" + word + "\n"

        except:
            print('### can not access the resource')
        print('------------------------------------')
        print('')

    conn.close()
    return bpm_result&tiptop_result, msg

result, message = Check_Mapping_Network_Driver_File()

if not result:
    token = 'kB5Gh2KDGLi8Te6nGgXYxXh5qoIlVLjepkQbi5sEVIS'
    lineNotifyMessage(token, message)