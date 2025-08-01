// === CONFIGURATION DES PINS ===
// Moteur 1 --> avant
const int pwm1A = 9;
const int pwm1B = 10;
// Moteur 2 --> droite
const int pwm2A = 7;
const int pwm2B = 8;
// Moteur 3 --> Gauche
const int pwm3A = 6;
const int pwm3B = 5;

// Encodeurs
const int encA1 = 2, encB1 = 3;
const int encA2 = 18, encB2 = 19;
const int encA3 = 21, encB3 = 20;

// Compteurs de ticks
volatile long ticks1 = 0;
volatile long ticks2 = 0;
volatile long ticks3 = 0;

volatile long ticks1_v = 0;
volatile long ticks2_v = 0;
volatile long ticks3_v = 0;


unsigned long lastTime = 0;
// Constante du nombre de ticks par tour
const int TICKS_PER_REV = 445;
const float DIAMETRE_ROUE = 0.055; // en mètres
const float perimetre = PI * DIAMETRE_ROUE;
const int CONTROL_PERIOD_MS = 50; // Période d’échantillonnage (50 ms)

float distance1, vitesse1;   
float distance2, vitesse2;
float distance3, vitesse3;

bool triggerMotor = false;



float integral_error = 0;
float target_vitesse1 = -0.5,target_vitesse2 = 0.4,target_vitesse3 = 0.4;
float pwm_min = 50;
float Kp = 500;      // à régler
float Ki = 600.0;      // à régler
float k_ff = 50;
float integral_error_1 = 0,integral_error_2 = 0,integral_error_3 = 0;
int pwm_value_1, pwm_value_2, pwm_value_3;

String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);

  // Configuration moteurs en sortie
  pinMode(pwm1A, OUTPUT);
  pinMode(pwm1B, OUTPUT);
  pinMode(pwm2A, OUTPUT);
  pinMode(pwm2B, OUTPUT);
  pinMode(pwm3A, OUTPUT);
  pinMode(pwm3B, OUTPUT);

  // Encodeurs en entrée
  pinMode(encA1, INPUT);
  pinMode(encB1, INPUT);
  pinMode(encA2, INPUT);
  pinMode(encB2, INPUT);
  pinMode(encA3, INPUT);
  pinMode(encB3, INPUT);

  // Attach interruptions sur les canaux A
  attachInterrupt(digitalPinToInterrupt(encA1), readEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encA2), readEncoder2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encA3), readEncoder3, CHANGE);

    // Réinitialise les ticks
  ticks1 = 0;
  ticks2 = 0;
  ticks3 = 0;

  stopAllMotors();
}

void loop() {


//  // Tourne les moteurs pendant 1 seconde en avant
//  if (triggerMotor) {
//  turnM1(50,-1);
//  turnM2(50,-1);
//  turnM3(50,-1);
//  delay(5); // Laisser tourner pendant 1 seconde
//  }
//  else {
//    // Stoppe les moteurs
//  stopAllMotors();
//  delay(5); // Laisser tourner pendant 1 seconde
//  }
  
  // Calcul des tours
  float tours1 = (float)ticks1 / TICKS_PER_REV;
  float tours2 = (float)ticks2 / TICKS_PER_REV;
  float tours3 = (float)ticks3 / TICKS_PER_REV;


  unsigned long currentTime = millis();
  
  if (currentTime - lastTime >= CONTROL_PERIOD_MS) { // toutes les 100 ms
    
    float tours1_v = (float)ticks1_v / TICKS_PER_REV;
    float tours2_v = (float)ticks2_v / TICKS_PER_REV;
    float tours3_v = (float)ticks3_v / TICKS_PER_REV;
  
    
    distance1 = tours1_v * perimetre; 
    vitesse1 = distance1 / 0.05; // m/s
    
    distance2 = tours2_v * perimetre;
    vitesse2 = distance2 / 0.05; // m/s
    
    distance3 = tours3_v * perimetre;
    vitesse3 = distance3 / 0.05; // m/s

//    float error = target_vitesse1 - vitesse1;
//    integral_error += error * 0.05;
//
//    float feedforward = k_ff * target_vitesse1;
//
//    // PI Controller
//    float output = Kp * error + Ki * integral_error;
//    
////    // Ajout seuil minimal de démarrage
////    if (target_vitesse1 != 0 && abs(output) < pwm_min) {
////      output = pwm_min * (output > 0 ? 1 : -1);
////    }
//
//    int pwm_value = constrain(abs(output), 0, 255);

    

    // if (output >= 0) turnM1(pwm_value, 1); else turnM1(-pwm_value, -1);

    pwm_value_1 = controller_pid(vitesse1,target_vitesse1,Kp,Ki,&integral_error_1);
    pwm_value_2 = controller_pid(vitesse2,target_vitesse2,Kp,Ki,&integral_error_2);
    pwm_value_3 = controller_pid(vitesse3,target_vitesse3,Kp,Ki,&integral_error_3);

    if (pwm_value_1 >= 0) turnM1(pwm_value_1, 1); else turnM1(-pwm_value_1, -1);
    if (pwm_value_2 >= 0) turnM2(pwm_value_2, 1); else turnM2(-pwm_value_2, -1);
    if (pwm_value_3 >= 0) turnM3(pwm_value_3, 1); else turnM3(-pwm_value_3, -1);

    ticks1_v = 0; // reset pour le prochain intervalle
    ticks2_v = 0; // reset pour le prochain intervalle
    ticks3_v = 0; // reset pour le prochain intervalle

    // Debug
//    Serial.print("vitesse1: "); Serial.print(vitesse1);
//    Serial.print(" | output: "); Serial.print(output);
//    Serial.print(" | PWM: "); Serial.print(pwm_value);
//    Serial.print(" | Target: "); Serial.println(target_vitesse1);

    Serial.print("vitesse1: "); Serial.print(vitesse1);
    Serial.print("| vitesse2: "); Serial.print(vitesse2);
    Serial.print("| vitesse3: "); Serial.println(vitesse3);
    
//    Serial.print(" | PWM: "); Serial.print(pwm_value_1);Serial.print(" | Target: "); Serial.println(target_vitesse1);
//    Serial.print(" | PWM: "); Serial.print(pwm_value_2);Serial.print(" | Target: "); Serial.println(target_vitesse2);
//    Serial.print(" | PWM: "); Serial.print(pwm_value_3);Serial.print(" | Target: "); Serial.println(target_vitesse3);
    lastTime = currentTime;
}
  // Affiche les résultats
//  Serial.println("=== Résultats après 1 seconde ===");
//  Serial.print("Moteur 1 : "); Serial.print(ticks1); Serial.print(" ticks, ");
//  Serial.print(tours1, 2); Serial.print(" tours, ");
//  Serial.print(distance1, 2); Serial.print(" m, ");
//  Serial.print(vitesse1, 2); Serial.println(" m/s");
//
//  Serial.print("Moteur 2 : "); Serial.print(ticks2); Serial.print(" ticks, ");
//  Serial.print(tours2, 2); Serial.print(" tours, ");
//  Serial.print(distance2, 2); Serial.print(" m, ");
//  Serial.print(vitesse2, 2); Serial.println(" m/s");
//
//  Serial.print("Moteur 3 : "); Serial.print(ticks3); Serial.print(" ticks, ");
//  Serial.print(tours3, 2); Serial.print(" tours, ");
//  Serial.print(distance3, 2); Serial.print(" m, ");
//  Serial.print(vitesse3, 2); Serial.println(" m/s");

  delay(10); // Pause avant prochaine mesure (boucle)
}

