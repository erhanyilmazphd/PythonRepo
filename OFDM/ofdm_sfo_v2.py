import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class OFDMSimulation:
    def __init__(self):
        # --- System Parameters ---
        self.N = 64  # FFT size
        self.CP = 16  # Cyclic Prefix length
        self.n_symbols = 100  # Number of symbols to simulate
        self.sfo_ppm = 50  # Sampling Frequency Offset in PPM (High value to make effect visible)

        # --- Pilot & Data Configuration ---
        # Standard IEEE 802.11a/g-like subcarrier mapping
        self.all_indices = np.arange(self.N)
        # Pilots at specific indices (shifted for -N/2 to N/2 view, then mapped to 0..N-1)
        self.pilot_indices = np.array([-21, -7, 7, 21]) + self.N // 2
        self.pilot_indices = np.fft.ifftshift(self.pilot_indices)  # Map to FFT input order

        # DC null
        self.dc_index = np.array([0])

        # Data indices: All minus (Pilots + DC)
        self.occupied_indices = np.setdiff1d(self.all_indices, self.dc_index)
        self.data_indices = np.setdiff1d(self.occupied_indices, self.pilot_indices)

        # Pilot Value (Fixed QPSK pilot)
        self.pilot_value = 1 + 0j

    def tx_chain(self):
        """Generates the time domain OFDM signal."""
        # 1. Generate Random Data (QPSK)
        n_data_carriers = len(self.data_indices)
        bits = np.random.randint(0, 4, (self.n_symbols, n_data_carriers))

        # QPSK Mapping: 0->1+j, 1->-1+j, 2->-1-j, 3->1-j
        mapping_table = {0: 1 + 1j, 1: -1 + 1j, 2: -1 - 1j, 3: 1 - 1j}
        # Normalize power
        self.tx_data_symbols = np.vectorize(mapping_table.get)(bits) / np.sqrt(2)

        # 2. Build Frequency Grid
        tx_grid = np.zeros((self.n_symbols, self.N), dtype=complex)

        # Map Data
        tx_grid[:, self.data_indices] = self.tx_data_symbols

        # Map Pilots
        tx_grid[:, self.pilot_indices] = self.pilot_value

        # Save grid for Rx reference
        self.tx_grid_ref = tx_grid

        # 3. IFFT (Frequency -> Time)
        tx_time = np.fft.ifft(tx_grid, axis=1)

        # 4. Add Cyclic Prefix
        tx_cp = np.hstack((tx_time[:, -self.CP:], tx_time))

        # Serialize to single stream
        self.tx_signal_serial = tx_cp.flatten()
        return self.tx_signal_serial

    def channel_with_sfo(self, tx_signal):
        """
        Simulates the channel and the SFO.
        SFO is modeled as a resampling of the time domain signal.
        """
        # Time vector for ideal Tx clock
        T_sample = 1.0  # Normalized sampling time
        t_tx = np.arange(len(tx_signal)) * T_sample

        # --- Apply SFO ---
        # Rx clock is faster or slower by SFO_ppm.
        # t_rx = t_tx * (1 + delta)
        # To simulate what the Rx 'sees', we interpolate the Tx signal
        # onto the Rx time instances.

        sfo_factor = 1 + (self.sfo_ppm * 1e-6)

        # The Rx takes samples at integer intervals [0, 1, 2...]
        # but these correspond to physical times [0, sfo_factor, 2*sfo_factor...]
        # We need to find the value of the Tx signal at these skewed times.

        # Create interpolation function from ideal Tx signal
        interpolator = interp1d(t_tx, tx_signal, kind='linear', fill_value="extrapolate")

        # Query the interpolator at the skewed time points
        # If Rx clock is faster (SFO > 0), it samples "later" in the signal earlier?
        # Actually: If Rx rate is fs' = fs(1+delta), then T' = T/(1+delta).
        # We sample at n*T'.
        t_rx_sampling_points = t_tx * sfo_factor

        rx_signal_sfo = interpolator(t_rx_sampling_points)

        # --- Add AWGN Noise ---
        snr_db = 200
        sig_power = np.mean(np.abs(rx_signal_sfo) ** 2)
        noise_power = sig_power * 10 ** (-snr_db / 10)
        noise = (np.random.randn(len(rx_signal_sfo)) + 1j * np.random.randn(len(rx_signal_sfo))) * np.sqrt(
            noise_power / 2)

        noise = 0

        return rx_signal_sfo + noise

    def rx_chain_and_correction(self, rx_serial):
        """
        Demodulates and performs SFO correction using Pilot Phase Tracking.
        """
        total_len = self.N + self.CP
        rx_grid = np.zeros((self.n_symbols, self.N), dtype=complex)

        # Arrays to store constellations for plotting
        uncorrected_constellation = []
        corrected_constellation = []

        print(f"Processing {self.n_symbols} symbols for SFO correction...")

        for i in range(self.n_symbols):
            # 1. CP Removal & FFT
            start_idx = i * total_len + self.CP
            end_idx = (i + 1) * total_len

            # Simple boundary check
            if end_idx > len(rx_serial): break

            rx_symbol_time = rx_serial[start_idx: end_idx]
            rx_symbol_freq = np.fft.fft(rx_symbol_time)

            rx_grid[i, :] = rx_symbol_freq

            # Extract raw data for "Uncorrected" plot
            uncorrected_constellation.extend(rx_symbol_freq[self.data_indices])

            # --- SFO & CFO Correction Block ---

            # 2. Extract Received Pilots
            rx_pilots = rx_symbol_freq[self.pilot_indices]

            # 3. Channel Estimation at Pilot Locations (LS Estimate)
            # H_est = Y_pilot / X_pilot
            # Since we transmitted 1+0j, H_est is just the received pilot (simplified)
            # In a real fading channel, you would divide by the known pilot sequence.
            h_est_pilots = rx_pilots / self.pilot_value

            # 4. Calculate Phase of the Pilots
            # SFO creates a linear phase slope across subcarriers.
            # CFO creates a constant phase offset (intercept).
            pilot_phases = np.angle(h_est_pilots)

            # Unwrapping is critical if phase exceeds pi
            pilot_phases = np.unwrap(pilot_phases)

            # 5. Linear Regression (The Fix for your Error)
            # We want to fit: phase = m * k + c
            # k are the subcarrier indices of the pilots.

            # Get pilot subcarrier indices in intuitive order (-N/2..N/2) for linear fit
            k_pilots = self.pilot_indices.copy()
            k_pilots[k_pilots >= self.N // 2] -= self.N
            k_pilots = np.sort(k_pilots)

            # Re-sort phases to match sorted k
            # (Note: self.pilot_indices definitions were fixed, but FFT order requires care.
            # Using fftshift helps align k visually)

            # Let's do it strictly on the indices we used to extract
            k_active = self.pilot_indices.copy()
            # Handle the wrapping for indices > N/2 for the math to represent "frequency" correctly
            k_active = np.where(k_active >= self.N / 2, k_active - self.N, k_active)

            # Construct Matrix A for Least Squares: [k, 1]
            A = np.vstack([k_active, np.ones(len(k_active))]).T

            # --- THE FIX IS HERE ---
            # numpy.linalg.lstsq returns (solution, residuals, rank, s)
            # We only need index [0]
            solution = np.linalg.lstsq(A, pilot_phases, rcond=None)[0]
            m, c = solution  # m = slope (timing error), c = intercept (phase error)

            # 6. Apply Correction
            # Generate correction vector for ALL subcarriers
            k_all = np.arange(self.N)
            k_all_shifted = np.where(k_all >= self.N / 2, k_all - self.N, k_all)

            # Correction phase = -(m*k + c)
            correction_phase = -(m * k_all_shifted + c)
            correction_factor = np.exp(1j * correction_phase)

            corrected_symbol = rx_symbol_freq * correction_factor
            corrected_constellation.extend(corrected_symbol[self.data_indices])

        return uncorrected_constellation, corrected_constellation

    def run(self):
        # 1. Tx
        tx_sig = self.tx_chain()

        # 2. Channel (SFO + Noise)
        rx_sig = self.channel_with_sfo(tx_sig)

        # 3. Rx & Correct
        uncorrected, corrected = self.rx_chain_and_correction(rx_sig)

        # 4. Visualization
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 3, 1)
        plt.scatter(np.real(self.tx_data_symbols), np.imag(self.tx_data_symbols), alpha=0.5, s=5, c='g')
        plt.title(f'TX Data Symbols')
        plt.grid(True)
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

        plt.subplot(1, 3, 2)
        plt.scatter(np.real(uncorrected), np.imag(uncorrected), alpha=0.5, s=5, c='r')
        plt.title(f'Uncorrected RX Constellation\n(SFO = {self.sfo_ppm} ppm)')
        plt.grid(True)
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

        plt.subplot(1, 3, 3)
        plt.scatter(np.real(corrected), np.imag(corrected), alpha=0.5, s=5, c='b')
        plt.title('Corrected RX Constellation\n(Pilot-based LS Estimation)')
        plt.grid(True)
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sim = OFDMSimulation()
    sim.run()