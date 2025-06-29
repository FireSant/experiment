import sqlite3
import pandas as pd
square=lambda n: n*n
#primero conectar base de datos //first, connect de database trought the sqlite lib
with sqlite3.connect("northwind.db") as conn:
    #se crea la funcion square. solo pq se la quiere usar para el data frame //it's created the square function 
    conn.create_function("square",1,square)
    #se define el cursor que es el que va a ejecutar cualquier consulta // cursor gets defined. throught it, you can execute any query to the db
    cursor=conn.cursor()
    #se ejecuta la consulta deseada. en este caso devolver todas las columnas, ademas sacar el cuadrado del precio
    #desired query gets executed. In this case, get all columns, also get the squared price 
    cursor.execute('SELECT *, square(price) from Products')
    results=cursor.fetchall()
    #convertir en dataframe por medio de pandas
    #convert the obtained data on datframe through the pandas Dataframe func
    results_df=pd.DataFrame(results)
    #muestra results_df //shows dataframe results
    print(results_df)


#quisiera saber como hacer que se muestren encabezados de las columnas
#ademas, saber como parte de que proyecto puedo usar las consultas a sql
#en un futuro como implementar sql, python, nube. Un proyecto destinado a Prev. Rie. Lbrl.



