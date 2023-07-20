#include <Arduino.h>
#include <TimerOne.h>
#include "TM1637.h"            // 四位显示屏的库

// 光敏传感器
#define PIN_A 2
#define PIN_D 2

// TM1637显示屏
#define CLK 12
#define DIO 13
#define ON 1
#define OFF 0

// 时钟
int8_t TimeDisp[] = { 0x00, 0x00, 0x00, 0x00 };
unsigned char ClockPoint = 1;
unsigned char Update;
unsigned char halfsecond = 0;
unsigned char second ;
unsigned char minute = 0;
unsigned char hour = 0;

TM1637 tm1637(CLK, DIO);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);                                             // 打开Arduino Uno的串口连接
  Serial.flush ();
  tm1637.set();
  tm1637.init();
  tm1637.display(TimeDisp);
  Timer1.initialize(500000);          // 定时器中断的时间间隔被设置为 500 毫秒
  Timer1.attachInterrupt(TimingISR);  //declare the interrupt serve routine:TimingISR
}


void loop() {
  // put your main code here, to run repeatedly:
  int val;
  val = analogRead(PIN_A);
  Serial.print("s:a:");
  Serial.print(val);
  Serial.print(", d:");
  val = digitalRead(PIN_D);
  Serial.println(val);
  delay(500);
  if(Update == ON)
  {
    TimeUpdate();
    tm1637.display(TimeDisp);
  }

}

void TimingISR()
{
  halfsecond ++;
  Update = ON;
  if(halfsecond == 2){
    second ++;
    if(second == 60)
    {
      minute ++;
      if(minute == 60)
      {
        hour ++;
        if(hour == 24)hour = 0;
        minute = 0;
      }
      second = 0;
    }
    halfsecond = 0;
  }
 // Serial.println(second);
  ClockPoint = (~ClockPoint) & 0x01;
}

void TimeUpdate(void)
{
  if(ClockPoint)tm1637.point(POINT_ON);
  else tm1637.point(POINT_OFF);
  TimeDisp[0] = hour / 10;
  TimeDisp[1] = hour % 10;
  TimeDisp[2] = minute / 10;
  TimeDisp[3] = minute % 10;
  Update = OFF;
}

void serialEvent() {
  String inputString = "";
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inputString.indexOf("start")!=-1) {
      // 重置计时器
      hour = 0;
      halfsecond = 0;
      second = 0;
      minute = 0;
    }
    inputString = "";
    Serial.println(inputString);
  }
}
