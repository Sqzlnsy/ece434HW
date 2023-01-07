// Jason Su @ 01/07/2023
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr1, *gpio_addr0;
    volatile unsigned int *gpio_oe_addr;
    volatile unsigned int *gpio_dataout_addr1, *gpio_dataout_addr0;
    volatile unsigned int *gpio_datain_addr1, *gpio_datain_addr0;
    unsigned int reg;
    
    // Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, GPIO1_SIZE);
    gpio_addr1 = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);
    printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, GPIO0_SIZE);
    gpio_addr0 = mmap(0, GPIO0_SIZE, PROT_READ, MAP_SHARED, fd, GPIO0_START_ADDR);

    gpio_oe_addr          = gpio_addr1 + GPIO_OE;
    gpio_dataout_addr1 = gpio_addr1 + GPIO_DATAOUT;
    gpio_datain_addr1     = gpio_addr1 + GPIO_DATAIN;

    if((gpio_addr1 == MAP_FAILED)) {
        printf("Unable to map GPIO1\n");
        exit(1);
    }
    if((gpio_addr0 == MAP_FAILED)) {
        printf("Unable to map GPIO0\n");
        exit(1);
    }
    printf("GPIO0 mapped to %p\n", gpio_addr0);
    printf("GPIO1 mapped to %p\n", gpio_addr1);

    // Set USR2 and USR3 to be an output pin
    reg = *gpio_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~(USR3 | USR2);       // Set USR3 bit to 0
    reg |= (1<<16);              // Set GPIO48 bit to 1
    *gpio_oe_addr = reg;
    printf("GPIO1 configuration: %X\n", reg);

    gpio_dataout_addr0 = gpio_addr0 + GPIO_DATAOUT;
    gpio_datain_addr0     = gpio_addr0 + GPIO_DATAIN;
    gpio_oe_addr          = gpio_addr0 + GPIO_OE;
    reg = *gpio_oe_addr;
    printf("GPIO0 configuration: %X\n", reg);
    reg |= (1<<20);              // Set GPIO20 bit to 1
    //*gpio_oe_addr = reg;
    printf("GPIO0 configuration: %X\n", reg);

    while (keepgoing){
        usleep(250000);
        reg = *gpio_datain_addr0;
        reg &= (1<<20);
        printf("USR2:");
        if (reg!=0){
            reg = *gpio_dataout_addr1;
            reg = reg | USR2;
            printf("on  |   ");
        } else {
            reg = *gpio_dataout_addr1;
            reg &= ~USR2;
            printf("off  |   ");
        }
        *gpio_dataout_addr1=reg;

        reg = *gpio_datain_addr1;
        reg &= (1<<16);
        printf("USR3:");
        if (reg!=0){
            reg = *gpio_dataout_addr1;
            reg = reg | USR3;
            printf("on\r");
        } else {
            reg = *gpio_dataout_addr1;
            reg &= ~USR3;
            printf("off\r");
        }
        *gpio_dataout_addr1=reg;
    };
    munmap((void *)gpio_addr0, GPIO0_SIZE);
    munmap((void *)gpio_addr1, GPIO0_SIZE);
    close(fd);
    return 0;
}
