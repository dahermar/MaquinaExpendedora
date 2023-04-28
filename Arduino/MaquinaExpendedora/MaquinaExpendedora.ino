#if 0
#include <SPI.h>
#include <PN532_SPI.h>
#include <PN532.h>
#include <NfcAdapter.h>


PN532_SPI pn532spi(SPI, 10);
NfcAdapter nfc = NfcAdapter(pn532spi);
#else

#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>

#include <LiquidCrystal_I2C.h>

PN532_I2C pn532_i2c(Wire);
NfcAdapter nfc = NfcAdapter(pn532_i2c);
#endif

#include <Keypad.h>
#include <Servo.h>
const byte COLS = 4; //four columns
const byte ROWS = 4; //four rows

Servo servo1, servo2, servo3;



//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte colPins[COLS] = {5, 4, 3, 2}; //connect to the row pinouts of the keypad
byte rowPins[ROWS] = {12, 8, 7, 6}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad myKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

int state = -1;
int errorCode = 0;
String serialIn;

LiquidCrystal_I2C lcd(0x27,16,2);

void setup(){
  Serial.begin(9600);
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  nfc.begin();

   // Inicializar el LCD
  lcd.init();
  
  //Encender la luz de fondo.
  lcd.backlight();
  
  // Escribimos el Mensaje en el LCD.
  lcd.print("Inicializando");
  lcd.setCursor(0, 1);
  lcd.print("sistema");
}
  
void loop(){
  switch(state){
    case -1:
      waitForACK();
      break;
    case 0:
      readNFC();
      break;
    case 1:
      selectProduct();
      break;
  }

  // Ubicamos el cursor en la primera posición(columna:0) de la segunda línea(fila:1)
  //lcd.setCursor(0, 1);
}

void waitForACK(){
  Serial.println("Conection_ACK");
  serialIn = Serial.readString();
  Serial.println("Leido:" + serialIn);
  if (serialIn == "ACK_Back")
    state++;
  
}

void readNFC(){
  String uidRead = "";
  if (nfc.tagPresent()){
      NfcTag tag = nfc.read();
      uidRead = tag.getUidString();
      Serial.println("NFC_UID:" + uidRead);
      serialIn = Serial.readString();
      if (serialIn != "No Valido"){
        Serial.println("Valido");
        lcd.clear();
        lcd.print("Hola " + serialIn);
        lcd.setCursor(0, 1);
        lcd.print("Elige producto");
        errorCode = 0;
        state++;
      }
      else{
        Serial.println("No Vale");
        errorCode = 1;
      }
      Serial.println("String de Rasp:" + serialIn);
  }
  else{
    if(errorCode == 0){
      lcd.clear();
      lcd.print("Acerque el");
      lcd.setCursor(0, 1);
      lcd.print("dispositivo NFC");
    }
    else if(errorCode == 1){
      lcd.clear();
      lcd.print("NFC no valido");
      lcd.setCursor(0, 1);
      lcd.print("Use NFC valido");
    }
    else if(errorCode == 2){
      lcd.clear();
      lcd.print("No hay unidades");
      lcd.setCursor(0, 1);
      lcd.print("Acerque el NFC");
    }
    else if(errorCode == 3){
      lcd.clear();
      lcd.print("Error en seleccion");
      lcd.setCursor(0, 1);
      lcd.print("Acerque el NFC");
    }
  }
  delay(500);
  
}

void selectProduct(){
  char keyPressed = myKeypad.getKey();
  
  if (keyPressed == '1'){
    Serial.println(keyPressed);
    Serial.println("PRODUCTO:1");
    serialIn = Serial.readString();
    Serial.println("String de Rasp en Prod:" + serialIn);
    if(serialIn == "Producto correcto"){
      servo1.write(180);
      delay(1000);
      servo1.write(0);
    }
    else if(serialIn == "Error cantidad"){
      errorCode = 2;
    }
    else{
      errorCode = 3;
    }
    state = 0;
  }
  else if (keyPressed == '2'){
    Serial.println(keyPressed);
    Serial.println("PRODUCTO:2");
    serialIn = Serial.readString();
    Serial.println("Aqui");
    Serial.println("String de Rasp en Prod:" + serialIn);
    if(serialIn == "Producto correcto"){
      servo2.write(180);
      delay(1000);
      servo2.write(0);
    }
    else if(serialIn == "Error cantidad"){
      errorCode = 2;
    }
    else{
      errorCode = 3;
    }
    state = 0;
  }
  else if (keyPressed == '3'){
    Serial.println(keyPressed);
    Serial.println("PRODUCTO:3");
    serialIn = Serial.readString();
    Serial.println("String de Rasp en Prod:" + serialIn);
    if(serialIn == "Producto correcto"){
      servo3.write(180);
      delay(1000);
      servo3.write(0);
    }
    else if(serialIn == "Error cantidad"){
      errorCode = 2;
    }
    else{
      errorCode = 3;
    }
    state = 0;
  }
}
