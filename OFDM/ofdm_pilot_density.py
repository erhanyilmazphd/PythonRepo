import numpy as np
import matplotlib.pyplot as plt

def adaptive_pilot_density(f_d, T_sym, eta, N, Nmin=4, k_eta=50):
    # Doppler-limited pilot density
    pilot_doppler = 1 / (2 * f_d * T_sym)
    # Sampling-offset-limited pilot density
    pilot_sfo = k_eta * abs(eta) * N
    # Final adaptive pilot count
    Np = int(np.ceil(max(Nmin, min(N, pilot_doppler + pilot_sfo))))
    return Np

# Example: 5 GHz carrier, 120 kHz subcarrier spacing (5G)
f_c = 5e9
v = 60 / 3.6             # 60 km/h user
c = 3e8
f_d = v * f_c / c        # Doppler shift ≈ 277 Hz
T_sym = 1/120e3          # 8.33 µs
eta = 30e-6              # 30 ppm
N = 128

Np = adaptive_pilot_density(f_d, T_sym, eta, N)
print(f"Recommended pilot tones per OFDM symbol: {Np}")


#----------------------------------------------------------------------------------
etas = [10e-6, 30e-6, 50e-6]
velocities = np.linspace(1, 150, 10)  # km/h
f_c = 5e9; c = 3e8; N = 128; T_sym = 1/120e3

plt.figure(figsize=(7,5))
for eta in etas:
    pilots = [adaptive_pilot_density(v/3.6 * f_c / c, T_sym, eta, N) for v in velocities]
    plt.plot(velocities, pilots, label=f'SFO={eta*1e6:.0f} ppm')

plt.grid(True, ls=':')
plt.xlabel('User Speed (km/h)')
plt.ylabel('Optimal Pilot Count per OFDM Symbol')
plt.title('Adaptive Pilot Density vs. Mobility & SFO')
plt.legend()
plt.show()
