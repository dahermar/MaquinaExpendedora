#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import time
#time.sleep(60)

"""
This is a detailed example using almost every command of the API
"""
 
import telebot
from telebot import types
import time
import os
import mariadb

mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
)

def extract_arg(arg):
    return arg.split()[1:]

admin_cid = 755565056
#creamos cursor
cursor= mydb.cursor()

TOKEN = '6291617574:AAFzG4EbtiHcv6R7r7_fZT8btqlnyvYSchk'
 
knownUsers = [] # todo: save these in a file,
userStep = {} # so they won't reset every time the bot restarts
 
commands = { # command description used in the "help" command
             'start': 'Inicializa el bot',
             'ayuda': 'Da informacion sobre los comandos disponibles',
             'gasto': 'Consulta cuanto es tu gasto acumulado',
             'clientes': 'Consulta el gasto de un cliente (solo para admin)',
             'productos': 'Consulta la información de los productos (solo para admin)',
             'pago': 'Elimina el gasto acumulado de un cliente (solo para admin)',
             'reponer': 'Cambia la cantidad disponible de un producto (solo para admin)'
}
 
hideBoard = types.ReplyKeyboardRemove() # if sent as reply_markup, will hide the keyboard
 
# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
# had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print ("New user detected, who hasn't used \"/start\" yet")
        return 0
 
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
 
# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid) 
        userStep[cid] = 0
#        command_help(m) # show the new user the help page
 
# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Estos son los comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)
 

#Mira cuanto ha gastado un cliente determinado
@bot.message_handler(commands=['gasto'])
def command_long_text(m):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    cid = m.chat.id
    #bot.send_message(cid, "Vamos a comprobar cuanto ha gastado ")
    #bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    #time.sleep(2)
    #pr=m.text[len("/gasto "):]
    pr = cid
    query=("SELECT gasto FROM clientes WHERE telegramcid = ?")
    val=(pr,)
    cursor.execute(query,val)
    resultado= cursor.fetchone()
    if resultado :
        bot.send_message(cid, "Gasto acumulado: "+str(round(resultado[0], 2)) + " €")
    else:
        bot.send_message(cid, "No estas registrado en el sistema")
 
@bot.message_handler(commands=['clientes'])
def command_long_text(m):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    cid = m.chat.id
    if cid == admin_cid:
        cursor.execute("SELECT * FROM clientes")
        mensaje = "Información de clientes:\n"
        for x in cursor:
            mensaje += "\nCliente con id: "+ x[0] + "\n   Nombre: "+ x[1] + "\n   Gasto: "+ str(x[3]) + "€"
            print(x)
        bot.send_message(cid, mensaje)
    else:
        bot.send_message(cid, "Comando válido solo para administradores")

@bot.message_handler(commands=['productos'])
def command_long_text(m):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    cid = m.chat.id
    if cid == admin_cid:
        
        cursor.execute("SELECT * FROM productos")
        mensaje = "Información de productos:\n"
        for x in cursor:
            mensaje += "\nProducto con id: "+ x[0] + "\n   Nombre: "+ x[1] + "\n   Cantidad: "+ str(x[2]) + "\n   Precio: "+ str(x[3]) + "€"
            print(x)
        bot.send_message(cid, mensaje)
        
        print("M: " + str(extract_arg(m.text)))
    else:
        bot.send_message(cid, "Comando válido solo para administradores")
        
@bot.message_handler(commands=['pago'])
def command_long_text(m):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    cid = m.chat.id
    if cid == admin_cid:
        args = extract_arg(m.text)
        if len(args) > 0:
            query=("SELECT * FROM clientes WHERE id = ?")
            val=(args[0],)
            cursor.execute(query,val)
            resultado= cursor.fetchone()
            if resultado: 
                query = ("UPDATE clientes SET gasto = ? WHERE id = ?")
                val=(0,args[0])
                cursor.execute(query,val)
                mydb.commit()
                bot.send_message(cid, "Gasto actualizado")
            else:
                bot.send_message(cid, "Identificador no válido")
            
        else:
            bot.send_message(cid, "Faltan argumentos: /pago idCliente")
    else:
        bot.send_message(cid, "Comando válido solo para administradores")
        
@bot.message_handler(commands=['reponer'])
def command_long_text(m):
    mydb = mariadb.connect(
    host='localhost',
    user='myuser',
    password='admin',
    database='mybase'
    )
    cursor= mydb.cursor()
    cid = m.chat.id
    if cid == admin_cid:
        args = extract_arg(m.text)
        if len(args) > 1:
            query=("SELECT * FROM productos WHERE id = ?")
            val=(args[0],)
            cursor.execute(query,val)
            resultado= cursor.fetchone()
            if resultado: 
                query = ("UPDATE productos SET cantidad = ? WHERE id = ?")
                val=(args[1],args[0])
                cursor.execute(query,val)
                mydb.commit()
                bot.send_message(cid, "Producto actualizado")
            else:
                bot.send_message(cid, "Identificador no válido")
            
        else:
            bot.send_message(cid, "Faltan argumentos: /reponer idProducto cantidad")
    else:
        bot.send_message(cid, "Comando válido solo para administradores")
 
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")
 
bot.polling()
