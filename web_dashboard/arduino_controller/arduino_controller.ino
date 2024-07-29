#include <Encoder.h>
// Include the Wire library for I2C
#include <Wire.h>

// Définir les broches de l'encodeur
const int pinA = 2;
const int pinB = 3;

// Definir les pins des moteurs
const int M1_1 = 9;
const int M1_2 = 10;
const int M2_1 = 5;
const int M2_2 = 6;

const int ledPin = 13; 

// Créer une instance de l'encodeur
//Encoder myEncoder(pinA, pinB);

long oldPosition  = -999;

void turn_on_motors(){
  analogWrite(M1_1,100);
  analogWrite(M1_2,0);
  analogWrite(M2_1,100);
  analogWrite(M2_2,0);
}

void turn_off_motors(){
  analogWrite(M1_1,0);
  analogWrite(M1_2,0);
  analogWrite(M2_1,0);
  analogWrite(M2_2,0);
}


void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  
  digitalWrite(ledPin, LOW);
  
  Serial.begin(9600);
  Serial.println("Encoder Test:");
  
  pinMode(M1_1,OUTPUT);
  pinMode(M1_2,OUTPUT);
  pinMode(M2_1,OUTPUT);
  pinMode(M2_2,OUTPUT);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    int code = (int) c;
    if (code == 16) {
      digitalWrite(ledPin, 1);
      turn_on_motors();
    Serial.println(code);
    }
    else {
      turn_off_motors();
      digitalWrite(ledPin, c);
      Serial.println(code);
    }
  }
}

void loop() {
//  long newPosition = myEncoder.read();
//  if (newPosition != oldPosition) {
//    oldPosition = newPosition;
//    Serial.print("Position: ");
//    Serial.println(newPosition);
//  }
delay(100);
}
