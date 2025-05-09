import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim

dt        = 0.01
warmup    = 25.0      # sec, necessary to ensure that the SV_z component starts at 1g
duration  = 50.0      # sec, experiment AFTER warmup
t_warm    = np.arange(0, warmup, dt)
t_exp     = np.arange(0, duration, dt)
pad_len   = t_warm.size

stim_start   = 1.0
stim_end     = 35.0
tilt_freq    = 5.0                    # rad/sec
tilt_amp_vel = np.deg2rad(10.0)     # how much tilt we want the person to experience

# Otolith TF params
K_oto      = 3.4
tau_n      = 1.0
tau1, tau2 = 0.5, 0.016

# SV-LPF time constant
tau_sv     = 5.0

def windowed_sine(t, start, end, omega, A):
    sig = np.zeros_like(t)
    mask = (t >= start) & (t <= end)
    sig[mask] = A * np.sin(omega * (t[mask] - start))
    return sig

# Otolith TF
def otolith_tf(signal, t):
    num = [K_oto, K_oto * tau_n]
    den = np.convolve([tau1, 1], [tau2, 1])
    _, y, _ = lsim(lti(num, den), signal, t)
    return y / K_oto

# SV LPF
def lpf(signal, t, tau):
    _, y, _ = lsim(lti([1], [tau, 1]), signal, t)
    return y


# --- ACTUAL SIMULATION ---
omega_y_exp = windowed_sine(t_exp, stim_start, stim_end, tilt_freq, tilt_amp_vel)
omega_x_exp = np.zeros_like(t_exp)
omega_z_exp = np.zeros_like(t_exp)

theta = np.cumsum(omega_y_exp) * dt

g_x_exp = np.sin(theta)
g_y_exp = np.zeros_like(theta)
g_z_exp = np.cos(theta)

f_x_exp = g_x_exp
f_y_exp = g_y_exp
f_z_exp = g_z_exp

# Setting the warmup
f_x_full = np.concatenate([np.zeros_like(t_warm),        f_x_exp])
f_y_full = np.concatenate([np.zeros_like(t_warm),        f_y_exp])
f_z_full = np.concatenate([np.ones_like(t_warm),         f_z_exp])
t_full   = np.arange(0, warmup + duration, dt)

f_x_neural = otolith_tf(f_x_full, t_full)
f_y_neural = otolith_tf(f_y_full, t_full)
f_z_neural = otolith_tf(f_z_full, t_full)

SV_x_full = lpf(f_x_neural, t_full, tau_sv)
SV_y_full = lpf(f_y_neural, t_full, tau_sv)
SV_z_full = lpf(f_z_neural, t_full, tau_sv)

# Get rid of the warmup so it doesn't show up in the graphs
SV_x = SV_x_full[pad_len:]
SV_y = SV_y_full[pad_len:]
SV_z = SV_z_full[pad_len:]
t    = t_exp

# --- PLOTTING ---
fig, ax = plt.subplots(3, 1, figsize=(13, 9))

# Specific-force INPUT
ax[0].plot(t, f_x_exp, label=r'$f_x$', color='tab:blue')
ax[0].plot(t, f_y_exp, label=r'$f_y$',         color='tab:green')
ax[0].plot(t, f_z_exp, label=r'$f_z$',         color='tab:red')
ax[0].set_title('Input: Specific Force')
ax[0].set_ylabel('[g]')
ax[0].set_xlabel('Time [s]')
ax[0].legend()
ax[0].grid(True)

# Angular velocity
ax[1].plot(t, omega_x_exp, label=r'$\omega_x$', color='tab:blue')
ax[1].plot(t, omega_y_exp, label=r'$\omega_y$', color='tab:green')
ax[1].plot(t, omega_z_exp, label=r'$\omega_z$', color='tab:red')
ax[1].set_title('Input: Angular Velocity')
ax[1].set_ylabel('[rad/s]')
ax[1].set_xlabel('Time [s]')
ax[1].legend()
ax[1].grid(True)

# Subjective vertical
ax[2].plot(t, SV_x, label=r'$SV_x$', color='tab:blue')
ax[2].plot(t, SV_y, label=r'$SV_y$', color='tab:green')
ax[2].plot(t, SV_z, label=r'$SV_z$', color='tab:red')
ax[2].set_title('Output: Subjective Vertical')
ax[2].set_ylabel('[g]')
ax[2].set_xlabel('Time [s]')
ax[2].legend()
ax[2].grid(True)

fig.suptitle('Tilt Simulation @ 5.0 rad/sec', fontsize=16)

plt.tight_layout()
plt.show()