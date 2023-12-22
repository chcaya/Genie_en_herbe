#include <Arduino.h>

#define MAX_UINT8_T 255

#define N_PLAYERS 8

#define PIN_E1J1 15
#define PIN_E1J2 4
#define PIN_E1J3 16
#define PIN_E1J4 17

// #define PIN_E2J1 5
// #define PIN_E2J2 18
// #define PIN_E2J3 19
// #define PIN_E2J4 21

#define PIN_E2J1 13
#define PIN_E2J2 14
#define PIN_E2J3 27
#define PIN_E2J4 26

uint8_t PIN_PLAYERS[N_PLAYERS] = {PIN_E1J1, PIN_E1J2, PIN_E1J3, PIN_E1J4,
                                  PIN_E2J1, PIN_E2J2, PIN_E2J3, PIN_E2J4};

uint8_t inputs = 0;
unsigned long lastTime = 0;
bool hasReset = false;

void ResetInputs()
{
  hasReset = true;
  inputs = 0;
}

void ReadInputs()
{
  for(uint8_t i = 0; i < N_PLAYERS; ++i)
  {
    if (!digitalRead(PIN_PLAYERS[i])) // Invert the input state (due to pull-up resistors)
    {
      inputs |= (1 << i); // Set the ith bit if the input is active
    }
  }
}



void setup()
{
  Serial.begin(9600);

  lastTime = millis();

  for(uint8_t i = 0; i < N_PLAYERS; ++i)
  {
    pinMode(PIN_PLAYERS[i], INPUT_PULLUP);
  }

  ResetInputs();
}

void loop()
{
  if (Serial.available() > 0)
  {
    char command = Serial.read();
    if (command == 'R')
    {
      // Reset scores requested, perform the reset
      ResetInputs();
    }
  }

  if(hasReset)
  {
    ReadInputs();

    if(inputs != 0)
    {
      Serial.println(inputs);
    }

    if(inputs != 0){hasReset = false;}
  }
}
