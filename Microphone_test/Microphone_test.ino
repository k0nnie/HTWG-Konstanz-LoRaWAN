const int soundPin = A1;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // int value = analogRead(soundPin);
  int value = analogRead (soundPin) * (5.0 / 1023.0);
  // Serial.println(value);
  if (value != 0) {
    Serial.print ("Analog voltage value:");
    Serial.print (value, 4);
    Serial.print ("\n");
  }

  delay(20);
}
