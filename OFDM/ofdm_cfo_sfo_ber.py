import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft


def simulate_OFDM_BER_plot(M=64, N=64, Ncp=16, CFO=0.05, SFO=30e-6, SNRdB=np.arange(0, 31, 5)):
    k = int(np.log2(M))
    ber = np.zeros_like(SNRdB, dtype=float)
    X_const = np.sqrt(1 / 42) * (
                2 * np.random.randint(0, 8, N) - 7 + 1j * (2 * np.random.randint(0, 8, N) - 7))  # 64-QAM-like

    for i, snr in enumerate(SNRdB):
        errors = 0
        bits_total = 0
        for _ in range(200):  # Monte Carlo runs
            # Random OFDM symbol
            bits = np.random.randint(0, 2, N * k)
            X = X_const
            s = ifft(X, N)
            tx = np.concatenate([s[-Ncp:], s])
            n = np.arange(len(tx))

            # Apply CFO and SFO
            rx = tx * np.exp(1j * 2 * np.pi * CFO * n / N)
            rx = np.interp(n * (1 + SFO), n, rx)

            # Add AWGN
            noise = (np.random.randn(len(rx)) + 1j * np.random.randn(len(rx))) / np.sqrt(2 * 10 ** (snr / 10))
            rx += noise

            # Receiver (assume perfect sync for baseline)
            rx_corr = rx * np.exp(-1j * 2 * np.pi * CFO * n / N)
            y = fft(rx_corr[Ncp:Ncp + N])

            # Decision & BER
            decisions = np.sign(np.real(y)) + 1j * np.sign(np.imag(y))
            errors += np.sum(np.sign(np.real(y)) != np.sign(np.real(X))) + np.sum(
                np.sign(np.imag(y)) != np.sign(np.imag(X)))
            bits_total += 2 * N
        ber[i] = errors / bits_total

    plt.figure(figsize=(7, 5))
    plt.semilogy(SNRdB, ber, 'o-', label='64-QAM, CFO/SFO impaired')
    plt.grid(True, which='both', ls=':')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('BER vs. SNR for CFO/SFO-Impaired OFDM (64-QAM)')
    plt.legend()
    plt.show()


simulate_OFDM_BER_plot()
