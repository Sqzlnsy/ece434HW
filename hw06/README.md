# hw06
1. Where does Julia Cartwright work?  
  National Instrument  
2. What is PREEMT_RT? Hint: Google it.  
  PREEMPT-RT is the real-time kernel patch, which makes interrupt run as threads.    
3. What is mixed criticality?   
  Some time sensitive processes and some non time sensitive processes need to run together and communicate with each other. 
4. How can drivers misbehave?  
  Since real-time processes and non time sensitve processes share the same driver stack, misbehaving drivers in the non-time sensitve may affects real-time processes.   
5. What is Δ in Figure 1?   
  The time between when the event happens and the corresponding service is excuted.    
6. What is Cyclictest[2]?  
  Cyclictest accurately and repeatedly measures the difference between a thread's intended wake-up time and the time at which it actually wakes up in order to provide statistics about the system's latencies.  
7. What is plotted in Figure 2?  
  The delta measured on a linux system (purple) and the delat measured on a linux system with PREMMT_RT(green) using the same hardware. 
8. What is dispatch latency? Scheduling latency?   
  Dispatch latency is the time between hardware firing an interrupt and the thread woken up. Scheduling latency is the time between the scheduler aware of this high priority task and the CPU actually excutes the task  
9. What is mainline?  
  It captures how cpu swicthing from one threads to another. 
10. What is keeping the External event in Figure 3 from starting?  
  Because it doesn't get handled until the current excuting irq is done. 
11. Why can the External event in Figure 4 start sooner?  
  Because very few codes run in the hardirq, the external event thread can be woken up as long as the small portion of code is done. 
  
## RT vs non-RT
### Without load
![plot](./cyclictest.png)  
### With load
![plot](./cyclictestLoad.png)  
RT has a bounded latency of around 150us, and the difference are more obvious when there are other things running. I run the extended Kalman filte code processing simulated data as load when generating the histogram.


# hw06 grading

| Points      | Description | |
| ----------- | ----------- |-|
|  2/2 | Project | *Telemetry for Vehicles*
|  4/5 | Questions | *Mainline is the main kernel tree.*
|  4/4 | PREEMPT_RT
|  2/2 | Plots to 500 us
|  5/5 | Plots - Heavy/Light load
|  2/2 | Extras
| 19/20 | **Total**