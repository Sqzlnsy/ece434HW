# Homework 08
### 2.6
1. What make command will start your PRU code running?  
make TARGET= 'program' start  
2. What will stop it?  
make TARGET= 'program' stop 
3. How fast can you toggle the pin? Is there jitter1? Is it stable?  
It toggles at 12.48Mhz. It is jitter with many ripples. Not very stable, the freqency fluctuates around 12.4 to 12.5 Mhz.  
### 5.3
4. how stable the waveform is. What’s the Std Dev? Is there jitter?  
It is stable and the Std Dev is about 115kHz. It looks like sine wave.  
![alt text](MicrosoftTeams-image%20(13).png?raw=true "Title")
### 5.4
5. What output pins are being driven?
P9.31, P9.30, P9.29, P9.28  
6. What’s the highest frequency you can get with four channels?  
The highest freqency is 327kHz, and there is no jitter. 
### 5.9
5. how fast the code can transfer the input to the output?  
25.5ns
![alt text](MicrosoftTeams-image%20(14).png?raw=true "Title")
### 5.10


