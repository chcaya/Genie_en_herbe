#include <Arduino.h>

#define N_PLAYERS 8

#define PIN_E1J1 15
#define PIN_E1J2 4
#define PIN_E1J3 16
#define PIN_E1J4 17

#define PIN_E2J1 13
#define PIN_E2J2 14
#define PIN_E2J3 27
#define PIN_E2J4 26

uint8_t PIN_PLAYERS[N_PLAYERS] = {PIN_E1J1, PIN_E1J2, PIN_E1J3, PIN_E1J4,
                                  PIN_E2J1, PIN_E2J2, PIN_E2J3, PIN_E2J4};

uint8_t inputs = 0;
bool isButtonPressed = false;
bool hasPrinted = false;

void ResetInputs()
{
  inputs = 0;
  hasPrinted = false;
  isButtonPressed = false;
  interrupts();
}

inline void ISRCore(const uint8_t playerID)
{
  if(!isButtonPressed)
  {
    isButtonPressed = true;
    inputs |= (1 << playerID);
  }
}

void IRAM_ATTR ISRP1()
{
  ISRCore(0);
}

void IRAM_ATTR ISRP2()
{
  ISRCore(1);
}

void IRAM_ATTR ISRP3()
{
  ISRCore(2);
}

void IRAM_ATTR ISRP4()
{
  ISRCore(3);
}

void IRAM_ATTR ISRP5()
{
  ISRCore(4);
}

void IRAM_ATTR ISRP6()
{
  ISRCore(5);
}

void IRAM_ATTR ISRP7()
{
  ISRCore(6);
}

void IRAM_ATTR ISRP8()
{
  ISRCore(7);
}


void setup()
{
  Serial.begin(115200);

  for(uint8_t i = 0; i < N_PLAYERS; ++i)
  {
    pinMode(PIN_PLAYERS[i], INPUT_PULLUP);
  }

  attachInterrupt(PIN_PLAYERS[0], ISRP1, FALLING);
  attachInterrupt(PIN_PLAYERS[1], ISRP2, FALLING);
  attachInterrupt(PIN_PLAYERS[2], ISRP3, FALLING);
  attachInterrupt(PIN_PLAYERS[3], ISRP4, FALLING);
  attachInterrupt(PIN_PLAYERS[4], ISRP5, FALLING);
  attachInterrupt(PIN_PLAYERS[5], ISRP6, FALLING);
  attachInterrupt(PIN_PLAYERS[6], ISRP7, FALLING);
  attachInterrupt(PIN_PLAYERS[7], ISRP8, FALLING);

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

  if(isButtonPressed && !hasPrinted)
  {
    Serial.println(inputs);
    hasPrinted = true;
  }
}
