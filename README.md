# SUBJECTIVE VERTICAL: ASSIGNMENT
Assignment on the perception of the subjective vertical based on otolith &amp; semi-circular canal inputs (NO visual inputs) - low and high frequency cases.

## ASSIGNMENT GIVEN INSTRUCTIONS
1. Write a Python script to simulate how the subjective vertical changes.
2. No visual cues can be taken into account (ie: no visual attractor model).
3. Only use the subjective vertical model, as defined in the slides.
4. Two cases must be generated: One for low-frequency components @ 0.1 rad/sec., one for high-frequency components @ 5 rad/sec.

## PLOTTING
I tried to plot everything as is shown in the lecture slides: Two input graphs (specific force in Gs, angular velocity in degrees/sec), and one output graph (subjective vertical in Gs). I know that the semi-circular canals are sensitive to rotational ACCELERATION, but for clarity's sake I wanted to graph the rotational VELOCITY about each component - exactly like the slides in the lectures show.

There are four graphs in total (each made of three subgraphs as explained above). Two graphs depict linear movement about the x-axis for the two different cases (0.1 rad/sec, 5 rad/sec) and two graphs depict tilt movement about the y-axis for the two different cases. In the case of tilt, I chose a maximum tilt angle of 10 degrees, but this can be adjusted in the script if you would like to check smaller or greater tilts.

## EXPLANATION OF SCRIPTS

### 1. translational_movement.py
This script simulates the above-mentioned things for a case in which only translation movement about the x-axis happens. Line 9 of the code allows changing the frequency (so 0.1 or 5).
The amplitude is set at 1.0g, meaning that over the period of the signal, the maximum amplitude reached will be 1.0g of specific force.
The simulation starts at second 1, and ends at second 35. The total simulation time is 50 seconds. I did this on purpose such that we can observe how the subjective vertical before, during, and after having added in the oscillation.
The parameters of the otolith transfer function and of the subjective vertical low-pass filter are taken directly from the slides.
In both of these cases, since the movement is only translational (and not rotational), the semi-circular canals do not play a role - only the otoliths.

Overall, we can observe that at a frequency of 5 rad/sec, there are many oscillations in the subjective vertical x-component, but their magnitude remains very small, so the overall contribution of the forward/backward movement is very small. There is also still a 1.0g subjective vertical z-component, since gravity is always acting in the same direction with respect to the human.

In the case of 0.1 rad/sec, there is not even one entire oscillation, but the magnitude is significantly higher now. This in turn means that the forward-backward movement may now be interpreted as a tilt!

### 2. tilt_movement.py
This script simulates the above-mentionedthings for a case in which only tilt movement about the y-axis happens (so similar to pitching up and down). Line 14 of the code allows changing the frequency (so 0.1 or 5).
A big thing to note here is that when I wrote the script, I could NOT get the subjective vertical z-component to start out at 1g (which is expected since the tilt is 0 degrees at the start of the simulation: This is because the otolith TF and the SV LPF both start with a zero internal state. To work around this, I added what I called a "warmup" which is essentially a constant 1.0g input for a small amount of time (I chose 25 seconds) such that the internal state of the z-component can go up to 1.0g, so that when we start the simulation the z-component is directly plotted at 1.0g. It's a bit of a weird workaround but it's the only way I could get the physics of the system to match up with what we expect in real life. After that the simulation proceeds as normal, with the 10 degree tilt at the specified frequency.
Similar to the translation movement, the simulation starts at t=0 seconds, but the actual tilt starts at t=1 seconds, and ends at t=35 seconds. What is obvious (especially in the 0.1 rad/sec case) is that the tilting abruptly stops, but doesn't actually sway back to zero degrees: It just stops at whatever the tilt is at 35 seconds. The result of this that from second 35 onwards, the specific forces about the different axes don't go down to zero and one, but remain fixed at values. This is normal.

Overall, we can observe that at 5 rad/sec, there are oscillations in the specific force about the x and z axes. This is normal since when pitching, you’re literally rotating the gravity vector into and out of the x-axis. We observe that the high frequency of these oscillations results in a low magnitude of variations about both the x and z components. 

In the case of 0.1 rad/sec, there is not even one entire oscillation, but the magnitude of the specific forces has a larger variance across the x and z and components. Like stated above, when pitching you’re rotating the gravity vector into and out of the x-axis. This is why in the case of tilt as opposed to translation, the x and z components of the specific force vary at the same time. Overall, the contribution of a lower frequency components will influence the subjective vertical significantly more than the high-frequency components. Since the limits at this low frequency component are still above the threshold of the semi-circular canals (0.05 degrees/sec), these greatly contribute.
