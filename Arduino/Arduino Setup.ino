
char input;
int coffee_pin = 11;
int cafecreme_pin = 12; 
int cafelait_pin = 13;
int cappu_pin = 4;
int espresso_pin = 5;
int doubleEspresso_pin = 6;
int hotchoc = 7;
int hotwater = 8;
int wienerMelange = 3;
int select = 2;

//int left_pin = 9;
//int right_pin = 10;


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(coffee_pin, OUTPUT);
  pinMode(cafecreme_pin, OUTPUT);
  pinMode(cafelait_pin, OUTPUT);
  pinMode(cappu_pin, OUTPUT);
  pinMode(espresso_pin, OUTPUT);
  pinMode(doubleEspresso_pin, OUTPUT);
  pinMode(hotchoc, OUTPUT);
  pinMode(wienerMelange, OUTPUT);
  pinMode(hotwater, OUTPUT);  
  //pinMode(left_pin, OUTPUT);
  //pinMode(right_pin, OUTPUT);
  //pinMode(select, OUTPUT);  
  
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {

  digitalWrite(coffee_pin, LOW);
  digitalWrite(cafecreme_pin, LOW);
  digitalWrite(cafelait_pin, LOW);
  digitalWrite(cappu_pin, LOW);
  digitalWrite(espresso_pin, LOW);
  digitalWrite(doubleEspresso_pin, LOW);
  digitalWrite(hotchoc, LOW);
  digitalWrite(wienerMelange, LOW);
  digitalWrite(hotwater, LOW);  
  //digitalWrite(left_pin, LOW);
  //digitalWrite(right_pin, LOW);
  //digitalWrite(select, LOW);  


  if (Serial.available() > 0) {
    input = Serial.read();

    if (input == '1'){
        digitalWrite(coffee_pin, HIGH);  
        delay(750);              
        digitalWrite(coffee_pin, LOW);
        delay(750);             
        Serial.print("Making Coffee");
    } else if (input == '2'){
        digitalWrite(cafecreme_pin, HIGH);  
        delay(750);              
        digitalWrite(cafecreme_pin, LOW);             
        Serial.print("Making cafecreme");
    }else if (input == '3'){
        digitalWrite(cafelait_pin, HIGH);  
        delay(750);              
        digitalWrite(cafelait_pin, LOW);
        delay(750);             
        Serial.print("Making cafe au lait");
    }else if (input == '4'){
        digitalWrite(cappu_pin, HIGH);  
        delay(750);              
        digitalWrite(cappu_pin, LOW);
        delay(750);             
        Serial.print("Making cappuccino");
    }else if (input == '5'){
        digitalWrite(espresso_pin, HIGH);  
        delay(750);              
        digitalWrite(espresso_pin, LOW); 
        delay(750);            
        Serial.print("Making espresso");
    }else if (input == '6'){
        digitalWrite(doubleEspresso_pin, HIGH);  
        delay(750);              
        digitalWrite(doubleEspresso_pin, LOW);
        delay(750);             
        Serial.print("Making double espresso");
    }else if (input == '7'){
        digitalWrite(hotchoc, HIGH);  
        delay(750);              
        digitalWrite(hotchoc, LOW); 
        delay(750);            
        Serial.print("Making hot chocolate");
    }else if (input == '8'){
        digitalWrite(hotwater, HIGH);  
        delay(750);              
        digitalWrite(hotwater, LOW); 
        delay(750);            
        Serial.print("Making hot water");
    }else if (input == '9'){
        digitalWrite(wienerMelange, HIGH);  
        delay(750);              
        digitalWrite(wienerMelange, LOW); 
        delay(750);            
        Serial.print("Making Wiener Melange");
    }
  }
  
  
}
