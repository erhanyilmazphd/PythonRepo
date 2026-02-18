import numpy as np

# Schmidl & Cox (Time-Domain) CFO Estimator

def cfo_est(r):
    Np = len(r)//2   # Np = N/2
    P = np.sum(r[:Np] * np.conj(r[Np:]))
    eps_hat = np.angle(P)/np.pi

    return eps_hat
