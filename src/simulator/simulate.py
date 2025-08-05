"""
Simple X-ray image simulator.

X-ray intensity ∝ tube_current (mA) x tube_voltage (kVp).
We approximate attenuation with a centered Gaussian spot.
"""

from __future__ import annotations
import numpy as np


# ---------- Physical / empirical constants --------------------------------
MAX_MA:      float = 500.0         # [mA] GUI upper limit
MAX_KVP:     float = 120.0         # [kVp] GUI upper limit
DEFAULT_EXP_MS: float = 10.0       # [ms] default exposure time
DOSE_EXPONENT:  float = 1.7        # n in dose ∝ (kVp)^n
GAUSS_STD:      float = 0.5        # controls beam‑profile width
PHOTON_SCALE:   float = 1.0e4      # photons per unit relative dose

# --------------------------------------------------------------------------
def simulate(
    current_ma: float,
    voltage_kvp: float,
    *,
    exp_ms: float = DEFAULT_EXP_MS,
    exponent_n: float = DOSE_EXPONENT,
    photon_scale: float = PHOTON_SCALE,
    gauss_std: float = GAUSS_STD,
    size: int = 512,
) -> np.ndarray:
    """
    Parameters
    ----------
    current_ma : tube current [mA]
    voltage_kvp : tube voltage [kVp]
    exp_ms : exposure time [ms]
    exponent_n : exponent in dose law
    photon_scale : photons per unit relative dose (arbitrary)
    gauss_std : width of Gaussian beam profile
    size : output image size (square)

    Returns
    -------
    8-bit numpy array shape (size, size)
    """
    # --- Relative entrance dose ---
    mAs = current_ma * exp_ms / 1000.0
    dose_rel = mAs * (voltage_kvp ** exponent_n) / (MAX_MA * (MAX_KVP ** DOSE_EXPONENT))

    # --- Photon map ---
    y, x = np.ogrid[-1:1:size*1j, -1:1:size*1j]
    r2 = x**2 + y**2
    photons = np.exp(-r2 / (2 * gauss_std**2)) * dose_rel * photon_scale # photon count scale
    
    # --- Quantum noise ---
    photons_noisy = np.random.poisson(photons).astype(np.float32)
    
    # --- 8-bit normalisation---
    img = np.clip((photons_noisy / photons_noisy.max()) * 255, 0, 255).astype(np.uint8)
    return img