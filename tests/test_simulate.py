from simulator.simulate import simulate
import numpy as np

def test_intensity_monotonic():
    low = simulate(10, 40).mean()
    high = simulate(500, 120).mean()
    assert high > low