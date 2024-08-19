#include <GyverEncoder.h>
#include <LiquidCrystal_I2C.h>
#include <GyverDS18Array.h>
#include <uRTCLib.h>
#include <SPI.h>
#include <SD.h>


char daysOfTheWeek[7][12] = { "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" };
byte chipSelect = 4;
byte flag = 0;
byte i = 0;
byte k = 0;
byte control_temperature = 20;

long period = 60;
unsigned long current_millis;
static unsigned long start_millis;

float current_temperature = 0;
float sum_of_temperatures = 0;
float mean_temp = 0;
float temp_array[4];
uint64_t addr[] = {
  0x090568540A646128,
  0xE5062194BA3D5328,
  0x3C062194A8BFA728,
  0x93062194E6939528,
};

#define heater_relay_Pin 11
#define CLK 5
#define DT 6
#define SW 7

Encoder enc1(CLK, DT, SW);
LiquidCrystal_I2C lcd(0x27, 16, 2);
GyverDS18Array ds(12, addr, 4);
uRTCLib rtc(0x68);
File myFile;

void setup() {
  ds.requestTemp();
  pinMode(heater_relay_Pin, OUTPUT);
  enc1.setType(TYPE2);
  SD.begin(chipSelect);
  URTCLIB_WIRE.begin();
  myFile = SD.open("DATA.txt", FILE_WRITE);

  start_millis = millis();
  current_millis = millis();

  // Following line sets the RTC with an explicit date & time
  // rtc.set(0, 39, 18, 5, 7, 8, 24);
  // rtc.set(second, minute, hour, dayOfWeek, dayOfMonth, month, year)
  // set day of week (1=Sunday, 7=Saturday)

  lcd.init();
  lcd.backlight();

  if (myFile) {
    myFile.println("Year Month Day Hour Minute Second Ambient-temp Temperature-T1 Temperature-T2 Temperature-T3");
    myFile.close();
  }

  lcd.setCursor(0, 0);
  lcd.print("Set control tem-:");
  lcd.setCursor(0, 1);
  lcd.print("perature: ");
  while (flag == 0) {
    enc1.tick();
    if (enc1.isRight()) {
      control_temperature++;
      lcd.setCursor(10, 1);
      lcd.print(control_temperature);
      lcd.print("     ");
    }
    if (enc1.isLeft()) {
      control_temperature--;
      lcd.setCursor(10, 1);
      lcd.print(control_temperature);
      lcd.print("     ");
    }
    if (enc1.isClick()) {
      flag = 1;
      lcd.clear();
    }
  }
}

void loop() {
  rtc.refresh();
  current_millis = millis();
  byte second, minute, hour, dayOfWeek, dayOfMonth, month, year;
  readDS1307time(&second, &minute, &hour, &dayOfWeek, &month, &year);

  if (current_millis - start_millis >= period * 1000) {
    start_millis = current_millis;
    if (ds.ready()) {
      for (i = 0; i < ds.amount(); i++) {
        if (ds.readTemp(i)) {
          current_temperature = ds.getTemp();
        }
        if (i >= 1) sum_of_temperatures += current_temperature;
        temp_array[i] = current_temperature;
      }
      loggingTime();
      myFile = SD.open("DATA.txt", FILE_WRITE);
      myFile.print(temp_array[0]);
      myFile.print(" ");
      myFile.print(temp_array[1]);
      myFile.print(" ");
      myFile.print(temp_array[2]);
      myFile.print(" ");
      myFile.print(temp_array[3]);
      myFile.println("");
      myFile.close();
    }
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(temp_array[0]);
    lcd.setCursor(8, 0);
    lcd.print(temp_array[1]);
    lcd.setCursor(0, 1);
    lcd.print(temp_array[2]);
    lcd.setCursor(8, 1);
    lcd.print(temp_array[3]);
    mean_temp = sum_of_temperatures / (i - 1);

    sum_of_temperatures = 0;
    ds.requestTemp();
  }

  if (enc1.isRightH()) {
    if (k > 3) {
      k = 0;
    }
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temperature:");
    lcd.setCursor(0, 1);
    lcd.print("T");
    lcd.print(k + 1);
    lcd.print(": ");
    lcd.print(temp_array[k]);
    lcd.print(" C");
    k++;
  } else if (enc1.isDouble()) {
    lcd.clear();
  }

  if (mean_temp < control_temperature) {
    digitalWrite(heater_relay_Pin, HIGH);
  } else {
    digitalWrite(heater_relay_Pin, LOW);
  }
}

void readDS1307time(byte *second,
                    byte *minute,
                    byte *hour,
                    byte *dayOfWeek,
                    byte *month,
                    byte *year) {
  *second = rtc.second();
  *minute = rtc.minute();
  *hour = rtc.hour();
  *dayOfWeek = rtc.day();
  *month = rtc.month();
  *year = rtc.year();
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