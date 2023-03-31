void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  // use the pullup resistor to avoid huge noise
  pinMode(A0,INPUT_PULLUP);
}

int x = 0;

float sum = 0;
int lastupdate = 0;
int n = 0;

void loop() {

  // read
  x = analogRead(A0);

  // add to the current cycle's average and track number of samples
  sum += x;
  n += 1;

  // check if enough time has passed since the previous serial update
  int now = millis();
  if (now - lastupdate > 50)
  {
    // calculate the average input reading
    float avg = sum/n;
    Serial.println(String(avg) + " " + String(now));

    // reset cycle-tracking vars
    lastupdate=now;
    sum = 0;
    n = 0;
  }

}
