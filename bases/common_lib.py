#Cursor to Dictionary
def Cursor2Dict(cursor):
    results = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results
