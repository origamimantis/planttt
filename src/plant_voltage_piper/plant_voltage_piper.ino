void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
}

int g = 0;
int x = 0;

void loop() {
  // put your main code here, to run repeatedly:
  // wait for python reader to send a start signal, no need to read it

  g = analogRead(A0)*5/1024;
  x = analogRead(A1)*5/1024;
  Serial.println(String(x-g) + " " + String(millis()));
  delay(50);
}
