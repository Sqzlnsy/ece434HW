# 2. HW2: gpio speed
1. What's the min and max voltage?  
    3.362V, -118mV
2. What period and frequency is it?  
    246ms , 4.043kHz
3. How close is it to 200ms?  
    It is off by 50ms.
4. Why do they differ?  
    Because Bash cannot run code very fast. 
5. Run htop and see how much processor you are using.  
    3%
6. Try different values for the sleep time (2nd argument). What's the shortest period you can get? Make a table of the fastest values you try and the corresponding period and processor usage. Try using markdown tables: https://www.markdownguide.org/extended-syntax/#tables  

  | Period      | Processor usage | Sleep Time
  | ----------- | ----------- | ----------- |
  | 250        | 3%       | 100
  | 150        | 6%       | 50
  | 70        | 12%       | 10
  | 60          | 14.5%    | 5
  | 50         | 17%       | 0
7. How stable is the period?  
    It is not very stable, for 150ms period, the stdev. is around 20ms. 
8. Try launching something like vi. How stable is the period?  
    It is getting worse. 
9. Try cleaning up togglegpio.sh and removing unneeded lines. Does it impact the period?  
    The period becomes 243 ms, which is a 7ms better than
10. Togglegpio.sh uses bash (first line in file). Try using sh. Is the period shorter?  
    It becomes better, because the period is 20ms lower than bash run at 100ms sleep time.
11. What's the shortest period you can get?  
    30ms using sh
> Comparison  

 |              | Shell       | Python | C          | C w/o usleep | Python gpiod | C gpiod| 
  | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
  | Frequency | 20Hz          | 15kHz       | 5.3kHz      | 100kHz      | 56kHz      | 260kHz
  | CPU usage | 18%           | 97%         | 59%         | 98%         | 97%         | 97%

## ssh port changed to 2022 and fail2ban enabled

## Programs
1. etch-and-sketch.py  
    Up "P8_15"; Down "P8_12"; Right "P8_16"; Left "P8_26"
2. getsetEvent.py  
    
3. togglegpio.py    toggle P9_12


# hw02 grading

| Points      | Description |
| ----------- | ----------- |
|  2/2 | Buttons and LEDs 
|  8/8 | Etch-a-Sketch works
|      | Measuring a gpio pin on an Oscilloscope 
|  2/2 | Questions answered
|  4/4 | Table complete
|  2/2 | gpiod
|      | Security
|  0/1 | ssh port 
|  0/1 | fail2ban
| 18/20   | **Total**

Looks good, but ssh port change and fail2ban are missiing.
