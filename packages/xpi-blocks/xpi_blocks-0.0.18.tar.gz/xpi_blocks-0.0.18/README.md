# xPI.blocks

Library to work with sensors and peripheral devices from Raspberry PI (Orange PI) using Python


Supported sensors: 

1. checked BH1750 - light sensor (I2C)
2. BMP085/180 - temperature and pressure sensor (I2C)
3. ok OPT3001 - light sensor (most sensitive, complicated to configure) (I2C) 
4. checked MCP23017 - GPIO chip, 16 multiplexed inputs/outputs (I2C)
5. checked ADS1115 - ADC chip, 4 channels (I2C)
6. checked SHD20/HTU21D - temperature and humidity sensor (I2C)
7. checked PCA9685 - PWM Driver (servo, led) (I2C)
8. checked MAX17040G - Battery chip (voltage, capacity) (I2C)
9. ok BME280 - temperature, humidity and pressure sensor (I2C)
10. TCS34725 - RGB light sensor (I2C)
11. AT24Cxxx - memory chip (I2C) 
12. checked except thermostat LM75A - temperature sensor + thermostat (I2C)
13. SSD1306 - oled driver (I2C)
14. checked PCF8574 - GPIO chip, 8 intputs/outputs (I2C)
15. checked MCP410xx (MCP41010, MCP41050, etc) - Digital potentiometer (SPI)
16. checked X9Cxxx (x9c102, x9c103, x9c104, x9c503) - Digital potentiometer (GPIO) 
17. checked TB6612FNG - motor driver, 2 channel, independent pwm (GPIO)
18. checked DRV8833 - motor driver, 2 channel, dependent pwm (GPIO)
19. ok VNH2SP30 - powerful motor driver, 1 channel (GPIO)
20. checked ok ACS712 current sensor (along with ADS1115) 
21. checked - Voltage divider (along with ADS1115) 
22. checked - TEMT6000 light sensor (along with ADS1115) 
23. checked - GUVA-S12 UV sensor (along with ADS1115) 
24. checked - ML8511 UV sensor (along with ADS1115) 
25. Soil moisture sensor (along with ADS1115) 
26. Noise level sensor (based on microphone with ADS1115) 
27. Vibration sensor (along with ADS1115) 
28. BMI160 - IMU, 6 DOF 
29. BMX055 - IMU, 9 DOF
30. MPU6050 - IMU, 6 DOF
31. MPU9250 - IMU, 9 DOF 
32. MAX44009 - light sensor 
33. TSL2561 - light sensor
34. VEML6070 - UV sensor
35. HC-SR501, MH-SR602, AM312 - PIR sensor (GPIO)
36. Relay Module   (GPIO)
37. ok Unipolar Stepper motor via ULN2003 driver (GPIO)
38. Bipolar Stepper motor driver via L293 or L298 (GPIO)
39. ok 74HC595 (HC595) - Shift register (serial to parallel) (GPIO)
40. ok 74HC165 (HC165) - Shift register (parallel to serial)  (GPIO)
41. checked DS1307 - RTC clock (I2C) 
42. checked DS3231N - RTC clock (I2C)
43. ok - DS1302 - RTC chip (GPIO)


TODO: 
1. ok L9110H - motor driver, 1 channel (GPIO)
2. L9110H + MCP21017 - GPIO extender + motor driver (I2C)
3. HDC1080 (CCS811) - CO gas sensor 
4. MICS-6814 - CO NO2 NH3 gas sensor
5. DSM501A - PM2.5 sensor 
6. DHT22 (DHT11) - humidity and temperature sensor
7. W25Qxx - memory chip (SPI)
8. HW-MS03 - radar sensor module (human sensor)
9. NAP07 HIS07 - smoke sensor
10. JSN-SR04T - ultrasonic sensor (distance)
11. DS18B20 - temperature sensor (1-wire)
12. TCS3200 (GY-31) - color sensor
13. MAX30102 - heartrate sensor 
14. checked HC-SR04 (HCSR04) - distance sensor, also suitable with US-015 (GPIO)
15. HX711 (cell weight sensor) - digital load sensor 
16. HR-202 - humidity sensor 
17. SGP30 - CO2 sensor
18. MQ-x - various gas sensor (along with ads1115, I2C)
19. BME-680 - temperature, humidity, pressure sensor
20. ZP-16 - gas sensor
21. WS2812 - addressable & stackable RGB led (GPIO)
22. APDS-9960 - gesture sensor (I2C)
23. Vl53L1X - distance laser sensor
24. TOF10120(TOF05140) - distance laser sensor (UART/I2C)
25. FPM10A - fingerprint sensor  (UART)
26. BF350 - load cell/strain gauge 
27. HW-526 - rotation sensor
28. MAX471 - current sensor (along with ads1115, I2C)
29. KY-013 - thermistor/analog temperature sensor (along with ads1115, I2C)
30. TGS2600 - air quality PM10 sensor
31. L298D/L298P - powerful motor driver (2 motors) with integrated circuit sensor. 


# Installation: 

1. download or clone this repository
2. go to its folder 
3. type 'pip3 install -e .'
4. now you can use import modules from this library to any of your projects

