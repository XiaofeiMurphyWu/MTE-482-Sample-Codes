
void setup() {
  // put your setup code here, to run once:

  pinMode(2,OUTPUT);    //S2 for inputs
  pinMode(3,OUTPUT);    //S1 for inputs
  pinMode(4,OUTPUT);    //S0 for inputs
  
  pinMode(5,OUTPUT);    //S2 for outputs
  pinMode(6,OUTPUT);    //S1 for outputs
  pinMode(7,OUTPUT);    //S0 for outputs

  pinMode(8,OUTPUT);    //S2 for mux outputs
  pinMode(9,OUTPUT);    //S1 for mux outputs
  pinMode(10,OUTPUT);   //S0 for mux outputs

  pinMode(A1,INPUT);    //mux input

  //initiate serial monitor
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int input1[8];
  int input2[8];
  int input3[8];

  // Select a column mux
  for(int mpin=0; mpin<=2; mpin++){

    /*Serial.print("Mux #");
    Serial.print(mpin);
    Serial.println(": ");*/

    selectMuxPin(mpin);
      
    // Select individual copper tape
    for (int pin=7; pin>=0; pin--)
    {
      selectOutputPin(pin);
      readInput(input1, input2, input3);
      /*Serial.print("Col ");
      Serial.print(pin);
      Serial.print(": ");*/
      printInput(input1, input2, input3);
  
      delay(10);
    }    
  }

  Serial.println("End of cycle.");

  /*int mux = 1;
  int pin = 5;
  
  selectMuxPin(mux);
  selectOutputPin(pin);
  readInput(input1, input2, input3);
  Serial.print("Mux ");
  Serial.print(mux);
  Serial.print(", ");
  Serial.print("Col ");
  Serial.print(pin);
  Serial.print(": ");
  printInput(input1, input2, input3);*/
  
}

// Turn on channel to read voltage
void selectInputPin(byte pin){
  if (pin >= 4){
    digitalWrite(2, HIGH);
    pin = pin - 4; }
  else digitalWrite(2, LOW);
    
  if (pin >= 2){
    digitalWrite(3, HIGH);
    pin = pin - 2; }
  else digitalWrite(3, LOW);
    
  if (pin == 1) digitalWrite(4, HIGH);
  else digitalWrite(4, LOW);
}

// Turn on channel to supply voltage
void selectOutputPin(byte pin){
  
  if (pin >= 4){
    digitalWrite(5, HIGH);
    pin = pin - 4; }
  else digitalWrite(5, LOW);
    
  if (pin >= 2){
    digitalWrite(6, HIGH);
    pin = pin - 2; }
  else digitalWrite(6, LOW);
    
  if (pin == 1) digitalWrite(7, HIGH);
  else digitalWrite(7, LOW);
}

// Turn on channel to select mux
void selectMuxPin(byte pin){
  
  if (pin >= 4){
    digitalWrite(8, HIGH);
    pin = pin - 4; }
  else digitalWrite(8, LOW);
    
  if (pin >= 2){
    digitalWrite(9, HIGH);
    pin = pin - 2; }
  else digitalWrite(9, LOW);
    
  if (pin == 1) digitalWrite(10, HIGH);
  else digitalWrite(10, LOW);
}

void readInput(int input1[], int input2[], int input3[]){
  int inSignal1 = 0;
  int inSignal2 = 0;
  int inSignal3 = 0;

  for (int pin=0; pin<=7; pin++){
    selectInputPin(pin);
    inSignal1 = analogRead(A0);
    delay(10);
    inSignal2 = analogRead(A1);
    delay(10);
    inSignal3 = analogRead(A2);
    
    input1[pin] = inSignal1;
    input2[pin] = inSignal2;
    input3[pin] = inSignal3;

    //delay(5);

  } 
}

void printInput(int input1[], int input2[], int input3[]){  
  
  for (int index=7; index>=0; index--){
      Serial.print(input1[index]);
      Serial.print(",");
  }

  for (int index=7; index>=0; index--){
      Serial.print(input2[index]);
      Serial.print(",");
  }

  // Special print for rmux 3 due to its wiring
  for (int index=3; index<=6; index++){
      Serial.print(input3[index]);
      Serial.print(",");
  }
  
  Serial.print(input3[2]);
  Serial.print(",");
  Serial.print(input3[7]);
  Serial.println();
    
  //Serial.println();
}
