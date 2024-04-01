#include <Arduino.h>
#include <DMXSerial.h>

// global used vars
int channel = 1;
int value = 0;
int dmx_values[512];

// setup serial and dmx
void setup()
{
  Serial.begin(115200);
  DMXSerial.init(DMXController);
}

// helper function to update all 512 channels
void update_dmx()
{
  for (int i = 0; i < 512; i++)
  {
    DMXSerial.write(i, dmx_values[i]);
  }
}

// loop every tick
void loop()
{
  // update dmx when no serial events
  while (!Serial.available())
  {
    update_dmx();
  }

  // read current serial byte
  int current = Serial.read();

  // update value when byte is a number
  if ((current >= '0') && (current <= '9'))
  {
    value = 10 * value + current - '0';
  }

  // check for commands
  else
  {
    // if command is channel
    if (current == 'c')
    {
      // fallback when channel size is not valid
      if ((value < 1) || (value > 512))
      {
        channel = 1;
      }

      // update channel
      else
      {
        channel = value;
      }
    }

    // if command is channel
    else if (current == 'v')
    {
      // fallback when value size is not valid
      if ((value < 0) || (value > 255))
      {
        value = 0;
      }

      // update value
      else
      {
        dmx_values[channel] = value;
      }
    }

    // reset value after command
    value = 0;
  }
}