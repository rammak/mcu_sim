String incomingString;
int i = 0;

void setup() {
  Serial.begin(57600);

}

void loop() {
  if(Serial.available()) {
    char c = Serial.read();
    if(c != '\n' && i < 100) {
      incomingString += c;
      i++;
    }
    else {
      if(incomingString == "{\"all\":\"read\"}") {
        Serial.write("{\"all\":[-0.48259,-0.56391,-0.98551,0.56293,0.48357,0.98257,0.29332,0.37954,0.92604,-0.54434,-0.01072,"
        "0.31305,-0.68770,-0.77000,-0.13826,0.15290,-0.38267,0.47080,-3.4322e-05,-5.8005e-06,-2.3457e-05,-2.43017,-0.95357,0.61203,"
        "0.11364,0.08323,0.10061]}\n");
      }
      i = 0;
      incomingString.remove(0);
//      Serial.print(incomingString);
    }
  }

}
