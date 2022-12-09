# ece434HW 
> for the ECE434 homework

## 1. HW1: Etch-a-sketch
- Status: done 
- Up - 'w'; Down - 's'; Left - 'a'; Right - 'd'; Clear - 'c'; Exit - esc

## 2. HW2: gpio speed
1. What's the min and max voltage?
    3.362V, -118mV
2. What period and frequency is it?
    246ms , 4.043kHz
3. How close is it to 200ms?
    It is off by 50ms.
4. Why do they differ?
    Because Bash cannot run code very fast. 
5. Run htop and see how much processor you are using.
  30% to 40%
6. Try different values for the sleep time (2nd argument). What's the shortest period you can get? Make a table of the fastest values you try and the corresponding period and processor usage. Try using markdown tables: https://www.markdownguide.org/extended-syntax/#tables

  | Syntax      | Description |
  | ----------- | ----------- |
  | Header      | Title       |
  | Paragraph   | Text        |
7. How stable is the period?

8. Try launching something like vi. How stable is the period?

9. Try cleaning up togglegpio.sh and removing unneeded lines. Does it impact the period?

10. Togglegpio.sh uses bash (first line in file). Try using sh. Is the period shorter?

11. What's the shortest period you can get?
