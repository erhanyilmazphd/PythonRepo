import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class OFDM_System:
    def __init__(self, n_fft=64, n_cp=16, n_sym=50, sfo_ppm=200):
        self.n_fft = n_fft
        self.n_cp = n_cp
        self.n_sym = n_sym  # Number of symbols in the frame
        self.sfo_ppm = sfo_ppm  # Sampling Frequency Offset in PPM
        self.dc_index = n_fft // 2  # DC subcarrier index (center)

        # Pilot configuration (4 pilots scattered in the band)
        # Pilots are inserted at indices relative to DC
        self.pilot_indices = np.array([-21, -7, 7, 21]) + self.dc_index
        self.pilot_val = 1.0 + 0j  # Known pilot value

        # Data configuration
        self.all_indices = np.arange(n_fft)

        # Exclude DC and Pilots from Data Indices
        # We assume the user wants to ensure DC is handled in the concatenation
        self.data_indices = np.setdiff1d(self.all_indices,
                                         np.concatenate(([self.dc_index], self.pilot_indices)))

    def transmitter(self):
        """Generates OFDM frame with pilots."""
        # 1. Generate Random Data (QPSK)
        n_data = len(self.data_indices) * self.n_sym
        bits = np.random.randint(0, 2, (n_data, 2))
        qpsk = (2 * bits[:, 0] - 1) + 1j * (2 * bits[:, 1] - 1)
        qpsk *= 1 / np.sqrt(2)  # Normalize power

        tx_serial = []

        for i in range(self.n_sym):
            # Map data and pilots to subcarriers
            symbol_data = qpsk[i * len(self.data_indices): (i + 1) * len(self.data_indices)]
            freq_domain = np.zeros(self.n_fft, dtype=complex)

            # Map Data
            freq_domain[self.data_indices] = symbol_data
            # Map Pilots
            freq_domain[self.pilot_indices] = self.pilot_val
            # DC is left as 0.0

            # IFFT (Shift to center DC before IFFT)
            time_domain = np.fft.ifft(np.fft.fftshift(freq_domain))

            # Add Cyclic Prefix
            cp = time_domain[-self.n_cp:]
            ofdm_sym = np.concatenate((cp, time_domain))
            tx_serial.append(ofdm_sym)

        return np.concatenate(tx_serial)

    def channel_with_sfo(self, tx_signal):
        """
        Simulates the wireless channel and SFO.
        SFO is modeled by resampling the continuous waveform.
        """
        # 1. Apply SFO (Resampling)
        # SFO > 0 means Rx clock is faster (periods are shorter), so it records MORE samples.
        # However, physically, if Rx freq is higher, it samples the same duration with MORE ticks.
        # We simulate this by interpolating the Tx signal onto the Rx time grid.

        # Rx sample rate factor relative to Tx
        sfo_factor = 1 + self.sfo_ppm * 1e-6
        #sfo_factor = 1

        # Time vector for Tx signal (Ideal)
        t_tx = np.arange(len(tx_signal))

        # Interpolator (Simulating Continuous Time Signal reconstruction)
        # We separate Real and Imag parts for interpolation
        interpolator_real = interp1d(t_tx, tx_signal.real, kind='cubic', fill_value="extrapolate")
        interpolator_imag = interp1d(t_tx, tx_signal.imag, kind='cubic', fill_value="extrapolate")

        # Rx time grid
        # If Rx clock is faster (factor > 1), it takes more samples to cover the same Tx duration.
        # Or, for the same number of samples 'n' at Rx, the physical time 't' is different.
        # t_rx_sample_index = n
        # t_physical = n * T_rx = n * (T_tx / sfo_factor)
        # We want the signal value at t_physical.

        n_samples_rx = int(len(tx_signal) * sfo_factor)  # Approximate new length
        rx_indices = np.arange(n_samples_rx)

        # The "Tx time" corresponding to the Rx sample index 'n'
        t_instant_at_tx = rx_indices / sfo_factor

        # Resample
        rx_real = interpolator_real(t_instant_at_tx)
        rx_imag = interpolator_imag(t_instant_at_tx)
        rx_signal = rx_real + 1j * rx_imag

        # 2. Add AWGN
        noise_power = 0.00001
        #noise = np.sqrt(noise_power / 2) * (np.random.randn(len(rx_signal)) +
        #                                    1j * np.random.randn(len(rx_signal)))
        noise = 0

        return rx_signal + noise

    def receiver_correction(self, rx_signal):
        """
        Receiver processing: Sync, FFT, SFO Estimation, Correction.
        """
        corrected_symbols = []
        raw_symbols = []

        symbol_len = self.n_fft + self.n_cp

        # In a real system, we would have a Sample Timing Offset (STO) loop.
        # Here, we blindly chop the stream into symbol lengths.
        # Because of SFO, the "true" start of the symbol drifts.
        # We account for the rate change roughly to keep the window valid for this demo.
        sfo_rate = 1 + self.sfo_ppm * 1e-6
        #sfo_rate = 1

        for i in range(self.n_sym):
            # Calculate the start index accounting for the drift roughly
            # (In practice, STO loop tracks this)
            start_idx = int(i * symbol_len * sfo_rate)

            # Safety check
            if start_idx + symbol_len > len(rx_signal):
                break

            y_time = rx_signal[start_idx: start_idx + symbol_len]

            # Remove CP
            y_payload = y_time[self.n_cp:]

            # If payload length doesn't match FFT size due to rough slicing, trim/pad
            # (Resampling introduces fractional lengths, but we slice integers)
            if len(y_payload) > self.n_fft:
                y_payload = y_payload[:self.n_fft]
            elif len(y_payload) < self.n_fft:
                y_payload = np.pad(y_payload, (0, self.n_fft - len(y_payload)))

            # FFT
            y_freq = np.fft.fftshift(np.fft.fft(y_payload))
            raw_symbols.extend(y_freq[self.data_indices])

            # --- SFO ESTIMATION & CORRECTION ---

            # 1. Extract Pilots
            rx_pilots = y_freq[self.pilot_indices]

            # 2. Estimate Phase Error at Pilot Locations
            # Phase Error = angle(Rx_Pilot * conj(Tx_Pilot))
            # We assume we know the transmitted pilot value
            pilot_phases = np.angle(rx_pilots * np.conj(self.pilot_val))

            # Unwrap to ensure the linear fit works for rotations > pi
            pilot_phases = np.unwrap(pilot_phases)

            # 3. Estimate Slope (Linear Regression)
            # Theory: Phase_k = 2*pi * k * (SFO_drift + CFO)
            # We map pilot indices to centered subcarrier grid relative to DC
            centered_pilot_idx = self.pilot_indices - self.n_fft // 2

            # Fit line: y = m*x + c
            # m (slope) -> Sampling Time Error (proportional to subcarrier index)
            # c (intercept) -> Common Phase Error (CFO + Phase Noise)
            A = np.vstack([centered_pilot_idx, np.ones(len(centered_pilot_idx))]).T
            m, c = np.linalg.lstsq(A, pilot_phases, rcond=None)[0]

            print(f"SFO:{m}, CFO + Phase Noise:{c}")

            # 4. Apply Correction
            # Correction vector: exp( -j * (slope * k + intercept) )
            centered_data_idx = self.data_indices - self.n_fft // 2
            correction_phasor = np.exp(-1j * (m * centered_data_idx + c))

            y_freq_corrected = y_freq[self.data_indices] * correction_phasor
            corrected_symbols.extend(y_freq_corrected)

        return np.array(raw_symbols), np.array(corrected_symbols)


