#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Keypad.h>

// Pin Configurations
#define SS_PIN 5
#define RST_PIN 2
#define LED_PIN 13
#define BUZZER_PIN 15

// WiFi Credentials
const char* ssid = "Robotica";
const char* password = "Gira2024";
const char* serverName = "http://cerradura-production.up.railway.app/";

// RFID and LCD Initialization
MFRC522 rfid(SS_PIN, RST_PIN);  
LiquidCrystal_I2C lcd(0x27, 20, 4);  

// Keypad Configuration
const uint8_t ROWS = 4;
const uint8_t COLS = 4;

char keys[ROWS][COLS] = {
  { '1', '4', '7', '*' },
  { '2', '5', '8', '0' },
  { '3', '6', '9', '#' },
  { 'A', 'B', 'C', 'D' }
};

uint8_t colPins[COLS] = { 27, 14, 12, 13 };
uint8_t rowPins[ROWS] = { 32, 33, 25, 26 };

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Global Variables
String inputClave = "";
bool modoRFID = false;

// Helper Functions
String extraerNombre(String response) {
  int nombreStart = response.indexOf("\"nombre_completo\":\"") + 18;
  int nombreEnd = response.indexOf("\"", nombreStart);
  return response.substring(nombreStart, nombreEnd);
}

bool verificarAcceso(String valor) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String fullUrl = "https://cerradura-production.up.railway.app/tarjeta_adquisicion_valores/" + valor + "/";
    http.begin(fullUrl);
    
    int httpResponseCode = http.GET();
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
      
      if (response.indexOf("Valor valido") > 0) {
        String nombre = extraerNombre(response);
        
        lcd.clear();
        lcd.print("Bienvenido");
        lcd.setCursor(0, 1);
        lcd.print(nombre);
        
        digitalWrite(LED_PIN, HIGH);
        beepAccesoCorrecto();
        
        delay(2000);
        digitalWrite(LED_PIN, LOW);
        
        http.end();
        return true;
      }
    }
    
    http.end();
  }
  
  lcd.clear();
  lcd.print("Acceso Denegado");
  lcd.setCursor(0, 1);
  lcd.println(valor);
  Serial.println(valor);
  //beepAccesoDenegado();
  delay(5000);
  return false;
}

void beepAccesoCorrecto() {
    digitalWrite(BUZZER_PIN, LOW);
    Serial.println("encendido");
    delay(5000);
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("apagado");
}

/*void beepAccesoDenegado() {
    for (int i = 0; i < 3; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(5000);
        digitalWrite(BUZZER_PIN, LOW);
        delay(5000);
    }
}*/

/*void beepTecla() {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
}*/

void mostrarMenuPrincipal() {
    lcd.clear();
    lcd.print("Menu Principal");
    lcd.setCursor(4, 2);
    lcd.print("A:RFID B:Clave");
}

String obtenerUID() {
    String uid = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        uid += String(rfid.uid.uidByte[i], HEX);
    }
    return uid;
}

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  SPI.begin();        
  rfid.PCD_Init();    

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, HIGH);

  Wire.begin();
  lcd.init();
  lcd.backlight();
  
  mostrarMenuPrincipal();
}

void loop() {
  static unsigned long lastCredentialCheck = 0;
  
  // Periodic credential check (optional)
  if (millis() - lastCredentialCheck > 300000) {
    lastCredentialCheck = millis();
  }

  // RFID Mode
  if (modoRFID) {
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
      String uid = obtenerUID();
      verificarAcceso(uid);
      
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();
      modoRFID = false;
      mostrarMenuPrincipal();
    }
  }
  
  // Keypad Input
  char key = keypad.getKey();
  
  if (key) {
    //beepTecla();
    
    if (key == 'A') {  // Enter RFID Mode
      modoRFID = true;
      lcd.clear();
      lcd.print("Modo RFID");
      lcd.setCursor(0, 1);
      lcd.print("Acerque Tarjeta");
    }
    else if (key == 'B') {  // Enter Password Mode
      inputClave = "";
      lcd.clear();
      lcd.print("Ingrese Clave:");
      
      while (!modoRFID) {
        char keyPressed = keypad.getKey();
        
        if (keyPressed) {
          if (keyPressed == 'D') {  // Submit password
            verificarAcceso(inputClave);
            mostrarMenuPrincipal();
            break;
          }
          else if (keyPressed >= '0' && keyPressed <= '9') {
            inputClave += keyPressed;
            lcd.setCursor(0, 1);
            for(int i = 0; i < inputClave.length(); i++) {
              lcd.print("*");
            }
          }
        }
      }
    }
  }
}