#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <uRTCLib.h>
#include <SPI.h>
#include <SD.h>


#define HeaterRelayOutPin 13
#define ONE_WIRE_BUS 12

LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address 0x27, 16 column and 2 rows
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
uRTCLib rtc(0x68);
File myFile;


// Variables definition
float sum_of_temperatures = 0;
float mean_temp = 0;
int i = 0;
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
int numberOfDevices;
const int chipSelect = 10;
DeviceAddress tempDeviceAddress;


void setup(void) {
  Serial.begin(9600);
  SD.begin(chipSelect);

  pinMode(HeaterRelayOutPin, OUTPUT);
  sensors.begin();
  URTCLIB_WIRE.begin();
  numberOfDevices = sensors.getDeviceCount();
  
  // Following line sets the RTC with an explicit date & time
  // for example to set January 13 2022 at 12:56 you would call:
  // rtc.set(0, 45, 11, 4, 3, 7, 24);
  // rtc.set(second, minute, hour, dayOfWeek, dayOfMonth, month, year)
  // set day of week (1=Sunday, 7=Saturday)

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("MICROALGAE");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  delay(200);

  myFile=SD.open("DATA.txt", FILE_WRITE);

  // if the file opened ok, write to it:
  if (myFile) {
    Serial.println("File opened ok");
    // print the headings for our data
    myFile.println("Year Month Day Hour Minute Second Ambient-temp Temperature-T1 Temperature-T2 Temperature-T3 Mean-temp");
  }
  myFile.close();
}

void loop() {
  sensors.requestTemperatures();
  rtc.refresh();

  loggingTime();
  myFile = SD.open("DATA.txt", FILE_WRITE);

  for(i=0;i<numberOfDevices; i++) {
      // Search the wire for address
      if(sensors.getAddress(tempDeviceAddress, i)){
      
      /*
      // Output the device ID
      Serial.print("Temperature for device ");
      Serial.print(i,DEC);
      */
      lcd.setCursor(0, 0);
      lcd.print("T");
      lcd.print(i,DEC);
      lcd.print(": ");

      // Print the data
      float temp_C = sensors.getTempC(tempDeviceAddress);
      sum_of_temperatures += temp_C;

      if (myFile) {
        myFile.print(temp_C);
        myFile.print(" ");
      }

      /*
      Serial.print(": ");
      Serial.println(temp_C);
      */
      lcd.print(temp_C);
      lcd.print(" C");
      delay(3000);
      lcd.clear();
      }
    }
  mean_temp = sum_of_temperatures/i;
  myFile.println(mean_temp);
  myFile.close();

  if (mean_temp <= 30) {
    digitalWrite(HeaterRelayOutPin, HIGH);
  }
  else {
    digitalWrite(HeaterRelayOutPin, LOW);
  }

  /*
  Serial.print("Mean temperature of the box: ");
  Serial.println(mean_temp);
  Serial.println("");
  */
  lcd.setCursor(0, 0); 
  lcd.print("Mean temperature");
  lcd.setCursor(0, 1);
  lcd.print(mean_temp);
  lcd.print(" C");
  
  delay(3000);
  lcd.clear();

  sum_of_temperatures = 0;

  /*
  Serial.print("Current Date & Time: ");
  Serial.print(rtc.year());
  Serial.print('/');
  Serial.print(rtc.month());
  Serial.print('/');
  Serial.print(rtc.day());

  Serial.print(" (");
  Serial.print(daysOfTheWeek[rtc.dayOfWeek()-1]);
  Serial.print(") ");

  Serial.print(rtc.hour());
  Serial.print(':');
  Serial.print(rtc.minute());
  Serial.print(':');
  Serial.println(rtc.second());
  */
}

void loggingTime() {
  myFile = SD.open("DATA.txt", FILE_WRITE);
  if (myFile) {
    myFile.print(rtc.year());
    myFile.print(' ');
    myFile.print(rtc.month());
    myFile.print(' ');
    myFile.print(rtc.day());
    myFile.print(' ');
    myFile.print(rtc.hour());
    myFile.print(' ');
    myFile.print(rtc.minute());
    myFile.print(' ');
    myFile.print(rtc.second());
    myFile.print(' ');
  }
  myFile.close();
}