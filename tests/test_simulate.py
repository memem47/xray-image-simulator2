from simulator.simulate import simulate
import numpy as np

def test_intensity_monotonic():
    low = simulate(200, 100, exponent_n=1.0).mean()
    high = simulate(200, 100, exponent_n=2.5).mean()
    assert high > low