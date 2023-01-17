# Homework 05
1. EBC_make exercises done  
  Target = app.o  
  Dependency = app.c  
  Command = gcc  
2. A new kernel installed:  
  debian@BeagleBone:~$ uname -a  
  Linux BeagleBone 5.10.145-ti-rt-r55 #1xross SMP PREEMPT_RT Tue Dec 27 23:33:13 EST 2022 armv7l GNU/Linux
3. Run the examples hello, ebbchar (not ebbcharmutex), gpio_test, (not button) and led
4. gpio/gpio_test: copy P9_16 to P9_15 triggered on both falling and rising edges.
5. gpio2/gpio_test: use P9_16 to control P9_15; use P9_23 to control P9_12
6. When the new adxl345 is added, some files are generated in iio:device1, including the raw data, calibration, sample rate and so on 
7. Etch-a-sketch is controlled by IMU readings.
8. LED/LED.c toggles P9_12 and P9_15 at 1Hz and 2Hz.   
