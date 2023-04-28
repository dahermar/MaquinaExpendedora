import mariadb
import telebot
from telebot import types
import time
import os

mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
)
TOKEN = '6291617574:AAFzG4EbtiHcv6R7r7_fZT8btqlnyvYSchk'
 
knownUsers = [] # todo: save these in a file,
userStep = {} # so they won't reset every time the bot restarts
 
commands = { # command description used in the "help" command
             'start': 'Get used to the bot',
             'ayuda': 'Da informacion sobre los comandos disponibles',
             'gasto': 'Mira cuanto ha gastado un cliente determinado'
}
 
hideBoard = types.ReplyKeyboardRemove() # if sent as reply_markup, will hide the keyboard
 
# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
 
 
 
bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener) # register listener
 

#creamos cursor
cursor= mydb.cursor()
cid=755565056
consulta=input("Que desea hacer: (0 para salir) ")
while(consulta != "0"):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    if consulta== "1":
        cursor.execute("SELECT * FROM clientes")
        bot.send_message(cid, "Tabla clientes")
        for x in cursor:
            bot.send_message(cid, "Resultado: "+str(x))
            print(x)
    elif consulta== "2":
        cursor.execute("SELECT * FROM productos")
        bot.send_message(cid, "Tabla productos")
        for x in cursor:
            bot.send_message(cid, "Resultado: "+str(x))
            print(x)
    elif consulta== "3":
        pr=input("que cliente : ")
        query=("SELECT * FROM clientes WHERE id = ?")
        val=(pr,)
        cursor.execute(query,val)
        resultado= cursor.fetchone()
        if resultado :
            print(resultado)
            bot.send_message(cid, "Cliente "+str(pr))
            bot.send_message(cid, "Resultado: "+str(resultado))
        else:
            print("no se encontro el cliente")
        
    elif consulta== "4":
            pr=input("Que producto : ")
            query=("SELECT * FROM productos WHERE id = ?")
            val=(pr,)
            cursor.execute(query,val)
            resultado= cursor.fetchone()
            if resultado :
                bot.send_message(cid, "Producto "+str(pr))
                bot.send_message(cid, "Resultado: "+str(resultado))
                print(resultado)
            else:
                print("No se encontro el producto")
     
    consulta=input("Que desea hacer: (0 para salir) ")    

cursor.close()
mydb.close()

