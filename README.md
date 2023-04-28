# MaquinaExpendedora
Proyecto que combina el uso de una Raspberry Pi 3 y un Arduino Uno para construir una máquina expendedora que funciona mediante identificación NFC, sin necesidad de realizar un pago en el momento

## Integrantes

- Daniel Hernández Martínez
- David Bugoi

## Preliminares

La gran mayoría de las máquinas expendedoras del mercado funcionan de la siguiente manera: introduces una cantidad de dinero o pagas con tarjeta bancaria y te proporciona un producto que seleccionas a través de un teclado. Sin embargo, nuestro proyecto pretende realizar una máquina expendedora con una serie de cambios respecto a lo estándar. 


Este proyecto está enfocado para sitios como empresas, ya que el cliente no introduce dinero, si no que escanea una dispositivo NFC (tarjeta, móvil, etc) asociado a él. Cuando el cliente selecciona el producto, el sistema sumará el precio de este al gasto total acumulado del usuario, el cual se almacenará en una base de datos. Entonces la máquina le proporciona el producto sin la necesidad de haber efectuado un pago en ese momento. Finalmente será la empresa la que decida cómo cobrar el gasto acumulado, generalmente con un cargo igual a dicha cantidad en la cuenta del cliente a final de mes. 


Otra funcionalidad del sistema será la integración de un bot de telegram. Con él los usuarios podrán consultar en todo momento su gasto acumulado y recibir información sobre las transacciones en tiempo real.


Uno de los principales problemas de las máquinas expendedoras actuales es que requieren de una conexión a Internet para disponer de todas sus funcionalidades, principalmente del pago con tarjeta. Esto provoca que en lugares en los que la conexión a Internet no es muy buena, impida a los clientes obtener productos mediante el pago con tarjeta. Esto mismo sucede en nuestra facultad y es la principal motivación que hemos tenido para realizar este proyecto, el cual solventará dicho problema.


## Cuerpo

Nuestro sistema está compuesto por una Raspberry Pi 3 B+, un Arduino Uno y un bot de Telegram. La Raspberry tiene la función de almacenar la base de datos de los clientes y productos además de implementar el bot de Telegram. El Arduino tiene implementada una máquina de estados y realiza la interacción con el usuario y los productos mediante sus componentes electrónicos.  El bot ofrece al usuario la capacidad de consultar su saldo en cualquier momento y obtener información de las transacciones a tiempo real.


En esta máquina expendedora, la conexión a Internet no es obligatoria, ya que la base de datos está implementada en el propio sistema, en la Raspberry incluida dentro de la máquina. Debido a ello, en caso de una desconexión a Internet, solo dejaría de estar operativa la funcionalidad del bot de Telegram, pero la máquina seguiría con su comportamiento estándar, pudiendo los clientes obtener productos y acumular el gasto.


La comunicación entre la Raspberry y el Arduino se lleva a cabo por Bluetooth. Ambas placas escriben en Serial para comunicarse entre ellas. El Arduino está conectado por Tx/Rx a un módulo Bluetooth HC-06 conectado por Bluetooth a la Raspberry. La Raspberry utiliza el protocolo rfcomm para enviar los mensajes al módulo HC-06. Además utilizamos el protocolo I2C para la lectura NFC.


El usuario comienza su interacción con el sistema escaneando el dispositivo NFC asociado a él. Si está registrado en el sistema, indicará por teclado que producto desea. Si este está disponible, la máquina expenderá el producto y se sumará el precio al gasto total del usuario.


Los componentes utilizados son los siguientes:

- Módulo NFC PN532

- Módulo Bluetooth HC-06

- Servomotores 9g 180º

- Display LCD 1602

- Teclado Matricial



## Conclusiones relevantes

Consideramos que este proyecto sirve como prototipo de lo que sería una máquina expendedora comercial que solvente las necesidades expuestas en los preliminares. El proyecto es escalable ya que ofrece la posibilidad de realizar una serie de añadidos al diseño. El principal sería el utilizar una única Raspberry para varias máquinas y Arduinos. Esto nos permitiría controlar más de una máquina con la misma Raspberry y tener una base de datos unificada. Otra ampliación interesante sería la sustitución del bot de Telegram por una aplicación móvil propia.

## Instrucciones de instalación

En este apéndice están las instrucciones para instalar las librerías y aplicaciones y/o configurarlas para que nuestro sistema funcione. 

### Raspberry

- Instalar Raspberry Pi OS: https://www.raspberrypi.com/software/
Una vez instalado el sistema operativo dentro tendremos que instalar lo siguiente:
- Instalar MariaDB-server
  - sudo apt-get install mariadb-server
- Configurar mariadb
  - sudo mariadb
  - Dentro de mariadb (después de escribir el comando anterior) los siguientes comandos:
    - create database mybase;
    - create user ‘myuser’@’localhost’ identified by ‘admin’;
    - grant all privileges on mybase.* to ‘myuser’@’localhost’;
    - flush privileges;

-Instalar librerias de python
  - pip install mariadb
  - pip install pyTelegramBotAPI

- Finalmente para arrancar el sistema
  - Correr el archivo server.py
  - Correr el archivo telegrambot.py
  - Correr el archivo server_continuo.py 

Felicidades, ¡ya tienes el servidor corriendo!

Para configurar la conexión bluetooth consultar la sección Bluetooth de este documento

### Arduino
- Instalar IDE Arduino
  - https://www.arduino.cc/en/software
- Instalar las siguientes bibliotecas desde el IDE de Arduino:
  - Adafruit PN532 y sus dependencias
  - Keypad by Mark Stanley, Alexander Brevig
  - LiquidCrystal I2C by Frank de Brabander
    - Nosotros usamos la versión v1.1.1. Existe la v1.1.2, debería funcionar igual pero no lo hemos comprobado. En caso de que no funcione, instala la v1.1.1
- Instalar desde link externo:
  - PN532_HSU
    - Descargar de este github: https://github.com/elechouse/PN532
    - Extraer el zip y copiar cada una de las carpetas que aparecen dentro de la carpeta PN532-PN532_HSU en .\Documents\Arduino\libraries



## Fuentes consultadas

Librería Telegram Bot Python:

https://pypi.org/project/pyTelegramBotAPI/

https://www.flopy.es/crea-un-bot-de-telegram-para-tu-raspberry-ordenale-cosas-y-habla-con-ella-a-distancia/

Librería MariaDB python: 

https://mariadb-corporation.github.io/mariadb-connector-python/

https://www.tutorialspoint.com/python_data_access/

Conexión Bluetooth Raspberry Pi y Arduino:

https://www.youtube.com/watch?v=hBqmAM1tZR8&t=725s

Ebooks Gratis componentes Arduino (Teclado y Servomotores):

https://www.az-delivery.de/collections/kostenlose-e-books

Servomotores en Arduino:

https://programarfacil.com/blog/arduino-blog/servomotor-con-arduino/

Configurar NFC en Arduino:

https://how2electronics.com/interfacing-pn532-nfc-rfid-module-with-arduino/

https://www.youtube.com/watch?v=PXE8nsXh4eg
