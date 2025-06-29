import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import io 

conn=sqlite3.connect("northwind.db")
#do the query that calculate the most profitable employee
query='''SELECT *, productname, SUM(price*quantity) as Revenue
from OrderDetails od
join products p ON p.productid=od.productid
group by od.productid
order by revenue desc
limit 5
'''
query2='''Select FirstName || " " || LastName as employee, Count(*) as total
    From Orders o
    join employees e
    on e.employeeID=o.employeeId
    Group by o.employeeid
    order by total desc
    '''
topempl=pd.read_sql_query(query2, conn)
topempl.plot(x='employee', y="total", kind="bar", figsize=(5,2), legend=True)

plt.title('10 most profitable employees')
plt.xlabel('Employees')
plt.ylabel('revenue')
plt.xticks(rotation=90)
#plt.show()
top_prodcuts=pd.read_sql_query(query, conn)
print(top_prodcuts)