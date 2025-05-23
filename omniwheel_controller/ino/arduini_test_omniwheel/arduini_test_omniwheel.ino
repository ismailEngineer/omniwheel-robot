// === CONFIGURATION DES PINS ===
// Moteur 1
const int pwm1A = 5;
const int pwm1B = 6;
// Moteur 2
const int pwm2A = 7;
const int pwm2B = 8;
// Moteur 3
const int pwm3A = 9;
const int pwm3B = 10;

// Encodeurs
const int encA1 = 2, encB1 = 3;
const int encA2 = 18, encB2 = 19;
const int encA3 = 20, encB3 = 21;

// Compteurs de ticks
volatile long ticks1 = 0;
volatile long ticks2 = 0;
volatile long ticks3 = 0;

// Constante du nombre de ticks par tour
const int TICKS_PER_REV = 65;

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
}

void loop() {


  // Tourne les moteurs pendant 1 seconde en avant
  analogWrite(pwm1A, 150); analogWrite(pwm1B, 0);
  analogWrite(pwm2A, 150); analogWrite(pwm2B, 0);
  analogWrite(pwm3A, 150); analogWrite(pwm3B, 0);

  delay(1000); // Laisser tourner pendant 1 seconde

  // Stoppe les moteurs
  analogWrite(pwm1A, 0); analogWrite(pwm1B, 0);
  analogWrite(pwm2A, 0); analogWrite(pwm2B, 0);
  analogWrite(pwm3A, 0); analogWrite(pwm3B, 0);

  // Calcul des tours
  float tours1 = (float)ticks1 / TICKS_PER_REV;
  float tours2 = (float)ticks2 / TICKS_PER_REV;
  float tours3 = (float)ticks3 / TICKS_PER_REV;

  // Affiche les résultats
  Serial.println("=== Résultats après 1 seconde ===");
  Serial.print("Moteur 1 : "); Serial.print(ticks1); Serial.print(" ticks, ");
  Serial.print(tours1, 2); Serial.println(" tours");

  Serial.print("Moteur 2 : "); Serial.print(ticks2); Serial.print(" ticks, ");
  Serial.print(tours2, 2); Serial.println(" tours");

  Serial.print("Moteur 3 : "); Serial.print(ticks3); Serial.print(" ticks, ");
  Serial.print(tours3, 2); Serial.println(" tours");

  delay(50); // Pause avant prochaine mesure (boucle)
}

// === FONCTIONS D'INTERRUPTION ===

void readEncoder1() {
  bool A = digitalRead(encA1);
  bool B = digitalRead(encB1);
  if (A == B) ticks1++;
  else ticks1--;
}

void readEncoder2() {
  bool A = digitalRead(encA2);
  bool B = digitalRead(encB2);
  if (A == B) ticks2++;
  else ticks2--;
}

void readEncoder3() {
  bool A = digitalRead(encA3);
  bool B = digitalRead(encB3);
  if (A == B) ticks3++;
  else ticks3--;
}
