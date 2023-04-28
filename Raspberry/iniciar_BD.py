import mariadb

mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
)

#creamos cursor
cursor= mydb.cursor()
#TABLAs

#CLIENTE
cursor.execute("CREATE OR REPLACE TABLE clientes(id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), nfc VARCHAR(255), gasto FLOAT , telegramcid BIGINT)")
#PRODUCTOS
cursor.execute("CREATE OR REPLACE TABLE productos(id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), cantidad INT, precio FLOAT)")

#Incluir clientes
sql_incluir_cliente = "INSERT INTO clientes (id, name, nfc, gasto, telegramcid) VALUES (?, ?, ?, ?, ?)"
cliente1= ("1","Daniel Hernandez","93718A2D",0,755565056)
cursor.execute(sql_incluir_cliente,cliente1)

cliente2 = ("2","David Bugoi", "A3599591",0,6118226126)
cursor.execute(sql_incluir_cliente,cliente2)

cliente3 = ("3","Carlos Fernandez", "01020304",0,-1)
cursor.execute(sql_incluir_cliente,cliente3)

#Incluir productos
sql_incluir_producto = "INSERT INTO productos (id, name, cantidad, precio) VALUES (?, ?, ? ,?)"
producto1=("1","Smints",3,1.5)
cursor.execute(sql_incluir_producto,producto1)

producto2=("2","Halls",2,2.15)
cursor.execute(sql_incluir_producto,producto2)

producto3=("3","Trident",1,2.95)
cursor.execute(sql_incluir_producto,producto3)

#Hacemos los cambios en la base de datos
mydb.commit()

cursor.close()
mydb.close()

print("Base de datos actualizada")




