const int  debounceTime = 100; //  20 works better than great !

byte colPins[] = {12, 11, 10,  9,  8,  7, 6, 5};
byte rowPins[] = {A0, A1, A2, A3, A4, A5, 3, 4};

byte numCols = sizeof (colPins);
byte numRows = sizeof (rowPins);

// -------------------------------------
void setup ()
{
  Serial.begin (9600);

  for (int column = 0; column < numCols; column++)
  {
    pinMode      (colPins[column], OUTPUT);
    digitalWrite (colPins[column], HIGH);
  }

  for (int row = 0; row < numRows; row++)
  {
    pinMode      (rowPins[row], INPUT);
    digitalWrite (rowPins[row], HIGH);
  }

  pinMode (LED_BUILTIN, OUTPUT);

  Serial.print ("Dartboard ");
  Serial.print (sizeof (colPins));
  Serial.print ("X");
  Serial.print (sizeof (rowPins));
  Serial.println (" OK");
}

// -------------------------------------
void loop ()
{
  char key = getKey ();

  if (key != 0)
  {
    Serial.println (key);
  }
}

// -------------------------------------
char getKey ()
{
  char key = 0;

  for (int column = 0; column < numCols; column++)
  {
    digitalWrite (colPins[column], LOW);

    for (int row = 0; row < numRows; row++)
    {
      if (digitalRead (rowPins[row]) == LOW)
      {
        delay (debounceTime);

        while (digitalRead (rowPins[row]) == LOW)
        {
          //wait for key to be released
        }
        Serial.print (column);
        Serial.print (" - ");
        Serial.println (row);
        blink ();
      }
    }

    digitalWrite (colPins[column], HIGH);
  }

  return key;
}

// -------------------------------------
void blink ()
{
  for (int i = 0; i < 5; i++)
  {
    digitalWrite (LED_BUILTIN, HIGH);
    delay (50);

    digitalWrite (LED_BUILTIN, LOW);
    delay (50);
  }
}
