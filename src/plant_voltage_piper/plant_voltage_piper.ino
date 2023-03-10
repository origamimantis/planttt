void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
}

int x = 0;

void loop() {
  // put your main code here, to run repeatedly:
  // wait for python reader to send a start signal, no need to read it

  x = analogRead(A0);
  Serial.println(String(x) + " " + String(millis()));
  delay(50);
}
