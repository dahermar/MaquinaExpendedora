# Máquina Expendedora
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

## Configuración Bluetooth

La configuración de la conexión ha sido la parte más complicada del proyecto, por lo que pondremos un tutorial de como configurarla

### Bluetooth en Arduino

Para realizar la conexión bluetooth seguimos los siguientes pasos. La parte más sencilla del proceso fue la del Arduino. Para ello utilizamos el módulo bluetooth HC-06. Este actuará de esclavo en la conexión, siendo la Raspberry Pi el maestro. La configuración es sencilla. El módulo HC-05 tiene 4 pines. Uno de ellos es para la alimentación de 5V, el cual ha de conectarse al pin de salida de 5v del arduino o, en su defecto a una fuente externa de 5V. Otro es para conectar a tierra. Los otros dos pines son de Tx/Rx. El pin Tx ha de conectarse con el Rx del Arduino y el Rx con el Tx. Es importante no confundirse, ya que si no prestamos atención es sencillo confundirse y asumir que hay que conectar el Tx con el Tx y el Rx con el Rx, pero de esta forma la comunicación no funcionaría. 

Cabe remarcar que el código y conexiones que tenemos en el proyecto funcionaría igual utilizando un módulo HC-05 en vez del HC-06. La única diferencia es que el HC-05 puede utilizarse como esclavo y como maestro, mientras que el HC-06 solo puede ser usado como esclavo. Debido a ello, además de los mismos 4 pines que tiene el HC-06, el HC-05 dispone de dos extras: el Key y el State, que se utilizan cuando actúa como maestro. Pero como en nuestro caso lo vamos a utilizar de esclavo, si tenemos el HC-05, dejaremos estos pines sin conectar y realizaremos la misma conexión explicada previamente para el HC-06.

Una vez en este punto, el Arduino no “sabe” que está conectado por bluetooth, ya que simplemente hemos conectado sus pines Tx/Rx a un dispositivo, el cual no le especificamos cual es. Entonces, el Arduino solo tendrá que escribir en Serial cuando quiera enviar un dato a la Raspberry y leer de Serial cuando quiera recibirlo. Esto es debido a que, al tener sus pines Tx/Rx conectados con el módulo HC-06, simplemente está redirigiendo su comunicación Serial a este módulo. Es el HC-06 el encargado de enviar lo que reciba desde el Tx del Arduino en Serial al dispositivo con el que esté conectado por Bluetooth y enviar al Rx del Arduino lo que reciba del dispositivo.

### Bluetooth en Raspberry Pi

La parte de la conexión Bluetooth fue la que nos trajo más problemas. Consultamos multitud de tutoriales que utilizaban bibliotecas y aplicaciones que o bien ya no existían o habían cambiado tanto que esos métodos ya no funcionaban. Finalmente encontramos el siguiente vídeo (https://www.youtube.com/watch?v=hBqmAM1tZR8&t=725s),  que nos sirvió de base para configurar correctamente la conexión. Aunque hubo una sección que no nos funcionó, la de emparejar el dispositivo, conseguimos hacerlo utilizando la herramienta Blueman, como explicaremos a continuación.

En primer lugar lo que haremos será consultar la MAC del HC-06. Para ello, en primer lugar deberemos conectarlo al arduino y darle corriente. La luz roja deberá parpadear. A continuación utilizaremos la herramienta bluetoothctl incluida en Raspberry Pi OS. En una consola escribiremos los siguientes comandos:

- sudo bluetoothctl
- agent on
- scan on

A continuación nos aparecerá una lista de todos los dispositivos bluetooth que detecta, indicando su nombre y su MAC. Buscaremos el HC-06 (o HC-05) y apuntaremos su MAC, ya que la necesitaremos más adelante. Ahora tenemos que emparejar, que no conectar, el HC-06 con la Raspberry Pi. Esta es la sección del vídeo que no nos funcionaba. En el tutorial él utiliza la aplicación de bluetooth que aparece arriba a la derecha y escanea los dispositivos. En nuestro caso no nos aparecía el módulo bluetooth, puede que por utilizar el HC-06, ya que en el vídeo utiliza el HC-05. Para poder emparejarlo, utilizamos la herramienta Blueman. Esta herramienta es una aplicación con interfaz gráfica para la gestión de conexiones bluetooth. Para instalarla hay que ejecutar los siguientes comandos:

- sudo apt-get install pi-bluetooth
- sudo apt-get install bluetooth bluez blueman

Tras reiniciar el sistema ya tendremos acceso a Blueman. Podremos ejecutar la aplicación pulsando en el nuevo símbolo de bluetooth que aparecerá arriba a la derecha, no pulsar sobre el símbolo de bluetooth que había antes de instalar Blueman. Una vez abierto ahí sí aparecerá el HC-06 tras escanear los dispositivos. Tendremos que hacer click derecho sobre él y pulsar en emparejar (pair). No pulsar sobre conectar, ya que no es la función que queremos y dará un error. Ahora ya tenemos el módulo emparejado. Todos estos pasos hay que realizarlos una sola vez, aunque reiniciemos el sistema. El módulo permanecerá siempre emparejado.

Ahora ya tenemos el módulo conectado, pero tenemos que descubrir cómo pasar datos a través de él. Para ello utilizaremos el protocolo rfcomm. Rfcomm es un protocolo construido sobre L2CAP emula conexión en serie. Puede emular hasta sesenta conexiones de manera simultánea. Para utilizarlo tenemos que asociar una de estas conexiones a la MAC del HC-06, la cual hemos apuntado previamente. Para ello ejecutaremos el siguiente comando en una consola:

- sudo rfcomm bind n MAC

Ejecutaremos el comando sustituyendo “n” por un entero entre 0 y 59 y “MAC” por la MAC del HC-06. De esta forma habremos mapeado la salida “n” del protocolo rfcomm a la MAC del módulo bluetooth. De esta manera, cuando escribamos en Serial sobre la salida 6 del protocolo rfcomm, los datos llegarán al módulo bluetooth y se transmitirán al Arduino. Para enviar información a través del módulo bluetooth usando el protocolo rfcomm en python hay que escribir la siguiente instrucción:

- bluetooth = serial.Serial(“/dev/rfcommN”, 9600)

Cabe destacar que hay que sustituir la N final de “/dev/rfcommN” por el número de salida que hemos asignado al HC-06. Además en este ejemplo establecemos los Baudios a 9600 y tienen que coincidir con los que hemos puesto en la conexión serial del Arduino.


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
