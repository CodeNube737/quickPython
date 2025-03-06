// main.c (lab 6)
//assumes system clock is at 48 MHz
//input dividers on Timer A = div 1, input to Timer A = 48 MHz
//Divide by 512 -> PWM frequency = 93.75 kHz
//////////////////////////////////////////////////////////////////
#include "msp.h"
#include "coeffs1.h"

#define SMCLK       BIT0        // Port 7.0
#define A8_IN       BIT5        // Port 4.5 ADC input channel 8

#define PWM_PERIOD  512         // 9-bit DAC (2^9 = 512)
#define ADCSCALE    5           // 14-bit ADC; reduce by 5 bits to match DAC

#define SR_12kHz    4096
#define FSAMP       SR_12kHz    // Sampling frequency

// Buffer to store input samples for convolution
volatile float inputBuffer[N] = {0.0f};
volatile unsigned int bufferIndex = 0;

void main(void) {
    volatile unsigned int ADC_In = 0;
    volatile float Filtered_Output = 0.0f;

    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD; // Stop watchdog timer

    P6->DIR |= BIT0;        // Sampling flag P6.0
    P6->OUT = 0;

    P5->DIR |= BIT6;        // PWM output P5.6
    P5->SEL0 |= BIT6;
    P5->SEL1 &= ~BIT6;

    P4->SEL0 |= A8_IN;      // Use analog input #8 = P4.5 for ADC input
    P4->SEL1 |= A8_IN;

    ADC14->CTL0 &= ~ADC14_CTL0_ENC;
    ADC14->CTL0 = ADC14_CTL0_SHP | ADC14_CTL0_SSEL__SMCLK | ADC14_CTL0_DIV__4
                | ADC14_CTL0_SHT0__16 | ADC14_CTL0_ON;
    ADC14->MCTL[0] = 8u;

    TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | TIMER_A_CTL_ID__1 | TIMER_A_CTL_MC__CONTINUOUS;
    TIMER_A0->CCR[0] = FSAMP - 1;
    TIMER_A0->CCTL[0] = TIMER_A_CCTLN_CCIE;

    TIMER_A2->CTL = TIMER_A_CTL_SSEL__SMCLK | TIMER_A_CTL_ID__1 | TIMER_A_CTL_MC__UP;
    TIMER_A2->CCR[0] = PWM_PERIOD - 1;
    TIMER_A2->CCR[1] = PWM_PERIOD / 2;
    TIMER_A2->CCTL[1] = TIMER_A_CCTLN_OUTMOD_7;

    NVIC_EnableIRQ(TA0_0_IRQn);
    __enable_interrupts();

    // Main loop implementing FIR filter using discrete-time convolution
    while (1) {
        if ((ADC14->IFGR0 & ADC14_IFGR0_IFG0) != 0) {
            P6->OUT = 0x00;
            ADC_In = ((ADC14->MEM[0]) >> ADCSCALE);

            // Update input buffer with the new sample
            inputBuffer[bufferIndex] = (float)ADC_In;

            // Perform convolution
            float acc = 0.0f;
            int index = bufferIndex;
            int i;
            for (i = 0; i < N; i++) {
                acc += inputBuffer[index] * h[i];
                if (index == 0) {
                    index = N - 1;
                } else {
                    index--;
                }
            }

            // Obtain the filtered output
            Filtered_Output = acc;

            // Update buffer index
            bufferIndex++;
            if (bufferIndex >= N) {
                bufferIndex = 0;
            }

            // Update PWM duty cycle with filtered value
            TIMER_A2->CCR[0] = 0;
            TIMER_A2->CCR[1] = (unsigned int)Filtered_Output;
            TIMER_A2->CCR[0] = PWM_PERIOD - 1;
        }
    }
}

void TA0_0_IRQHandler(void) {
    TIMER_A0->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;
    TIMER_A0->CCR[0] += FSAMP;
    P6->OUT = 0x01;
    ADC14->CTL0 |= ADC14_CTL0_ENC | ADC14_CTL0_SC;
}
