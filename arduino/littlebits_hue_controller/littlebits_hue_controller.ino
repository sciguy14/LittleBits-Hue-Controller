// LittleBits Hue Controller by Jeremy Blum
// Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.
// http://www.jeremyblum.com
// File: littlebits_hue_controller.ino
// License: GPL v3 (http://www.gnu.org/licenses/gpl.html)

//Interface Pins
const int on_off_button_pin       = 0;  //D0
const int brightness_dial_pin     = A0; //A0
const int mood_button_pin         = A1; //A1
const int brightness_bargraph_pin = 5;  //D5
const int mood_readout            = 9;  //D9

//Constant Values
const int num_moods = 10; //10 mood settings (0-9)

//Button Debouncing & Knob Tracking Variables
boolean on_off_button_last    = LOW;
boolean on_off_button_current = LOW;
boolean mood_button_last      = LOW;
boolean mood_button_current   = LOW;
int     brightness_last;
int     brightness_current;
int     brightness_temp;
int     dial_breaks[4] = {15, 90, 165, 240}; // Values from 0 to 255 where the dial brightness levels occur

//State Variables
int mood = 0;           //Lighting Mood Selection (0-9)
boolean on_off = false; //Light State (on/off, true/false)
boolean transmit = false;

void setup()
{
  //Set Pin Modes
  pinMode(brightness_bargraph_pin, OUTPUT);
  pinMode(mood_readout, OUTPUT);

  //Start Serial communication
  Serial.begin(9600);
  
  //Setup Starting Brightness
  brightness_last = getBrightness(0);
  
  //Setup starting Mood Readout
  setMoodReadout(mood);
}

void loop()
{
  //On/Off Button Debouncing
  on_off_button_current = debounce(on_off_button_last, on_off_button_pin);
  if (on_off_button_current == HIGH && on_off_button_last == LOW)
  {
    on_off = !on_off;
    transmit = true;
  }
  on_off_button_last = on_off_button_current;
  
  //Mood Button Debouncing
  mood_button_current = debounce(mood_button_last, mood_button_pin);
  if (mood_button_current == HIGH && mood_button_last == LOW)
  {
    mood = mood++;
    if (mood >= num_moods) mood = 0;
    setMoodReadout(mood);
    if (on_off) transmit = true;
  }
  mood_button_last = mood_button_current;
  
  //brightness Selection
  brightness_temp = getBrightness(2);
  if (brightness_temp != 0) brightness_current = brightness_temp;
  if (brightness_current != brightness_last)
  {
    if (on_off) transmit = true;
  }
  brightness_last = brightness_current;
  
  //Transmit knob changes
  if (transmit)
  {    
    if (on_off)
    {
      setBargraph(brightness_current);
      Serial.print("on, ");
      Serial.print(mood);
      Serial.print(", ");
      Serial.println(brightness_current);
    }
    else
    {
      setBargraph(0);
      Serial.println("off");
    }
    transmit = false;  
  }
  
}

//Outputs value from 0-5. 0 means we're in a hysteresis zone, and the brightness should not change.
int getBrightness(int hysteresis)
{
  int brightness_raw = map(analogRead(brightness_dial_pin), 0, 1023, 0, 255);
  int output = 0;
  if                                                    (brightness_raw <= dial_breaks[0]-hysteresis) output = 1;
  else if (brightness_raw > dial_breaks[0]+hysteresis && brightness_raw <= dial_breaks[1]-hysteresis) output = 2;
  else if (brightness_raw > dial_breaks[1]+hysteresis && brightness_raw <= dial_breaks[2]-hysteresis) output = 3;
  else if (brightness_raw > dial_breaks[2]+hysteresis && brightness_raw <= dial_breaks[3]-hysteresis) output = 4;
  else if (brightness_raw > dial_breaks[3]+hysteresis)                                                output = 5;
  return output;
}

void setBargraph(int val)
{
  //Bargraph Bit Limits
  //0>1  1>2  2>3  3>4  4>5 
  //27,  76,  124, 174, 229
  if      (val == 0) analogWrite(brightness_bargraph_pin, 0);
  else if (val == 1) analogWrite(brightness_bargraph_pin, 50);
  else if (val == 2) analogWrite(brightness_bargraph_pin, 100);
  else if (val == 3) analogWrite(brightness_bargraph_pin, 150);
  else if (val == 4) analogWrite(brightness_bargraph_pin, 200);
  else if (val == 5) analogWrite(brightness_bargraph_pin, 250);
}

void setMoodReadout(int mood)
{
  analogWrite(mood_readout, map(mood, 0, 99, 0, 255));
}

boolean debounce(boolean last, int btn_pin)
{
  boolean current = digitalRead(btn_pin);
  if (last != current)
  {
    delay(5);
    current = digitalRead(btn_pin);
  }
  return current;
}
