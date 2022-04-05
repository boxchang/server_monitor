from bases.common_lib import Cursor2Dict
from bases.database import bpm_database, tiptop_database
from bases.settings import PROD_FLAG, eteam_group_token, bpm_group_token
from lineNotifyMessage import lineNotifyMessage

settings = [
    {"PROG_NAME": "apmt420", "DOCNO_COLUMN": "pmk01",
     "HOUR_RANGE": "24", "TT_TABLE": "pmk_file", "TT_STATUS_COLUMN": "pmk25"},  # apmt420
    {"PROG_NAME": "apmt540", "DOCNO_COLUMN": "pmm01",
     "HOUR_RANGE": "24", "TT_TABLE": "pmm_file", "TT_STATUS_COLUMN": "pmm25"},  # apmt540
    {"PROG_NAME": "apmt910", "DOCNO_COLUMN": "pna01",
     "HOUR_RANGE": "24", "TT_TABLE": "pna_file", "TT_STATUS_COLUMN": "pna13"},  # apmt910
    {"PROG_NAME": "aapt110", "DOCNO_COLUMN": "apa01",
     "HOUR_RANGE": "24", "TT_TABLE": "apa_file", "TT_STATUS_COLUMN": "apa63"},  # aapt110
    {"PROG_NAME": "aapt120", "DOCNO_COLUMN": "apa01",
     "HOUR_RANGE": "24", "TT_TABLE": "apa_file", "TT_STATUS_COLUMN": "apa63"},  # aapt120
    {"PROG_NAME": "aapt150", "DOCNO_COLUMN": "apa01",
     "HOUR_RANGE": "24", "TT_TABLE": "apa_file", "TT_STATUS_COLUMN": "apa63"},  # aapt150
    {"PROG_NAME": "aapt330", "DOCNO_COLUMN": "apf01",
     "HOUR_RANGE": "24", "TT_TABLE": "apf_file", "TT_STATUS_COLUMN": "apf42"},  # aapt330
    {"PROG_NAME": "aglt110", "DOCNO_COLUMN": "aba01",
     "HOUR_RANGE": "24", "TT_TABLE": "aba_file", "TT_STATUS_COLUMN": "aba20"},  # aglt110
]


class Param(object):
    PROG_NAME = ""  # 表單Table - 用來找單別
    DOCNO_COLUMN = ""  # 單別欄位名稱
    HOUR_RANGE = ""  # 查找時間 - 例如1天內的單據
    TT_TABLE = ""  # TT Table名稱
    TT_STATUS_COLUMN = ""  # 參數六、狀態欄位名稱

    def __init__(self, prog_name, docno_column, hour_range, tt_table, tt_status_column):
        self.PROG_NAME = prog_name
        self.DOCNO_COLUMN = docno_column
        self.HOUR_RANGE = hour_range
        self.TT_TABLE = tt_table
        self.TT_STATUS_COLUMN = tt_status_column

    def execute(self):
        doc_list = self.getBPM_Data()
        self.chkTT_Data(doc_list)

    def chkTT_Data(self, doc_list):
        db = tiptop_database(PROD_FLAG)
        COM_LIST = self.getTTComSchema()
        for doc in doc_list:
            schema = COM_LIST[doc[self.DOCNO_COLUMN][6:9]]
            sql = """select * from {SCHEMA}.{TT_TABLE} where {DOCNO_COLUMN}='{DOCNO}' and {TT_STATUS_COLUMN} ='S'"""
            sql = sql.format(SCHEMA=schema, TT_TABLE=setting['TT_TABLE'],
                             DOCNO_COLUMN=setting['DOCNO_COLUMN'],
                             DOCNO=doc[setting["DOCNO_COLUMN"]],
                             TT_STATUS_COLUMN=setting["TT_STATUS_COLUMN"])
            print(sql)
            cursor = db.execute_select_sql(sql)
            results = Cursor2Dict(cursor)
            if len(results) > 0:
                msg = '單號{DOCNO}，BPM已簽核完成，TT狀態尚未確認'.format(DOCNO=doc[setting["DOCNO_COLUMN"]])
                print(msg)
                lineNotifyMessage(eteam_group_token, msg)

    def getBPM_Data(self):
        db = bpm_database(PROD_FLAG)
        sql = """select {DOCNO_COLUMN} from ProcessInstance p, {PROG_NAME} b, WorkItem w
                    where p.serialNumber = b.processSerialNumber and p.contextOID = w.contextOID
                    and p.currentState = 3
                    group by {DOCNO_COLUMN} having max(completedTime) > DATEADD(hh, -{HOUR_RANGE},GETDATE( ))"""
        sql = sql.format(DOCNO_COLUMN=self.DOCNO_COLUMN, PROG_NAME=self.PROG_NAME, HOUR_RANGE=self.HOUR_RANGE)
        cursor = db.execute_select_sql(sql)
        results = Cursor2Dict(cursor)
        return results

    def getTTComSchema(self):
        results = {}
        ttdb = tiptop_database(PROD_FLAG)
        schema = "dcc" if PROD_FLAG else "s20"
        sql = "select azp01,azp03 from {schema}.azp_file where ta_azp01 = 'Y'"
        sql = sql.format(schema=schema)
        cursor = ttdb.execute_select_sql(sql)
        for row in cursor.fetchall():
            com_name = str(row[0]).upper()
            results[com_name] = str(row[1])
        return results

for setting in settings:
    param = Param(setting["PROG_NAME"], setting["DOCNO_COLUMN"], setting["HOUR_RANGE"], setting["TT_TABLE"], setting["TT_STATUS_COLUMN"])
    param.execute()