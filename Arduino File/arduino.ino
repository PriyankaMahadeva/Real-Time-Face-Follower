
#include <Servo.h>
Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo
int x;
int y;
int prevX;
int prevY;
void setup()
{
  Serial.begin(9600);
  servoVer.attach(9); //Attach Vertical Servo to Pin 5
  servoHor.attach(10); //Attach Horizontal Servo to Pin 6
  servoVer.write(90);
  servoHor.write(90);
  pinMode(6, OUTPUT);
}
void Pos()
{
  if(prevX != x || prevY != y)
  {
    int servoX = map(x, 600, 0, 70, 179);
    int servoY = map(y, 450, 0, 179, 95);
    servoX = min(servoX, 109);
    servoX = max(servoX, 55);
    servoY = min(servoY, 179);
    servoY = max(servoY, 10);
    
    servoHor.write(servoX);
    servoVer.write(servoY);
  }
}
void loop()
{
  if(Serial.available() > 0)
  {
    
    if(Serial.read() == 'X')
    {
      digitalWrite(6, HIGH);
      x = Serial.parseInt();
      if(Serial.read() == 'Y')
      {
        y = Serial.parseInt();
        y = y+90;
       Pos();
      }
    }
    while(Serial.available() > 0)
    {
      Serial.read();
    }
  }
}
