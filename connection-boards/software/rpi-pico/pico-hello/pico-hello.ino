void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial1.begin(115200);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial1.println ("15X1");
  delay(1000);

  digitalWrite(LED_BUILTIN, LOW);
  Serial1.println ("18X1");
  delay(1000);
}
