# SUBJECTIVE VERTICAL: ASSIGNMENT
Assignment on the perception of the subjective vertical based on otolith &amp; semi-circular canal inputs (NO visual inputs) - low and high frequency cases.

## ASSIGNMENT GIVEN INSTRUCTIONS
1. Write a Python script to simulate how the subjective vertical changes.
2. No visual cues can be taken into account (ie: no visual attractor model).
3. Only use the subjective vertical model, as defined in the slides.
4. Two cases must be generated: One for low-frequency components @ 0.1 rad/sec., one for high-frequency components @ 5 rad/sec.

## EXPLANATION OF SCRIPTS

### 1. x_movement.py
This script simulates the above-mentioned things for a case in which only translation movement about the x-axis happens. Line 9 of the code allows changing the frequency (so 0.1 or 5).
The amplitude is set at 1.0g, meaning that over the period of the signal, the maximum amplitude reached will be 1.0g of specific force.
The simulation starts at second 1, and ends at second 35. The total simulation time is 50 seconds. I did this on purpose such that we can observe how the subjective vertical before, during, and after having added in the oscillation.
The parameters of the otolith transfer function and of the subjective vertical low-pass filter are taken directly from the slides.
In both of these cases, since the movement is only translational (and not rotational), the semi-circular canals do not play a role - only the otoliths.

Overall, we can observe that at a frequency of 5 rad/sec, there are many oscillations in the subjective vertical x-component, but their magnitude remains very small, so the overall contribution of the forward/backward movement is very small. There is also still a 1.0g subjective vertical z-component, since gravity is always acting in the same direction with respect to the human.

In the case of 0.1 rad/sec, there is not even one entire oscillation, but the magnitude is significantly higher now. This in turn means that the forward-backward movement may now be interpreted as a tilt!