int controller_pid(float v, float target_v, float kp_v, float ki_v, float* integral_error)
{
    float error = target_v - v;
    *integral_error += error * 0.05;

    // PI Controller
    float output = kp_v * error + ki_v * (*integral_error);

    int pwm_value = constrain(abs(output), 0, 255);
    
    if (output >= 0) pwm_value = pwm_value; else pwm_value *= -1;
    
    return pwm_value;
}

void turnM1(int velocity, int dir){
  if (dir > 0 ) {
    analogWrite(pwm1A, velocity); analogWrite(pwm1B, 0);
  }
  else if (dir < 0 ) {
    analogWrite(pwm1A, 0); analogWrite(pwm1B, velocity);
  }
}

void turnM2(int velocity, int dir){
  if (dir > 0 ) {
    analogWrite(pwm2A, velocity); analogWrite(pwm2B, 0);
  }
  else if (dir < 0 ) {
    analogWrite(pwm2A, 0); analogWrite(pwm2B, velocity);
  }
}

void turnM3(int velocity, int dir){
  if (dir > 0 ) {
    analogWrite(pwm3A, velocity); analogWrite(pwm3B, 0);
  }
  else if (dir < 0 ) {
    analogWrite(pwm3A, 0); analogWrite(pwm3B, velocity);
  }
}

void stopAllMotors(){
  turnM1(0,1);
  turnM2(0,1);
  turnM3(0,1);
}

// === FONCTIONS D'INTERRUPTION ===

void serialEvent() {
//  if (Serial.available()) {
//    char c = Serial.read(); // on lit 1 caractère
//    if (c == 'z') triggerMotor = true;
//    else if (c == 's') triggerMotor = false;
//  }

  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
   }
  if (stringComplete) {
    parseCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void parseCommand(String cmd) {
  int m1_speed = 0, m2_speed = 0, m3_speed = 0;

  // Ex: M1:150;M2:-100;M3:0
  int idxM1 = cmd.indexOf("M1:");
  int idxM2 = cmd.indexOf("M2:");
  int idxM3 = cmd.indexOf("M3:");

  if (idxM1 >= 0) m1_speed = cmd.substring(idxM1 + 3, cmd.indexOf(';', idxM1)).toInt();
  if (idxM2 >= 0) m2_speed = cmd.substring(idxM2 + 3, cmd.indexOf(';', idxM2)).toInt();
  if (idxM3 >= 0) m3_speed = cmd.substring(idxM3 + 3).toInt();

  Serial.print("M1 = "); Serial.println(m1_speed);
  Serial.print("M2 = "); Serial.println(m2_speed);
  Serial.print("M3 = "); Serial.println(m3_speed);

  if (m1_speed >= 0) turnM1(m1_speed, 1); else turnM1(-m1_speed, -1);
  if (m2_speed >= 0) turnM2(m2_speed, 1); else turnM2(-m2_speed, -1);
  if (m3_speed >= 0) turnM3(m3_speed, 1); else turnM3(-m3_speed, -1);
}


void readEncoder1() {
  bool A = digitalRead(encA1);
  bool B = digitalRead(encB1);
  if (A == B) {
    ticks1++;
    ticks1_v++;
  }
  else {
    ticks1--;
    ticks1_v--;
  }
}

void readEncoder2() {
  bool A = digitalRead(encA2);
  bool B = digitalRead(encB2);
  if (A == B) {
    ticks2++;
    ticks2_v++;
  }
  else {
    ticks2--;
    ticks2_v--;
  }
}

void readEncoder3() {
  bool A = digitalRead(encA3);
  bool B = digitalRead(encB3);
  if (A == B) {
    ticks3++;
    ticks3_v++;
  }
  else {
    ticks3--;
    ticks3_v--;
  }
}
