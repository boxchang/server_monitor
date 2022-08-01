# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
sys.path.append("..")
from bases.common_lib import *
from bases.database import tiptop_database, bpm_database
from bases.settings import PROD_FLAG
from lineNotifyMessage import lineNotifyMessage


class check_tt_org(object):
    # 取得BPM所有部門，排除掉非組織部門或是虛擬部門
    def getBPM_OrgData(self):
        db = bpm_database(PROD_FLAG)
        sql = """select id,organizationUnitName from OrganizationUnit where id not like '001%' and validType = 1
        and id not in ('00010200', '00110900', '02000000', '06000000', '07000000', '99000000', 'ERP', 'ADMINPRJ')"""
        cursor = db.execute_select_sql(sql)
        results = Cursor2Dict(cursor)
        print(results)
        return results

    # 取得TT所有部門
    def getTT_OrgData(self):
        tt_dept = []
        db = tiptop_database(PROD_FLAG)
        COM_LIST = getTTComSchema(PROD_FLAG)
        for schema in COM_LIST.values():
            sql = """select gem01,gem02 from {schema}.gem_file"""
            sql = sql.format(schema=schema)
            cursor = db.execute_select_sql(sql)
            results = Cursor2Dict(cursor)
            print(results)
            tt_dept += results
        return tt_dept

    # 主要執行邏輯
    def execute(self):
        #取得BPM部門，以Dict存放
        bpm_dept_dict = self.getBPM_OrgData()

        #取得TT部門，並將Key值以List存放
        tt_dept_dict = self.getTT_OrgData()
        tt_dept_list = []

        for dept in tt_dept_dict:
            tt_dept_list.append(dept["GEM01"])
        print(tt_dept_list)

        for bpm_dept in bpm_dept_dict:
            if bpm_dept['id'] in tt_dept_list:
                continue
            else:
                # 修改為你要傳送的訊息內容
                message = """BPM存在部門 {id} {organizationUnitName} 但在TIPTOP的aooi030找不到部門資料"""
                message = message.format(id=bpm_dept['id'], organizationUnitName=bpm_dept['organizationUnitName'])
                print(message)
                lineNotifyMessage(bpm_group_token, message)


chk =check_tt_org()
chk.execute()