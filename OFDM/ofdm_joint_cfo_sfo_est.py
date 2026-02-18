import numpy as np
from numpy.fft import fft, ifft

def joint_OFDM_sync(r, X, N, max_iter=5, mu_eps=0.5, mu_eta=0.5):
    """
    Joint estimation of CFO, SFO, and channel response for OFDM systems.
    Parameters:
        r : ndarray
            Received time-domain OFDM symbol (after CP removal)
        X : ndarray
            Known transmitted subcarriers (pilot or preamble)
        N : int
            FFT size (number of subcarriers)
        max_iter : int
            EM iterations
        mu_eps, mu_eta : float
            Step sizes for CFO/SFO updates
    Returns:
        eps_hat, eta_hat, H_hat : tuple
            Estimated CFO, SFO, and frequency-domain channel
    """
    n = np.arange(N)
    eps_hat, eta_hat = 0.0, 0.0  # initial estimates
    H_hat = np.ones(N, dtype=complex)

    for _ in range(max_iter):
        # === E-step === (signal reconstruction)
        s_hat = ifft(X * H_hat, N)
        E_mat = np.exp(1j * 2 * np.pi * (eps_hat + eta_hat * n / N) * n / N)

        # === M-step === (update offsets)
        err = r - E_mat * s_hat
        grad_eps = np.imag(np.vdot(err, (1j * 2 * np.pi * n / N) * E_mat * s_hat)) / np.vdot(s_hat, s_hat)
        grad_eta = np.imag(np.vdot(err, (1j * 2 * np.pi * (n**2) / N**2) * E_mat * s_hat)) / np.vdot(s_hat, s_hat)

        eps_hat += mu_eps * grad_eps.real
        eta_hat += mu_eta * grad_eta.real

        # === Channel estimation update ===
        r_corr = E_mat.conj() * r
        Y = fft(r_corr, N)
        H_hat = Y / (X + 1e-9)  # LS update

    return eps_hat, eta_hat, H_hat


def simulate_joint_sync(N=64, CFO=0.04, SFO=40e-6, SNRdB=25):
    # Transmit QPSK symbols
    X = (2 * (np.random.randint(0, 2, N)) - 1) + 1j * (2 * (np.random.randint(0, 2, N)) - 1)
    s = ifft(X, N)
    n = np.arange(N)

    # Apply CFO, SFO, and noise
    E_true = np.exp(1j * 2 * np.pi * (CFO + SFO * n / N) * n / N)
    r = E_true * s
    noise = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2 * 10 ** (SNRdB / 10))
    r += noise

    # Joint estimation
    eps_hat, eta_hat, H_hat = joint_OFDM_sync(r, X, N, max_iter=8)

    print(f"True CFO={CFO:.5f}, Est CFO={eps_hat:.5f}")
    print(f"True SFO={SFO:.1e}, Est SFO={eta_hat:.1e}")
    return eps_hat, eta_hat, H_hat


simulate_joint_sync()


