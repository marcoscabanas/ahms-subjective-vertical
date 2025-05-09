import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim

duration   = 50     # sec
dt         = 0.01   # sec
t          = np.arange(0, duration, dt)

frequency  = 0.1     # 0.1 or 5.0 rad/sec
amplitude_g = 1.0   # in Gs (1G = 9.81 m/s**2)

stim_start, stim_end = 1.0, 35.0

# Otolith TF
K_oto, tau_n = 3.4, 1.0             # from slides
tau_1_oto, tau_2_oto = 0.5, 0.016   # from slides

def otolith_tf(signal_g):
    num = [K_oto, K_oto * tau_n]
    den = np.convolve([tau_1_oto, 1], [tau_2_oto, 1])
    return (lsim(lti(num, den), signal_g, t)[1]) / K_oto

# SV LPF
tau_sv = 5.0    # sec
lpf = lambda x, tau: lsim(lti([1], [tau, 1]), x, t)[1]

# --- ACTUAL SIMULATION ---
def windowed_sine(t, start, end, omega, A): # note: I wrote this to define start and end times of the actual sine function so that I can plot what happens BEFORE and AFTER the sine stops
    sig = np.zeros_like(t)
    mask = (t >= start) & (t <= end)
    sinetime = t[mask] - start
    sig[mask] = A * np.sin(omega * sinetime)
    return sig

f_x_in = windowed_sine(t, stim_start, stim_end, frequency, amplitude_g) # since this is where the sine acts
f_y_in = np.zeros_like(t)                                               # 0 since no sine acts
f_z_in = np.ones_like(t)                                                # 1 since only gravity is felt

omega_x_in = omega_y_in = omega_z_in = np.zeros_like(t) # no rotation in this translation case

f_x_neural = otolith_tf(f_x_in)
SV_x = lpf(f_x_neural, tau_sv)
SV_y = np.zeros_like(t)
SV_z = np.ones_like(t)

# --- PLOTTING ---
fig, ax = plt.subplots(3, 1, figsize=(13, 9), sharex=False)

# Specific-force INPUT
ax[0].plot(t, f_x_in, label=r'$f_x$ (input)', color='tab:blue')
ax[0].plot(t, f_y_in, label=r'$f_y$',         color='tab:green')
ax[0].plot(t, f_z_in, label=r'$f_z$',         color='tab:red')
ax[0].set_title('Specific Force (sensor input)'); ax[0].set_ylabel('[g]')
ax[0].set_xlabel('Time [s]'); ax[0].legend(); ax[0].grid(True)

# Angular-velocity INPUT
ax[1].plot(t, omega_x_in, label=r'$\omega_x$', color='tab:blue')
ax[1].plot(t, omega_y_in, label=r'$\omega_y$', color='tab:green')
ax[1].plot(t, omega_z_in, label=r'$\omega_z$', color='tab:red')
ax[1].set_title('Angular Velocity (sensor input)'); ax[1].set_ylabel('[deg s⁻¹]')
ax[1].set_xlabel('Time [s]'); ax[1].legend(); ax[1].grid(True)

# Subjective-vertical OUTPUT
ax[2].plot(t, SV_x, label=r'$SV_x$', color='tab:blue')
ax[2].plot(t, SV_y, label=r'$SV_y$', color='tab:green')
ax[2].plot(t, SV_z, label=r'$SV_z$', color='tab:red')
ax[2].set_title('Subjective Vertical (perceived)'); ax[2].set_ylabel('[g]')
ax[2].set_xlabel('Time [s]'); ax[2].legend(); ax[2].grid(True)

plt.tight_layout(); plt.show()
