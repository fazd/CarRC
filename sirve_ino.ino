#define LED 8
#define LEDD 6

// Using http://slides.justen.eng.br/python-e-arduino as refference
int ENA=10;
int ENB=5;
int in1=9;
int in2=8;
int in3=7;
int in4=6;

void setup() {
    pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
  //pinMode(LED, OUTPUT);
    //pinMode(LEDD, OUTPUT);
    Serial.begin(9600);
}



void _mForward()
{ 
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(in1,LOW);//digital output
  digitalWrite(in2,HIGH);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  //aSerial.println("Forward");
}

void _stop(){
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
  digitalWrite(in1,LOW);//digital output
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
  //Serial.println("Stop");
}
//define back function/
void _mBack()
{
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  //Serial.println("Back");
}
//define left function/
void _mleft()
{
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(in1,LOW);
  digitalWrite(in2,HIGH);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  //Serial.println("Left");
}
//define right function/
void _mright()
{
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  //Serial.println("Right");
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        if (serialListener == 'W') {
          _mForward(); 
        }
        else if (serialListener == 'A') {
          _mleft(); 
        }
        else if (serialListener == 'S') {
          _mBack(); 
        }
        else if (serialListener == 'D') {
          _mright(); 
        }
        else if (serialListener == 'Q') {
          _stop(); 
        }
    }
}


