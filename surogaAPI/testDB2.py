import pyodbc
server = 'surogasql.database.windows.net'
database = 'surogasql'
username = 'carlos.leandro@suroga.com'
password = '{Surooactias90-}'
driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password +';Authentication=ActiveDirectoryPassword') as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()