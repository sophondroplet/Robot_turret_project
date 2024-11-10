#include <Servo.h>
#define SERVO_X 7
#define SERVO_Y1 8
#define SERVO_Y2 6
#define SERVO_Z 9
#define FAST_MOTORS 11
#define SLOW_MOTOR 3
#define LIMIT_SWITCH
#define INIT_X_POS 90
#define INIT_Y_POS 90
#define INIT_Z_POS 100

Servo servo_x;
Servo servo_y1;
Servo servo_y2;
Servo servo_z;

bool fast_motors = false;
bool slow_motor = false;
bool reload = false;
int x_pos = INIT_X_POS;
int y_pos = INIT_Y_POS;
int z_pos = INIT_Z_POS;
int x_offset = 0;
int y_offset = 0;
int z_offset = 0;

void setup() {
  servo_x.attach(SERVO_X);
  servo_y1.attach(SERVO_Y1);
  servo_y2.attach(SERVO_Y2);
  servo_z.attach(SERVO_Z);

  pinMode(FAST_MOTORS, OUTPUT);
  pinMode(SLOW_MOTOR, OUTPUT);
  digitalWrite(FAST_MOTORS, LOW);
  digitalWrite(SLOW_MOTOR, LOW);
  servo_x.write(x_pos);
  servo_y1.write(y_pos);
  servo_y2.write(180-y_pos);
  servo_z.write(z_pos);
  Serial.begin(115200);
  Serial.setTimeout(100);
  establishConnection();
}

void loop() {
  // put your main code here, to run repeatedly:
  servo_x.write(180-x_pos);
  servo_y1.write(y_pos);
  servo_y2.write(180-y_pos);
  servo_z.write(z_pos);
  if(fast_motors == 1){
    digitalWrite(FAST_MOTORS, HIGH);
  }
  else{
    digitalWrite(FAST_MOTORS, LOW);
  }
  if(slow_motor == 1){
    digitalWrite(SLOW_MOTOR, HIGH);
  }
  else{
    digitalWrite(SLOW_MOTOR, LOW);
  }
}

void serialEvent(){
  String input = Serial.readStringUntil('\n');
  int r = parseR(input);
  if(r && reload == false){
    reloadSequence();
    reload = true;
  }
  else if(!r && reload == true){
    reload = false;
  }
  x_pos = parseX(input);
  y_pos = parseY(input);
  z_pos = parseZ(input);
  fast_motors = parseF(input);
  slow_motor = parseS(input);
  Serial.println("arduino: " + input + x_pos + y_pos + z_pos + fast_motors + slow_motor);
}

void establishConnection(){
  while(Serial.available() <= 0){
    Serial.print('C');
    delay(500);
  }
}

void reloadSequence(){
  int xDiff = INIT_X_POS - x_pos;
  int xStep = xDiff / abs(xDiff);
  int yDiff = INIT_Y_POS - y_pos;
  int yStep = yDiff / abs(yDiff);
  int zDiff = INIT_Z_POS - z_pos;
  int zStep = zDiff / abs(zDiff);
  while(true){
    if(x_pos == INIT_X_POS && y_pos == INIT_Y_POS && z_pos == INIT_Z_POS) break;
    if(x_pos != INIT_X_POS){
      x_pos += xStep;
      servo_x.write(x_pos);
    }
    if(y_pos != INIT_Y_POS){
      y_pos += yStep;
      servo_y1.write(y_pos);
      servo_y2.write(180 - y_pos);
    }
    if(z_pos != INIT_Z_POS){
      z_pos += zStep;
      servo_z.write(z_pos);
    }
  }
}
// "X(int:x(0-180))Y(int:y(0-180))Z(int:z(0-180))S(bool:slow)F(bool:fast)R(int:(0-1)"
int parseX(String input){
  input.remove(0,1);
  input.remove(input.indexOf('Y'));
  return input.toInt();

  //return input.substring(1, input.indexOf('Y').toInt();
  
}
int parseY(String input){
  input.remove(0, input.indexOf('Y')+1);
  input.remove(input.indexOf('Z'));
  return input.toInt();

  //return input.substring(input.indexOf('Y')+1, input.indexOf('S')).toInt(); 
}
int parseZ(String input){
  input.remove(0, input.indexOf('Z')+1);
  input.remove(input.indexOf('S'));
  return input.toInt();

  //return input.substring(input.indexOf('Z')+1, input.indexOf('S')).toInt();
}
bool parseS(String input){
  input.remove(0, input.indexOf('S')+1);
  input.remove(input.indexOf('F'));
  return input.toInt();

  //return input.substring(input.indexOf('S')+1, input.indexOf('F')).toInt();
}
bool parseF(String input){
  input.remove(0, input.indexOf('F')+1);
  input.remove(input.indexOf('R'));
  return input.toInt();
  //return input.substring(input.indexOf('F')+1).toInt();
}
bool parseR(String input){
  input.remove(0, input.indexOf('R')+1);
  return input.toInt();
}
