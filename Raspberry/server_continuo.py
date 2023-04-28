import mariadb
import serial
import re
import telebot
from telebot import types

bluetooth = serial.Serial("/dev/rfcomm6", 9600)

mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
)

TOKEN = '6291617574:AAFzG4EbtiHcv6R7r7_fZT8btqlnyvYSchk'

bot = telebot.TeleBot(TOKEN)

#creamos cursor
cursor= mydb.cursor()

estado = 0

print("Comienza la ejecucion")

while True:
    if estado== 0:
        serialIn = bluetooth.readline().decode("utf-8")
        if serialIn.startswith("NFC_UID:"):
            mydb = mariadb.connect(
            host='localhost',
            user='myuser',
            password='admin',
            database='mybase'
            )
            cursor= mydb.cursor()
            serialIn = re.sub('\s', '', re.sub("NFC_UID:", '', serialIn))
            print("NFC:", serialIn)
            query=("SELECT * FROM clientes WHERE nfc = ?")
            val=(serialIn,)
            cursor.execute(query,val)
            resultado= cursor.fetchone()
            if resultado :
                idCliente = resultado[0]
                cid=resultado[4]
                gasto=resultado[3]
                print("Cliente:", resultado[1])
                print("Id:", idCliente)
                print("gasto:", gasto)
                serialOut = '{0}'.format(resultado[1].split()[0])
                bluetooth.write(serialOut.encode("utf-8"))

                estado += 1
            else:
                print("NFC invalido")
                serialOut = '{0}'.format("No Valido")
                bluetooth.write(serialOut.encode("utf-8"))
        elif serialIn.startswith("Conection_ACK"):
            serialOut = '{0}'.format("ACK_Back")
            bluetooth.write(serialOut.encode("utf-8"))
        

    elif estado== 1:
        serialIn = bluetooth.readline().decode("utf-8")
        if serialIn.startswith("PRODUCTO:"):
            serialIn = re.sub('\s', '', re.sub("PRODUCTO:", '', serialIn))
            print("\nPRODUCTO:", serialIn)
            query=("SELECT * FROM productos WHERE id = ?")
            val=(serialIn,)
            cursor.execute(query,val)
            resultado= cursor.fetchone()
            if resultado:
                idProducto = resultado[0]
                precio = round(resultado[3], 2)
                producto = resultado[1]
                cantidad = resultado[2]
                print("Producto:", producto)
                print("Precio:", precio)
                print("Cantidad:", cantidad)
                if cantidad > 0:
                    estado += 1
                else:
                    print("Cantidad insuficiente")
                    estado = 0
                    serialOut = '{0}'.format("Error cantidad")
                    bluetooth.write(serialOut.encode("utf-8"))
            else:
                print("No se encontro el producto")
                estado = 0
                serialOut = '{0}'.format("Error producto")
                bluetooth.write(serialOut.encode("utf-8"))

    elif estado== 2:
        #Actualizar la base de datos aumentando el gasto acumulado del cliente
        print("Gasto Antes:", gasto)
        gasto += precio
        query = ("UPDATE clientes SET gasto = ? WHERE id = ?")
        val=(gasto,idCliente)
        cursor.execute(query,val)
        mydb.commit()
        print("Gasto Despues:", gasto)
        
        print("Cantidad Antes:", cantidad)
        cantidad -= 1
        query = ("UPDATE productos SET cantidad = ? WHERE id = ?")
        val=(cantidad,idProducto)
        cursor.execute(query,val)
        mydb.commit()
        print("Cantidad Despues:", cantidad)
        
        
        serialOut = '{0}'.format("Producto correcto")
        bluetooth.write(serialOut.encode("utf-8"))
        #Bot
        if cid != -1:
            try:
                bot.send_message(cid, "Transacción realizada\nProducto: " +producto + "\nPrecio: "+str(precio)+ "€")
            except:
                print("Error del bot")
        #Resetear estado
        estado = 0
        
        

cursor.close()
mydb.close()
