#include <Arduino.h>

// Useful links to setup stm32 blue pill
// https://donneyfan.com/blog/usb-serial-for-blue-pill-stm32-with-platformio
// https://github.com/platformio/platform-ststm32/issues/53

#define N_PLAYERS 8

// Don't use PA11 and PA12, they're used for USB
// Don't use PB5, for some reason, fucks up the interrupts

#define PIN_T1P1 PB11
#define PIN_T1P2 PB10
#define PIN_T1P3 PB1
#define PIN_T1P4 PB0

#define PIN_T2P1 PB12
#define PIN_T2P2 PB13
#define PIN_T2P3 PB14
#define PIN_T2P4 PB15

uint8_t PIN_PLAYERS[N_PLAYERS] = {PIN_T1P1, PIN_T1P2, PIN_T1P3, PIN_T1P4,
                                  PIN_T2P1, PIN_T2P2, PIN_T2P3, PIN_T2P4};

uint8_t inputs = 0;
volatile bool isButtonPressed = false;
volatile bool hasPrinted = false;

void ResetInputs()
{
  inputs = 0;
  hasPrinted = false;
  isButtonPressed = false;
}

inline void ISRCore(const uint8_t playerID)
{
  if(!isButtonPressed)
  {
    isButtonPressed = true;
    inputs |= (1 << playerID);
  }
}

void ISRT1P1()
{
  ISRCore(0);
}

void ISRT1P2()
{
  ISRCore(1);
}

void ISRT1P3()
{
  ISRCore(2);
}

void ISRT1P4()
{
  ISRCore(3);
}

void ISRT2P1()
{
  ISRCore(4);
}

void ISRT2P2()
{
  ISRCore(5);
}

void ISRT2P3()
{
  ISRCore(6);
}

void ISRT2P4()
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

  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[0]), ISRT1P1, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[1]), ISRT1P2, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[2]), ISRT1P3, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[3]), ISRT1P4, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[4]), ISRT2P1, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[5]), ISRT2P2, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[6]), ISRT2P3, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_PLAYERS[7]), ISRT2P4, FALLING);
  
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
