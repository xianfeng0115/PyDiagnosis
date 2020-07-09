String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
    digitalWrite(8, low);
  // reserve 200 bytes for the inputString:
  //inputString.reserve(200);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString);
    if (inputString.startsWith("open1")) {
      digitalWrite(8, LOW);
    } else if (inputString.startsWith("open2")) {
      digitalWrite(9, LOW);
    } else if (inputString.startsWith("open3")) {
      digitalWrite(10, LOW);
    } else if (inputString.startsWith("open4")) {
      digitalWrite(11, LOW);
    } else if (inputString.startsWith("close1")) {
      digitalWrite(8, HIGH);
    } else if (inputString.startsWith("close2")) {
      digitalWrite(9, HIGH);
    } else if (inputString.startsWith("close3")) {
      digitalWrite(10, HIGH);
    } else if (inputString.startsWith("close4")) {
      digitalWrite(11, HIGH);
    } else if (inputString.startsWith("getA0")) {
      int sensorValue = analogRead(A0);
      Serial.print("A0=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }else if (inputString.startsWith("getA1")) {
      int sensorValue = analogRead(A1);
      Serial.print("A1=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }else if (inputString.startsWith("getA2")) {
      int sensorValue = analogRead(A2);
      Serial.print("A2=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }else if (inputString.startsWith("getA3")) {
      int sensorValue = analogRead(A3);
      Serial.print("A3=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }else if (inputString.startsWith("getA4")) {
      int sensorValue = analogRead(A4);
      Serial.print("A4=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }else if (inputString.startsWith("getA5")) {
      int sensorValue = analogRead(A5);
      Serial.print("A5=");
      Serial.print(sensorValue);
      Serial.print("\n");
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
  hardware serial RX.  This routine is run between each
  time loop() runs, so using delay inside loop can delay
  response.  Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    //Serial.print(inChar);
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n' | inChar == '\r') {
      stringComplete = true;
    }
  }
}
