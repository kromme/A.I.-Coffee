// assign pin numbers. The numbers on the side of the arduino.
// these are connected to the buttons of the drinks.

int coffee_pin = 3;
int espresso_pin = 4;
int capu_pin = 5;
int heetwater_pin = 6;
int latte_pin = 7;
int choco_pin = 8;


// duration for output
int time = 100;

// initial command
int command = 0;

// set the mode of the pins to output, as we're going to send signals, not receive them.
void setup() {
  pinMode(coffee_pin, OUTPUT);
  pinMode(espresso_pin, OUTPUT);
  pinMode(capu_pin, OUTPUT);
  pinMode(heetwater_pin, OUTPUT);
  pinMode(latte_pin, OUTPUT);
  pinMode(choco_pin, OUTPUT);
  Serial.begin(9600);
}


// The continuous loop
void loop() {
  //receive command from the python script, via serial.
  if (Serial.available() > 0){
    
    // read the value given by Python
    command = Serial.read();

    // execute the send_command function
    send_command(command);
   
    // reset everything
    reset();
  }
 reset();
}

// pauze function
void pauze(){
  pauze();
}

// functions for the alternatives. Activate the pin, wait X milliseconds, deactivate pin.
void coffee(){
  digitalWrite(coffee_pin, HIGH);
  pauze();
  digitalWrite(coffee_pin, LOW);
}
void espresso(){
  digitalWrite(espresso_pin, HIGH);
  pauze();
  digitalWrite(espresso_pin, LOW);
}
void capu(){
  digitalWrite(capu_pin, HIGH);
  pauze();
  digitalWrite(capu_pin, LOW);
}
void heetwater(){
  digitalWrite(heetwater_pin, HIGH);
  pauze();
  digitalWrite(heetwater_pin, LOW);
}
void latte(){
  digitalWrite(latte_pin, HIGH);
  pauze();
  digitalWrite(latte_pin, LOW);
}
void choco(){
  digitalWrite(choco_pin, HIGH);
  pauze();
  digitalWrite(choco_pin, LOW);
}


// create the reset function. Reset all pins
void reset(){
  digitalWrite(coffee_pin, LOW);
  digitalWrite(espresso_pin, LOW);
  digitalWrite(capu_pin, LOW);
  digitalWrite(latte_pin, LOW);
  digitalWrite(heetwater_pin, LOW);
  digitalWrite(choco_pin, LOW);
}


// case when then statements. command is the parameter which is a value from Python. By using the case statements we correspond the given value with a function.
void send_command(int command){
  switch (command){
     Serial.print(command);
     
     //reset command
     case 0: reset(); break;

     // single command
     case 1: coffee(); break;
     case 2: espresso(); break;
     case 3: capu(); break;
     case 4: heetwater(); break;
     case 5: latte(); break;
     case 6: choco(); break;


     case 10: pauze(); break;
     default: Serial.print("Inalid Command\n");
    }
}
