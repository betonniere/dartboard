const byte numRows      = 8;
const byte numCols      = 10;
const int  debounceTime = 100; //  20 works better than great !

char keymap[numRows][numCols] = {
  {'0','1','2','4','5','6','7','8','9','*'},
  {'a','b','c','d','e','f','g','h','i','?'},
  {'j','k','l','m','n','o','p','q','r','&'},
  {'s','t','u','v','w','x','y','z','A','@'},
  {'B','C','D','E','F','G','H','I','J','}'},
  {'K','L','M','N','O','P','Q','R','S',')'},
  {'T','U','V','W','X','Y','Z','+','-',']'},
  {'/','!','$','#','(','=','[','_','<','>'}
};

byte rowPins[numRows] = {A0, A1, A2, A3, A4, A5, 2, 3};
byte colPins[numCols] = {13, 12, 11, 10,  9,  8 ,7, 6, 5, 4};

void setup ()
{
  Serial.begin (9600);

  for (int row = 0; row < numRows; row++)
  {
    pinMode      (rowPins[row], INPUT);
    digitalWrite (rowPins[row], HIGH);
  }

  for (int column = 0; column < numCols; column++)
  {
    pinMode      (colPins[column], OUTPUT);
    digitalWrite (colPins[column], HIGH);
  }
}

void loop ()
{
  char key = getKey ();

  if (key != 0)
  {
    Serial.println (key);
  }
}

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
        d  elay (debounceTime);
        while (digitalRead (rowPins[row]) == LOW)
        {
          // wait for key to be released
        }
        key = keymap[row][column];
      }
    }

    digitalWrite (colPins[column], HIGH);
  }

  return key;
}

