from bases.settings import *
from bases.database import tiptop_database

#Cursor to Dictionary
def Cursor2Dict(cursor):
    results = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


# 取得環境正式或測試
def getDBEnvFlag():
    return PROD_FLAG


# 取得營運中心DB Schema
def getDBSchema(com_name, prod=getDBEnvFlag()):
    COM_LIST = getTTComSchema(prod)
    return COM_LIST[com_name]


def getTTComSchema(prod_flag):
    results = {}
    ttdb = tiptop_database(prod_flag)
    schema = "dcc" if PROD_FLAG else "s20"
    sql = "select azp02,azp03 from {schema}.azp_file where ta_azp01 = 'Y'"
    sql = sql.format(schema=schema)
    cursor = ttdb.execute_select_sql(sql)
    for row in cursor.fetchall():
            com_name = str(row[0]).upper()
            results[com_name] = str(row[1])
    return results