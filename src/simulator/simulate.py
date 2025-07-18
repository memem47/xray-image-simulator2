"""
Simple X-ray image simulator.

X-ray intensity ∝ tube_current (mA) x tube_voltage (kVp).
We approximate attenuation with a centered Gaussian spot.
"""

from __future__ import annotations
import numpy as np

def simulate(current_ma: float, voltage_kvp: float,
             size: int = 512) -> np.ndarray:
    # normalization so output remains 0-255
    intensity = (current_ma * voltage_kvp) / (500 * 120)
    # base image: smooth radial gradient (simulating focal spot blur)
    y, x = np.ogrid[-1:1:size*1j, -1:1:size*1j]
    r = np.sqrt(x**2 + y**2)
    img = np.exp(-4 * r**2) * intensity  # Gaussian blob
    img = np.clip(img * 255, 0, 255).astype(np.uint8)
    return img