import  pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:surogasql.database.windows.net,1433;DATABASE=surogasql;UID=carlos.leandro@suroga.com;PWD=Surooactias90-;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword')

#conn.commit()

cursor = conn.cursor()

cursor.execute('Select * FROM StudentReviews')

#conn.commit()

for  i  in  cursor:
    print(i)

cursor.close()

conn.close()