# --- Execution ---
# Using 500 ppm to visually exaggerate the rotation effect
sim = OFDM_System(n_fft=64, n_cp=16, n_sym=50, sfo_ppm=500)
tx = sim.transmitter()
rx = sim.channel_with_sfo(tx)
raw, corrected = sim.receiver_correction(rx)

# --- Visualization ---
plt.figure(figsize=(12, 5))

# Plot 1: Raw Received Constellation (Spinning)
plt.subplot(1, 2, 1)
plt.scatter(raw.real, raw.imag, alpha=0.5, s=10, c=np.arange(len(raw)), cmap='viridis')
plt.title(
    f'Raw Rx Constellation (SFO = {sim.sfo_ppm} ppm)\nNote the rotation over time (color) and subcarrier (radial)')
plt.xlabel('I')
plt.ylabel('Q')
plt.grid(True, alpha=0.3)
plt.xlim([-2, 2])
plt.ylim([-2, 2])
cbar = plt.colorbar()
cbar.set_label('Time (Symbol Index)')

# Plot 2: Corrected Constellation
plt.subplot(1, 2, 2)
plt.scatter(corrected.real, corrected.imag, alpha=0.5, s=10, c='g')
plt.title('Corrected Constellation\n(Pilot-based Slope Derotation)')
plt.xlabel('I')
plt.ylabel('Q')
plt.grid(True, alpha=0.3)
plt.xlim([-2, 2])
plt.ylim([-2, 2])

plt.tight_layout()
plt.show()