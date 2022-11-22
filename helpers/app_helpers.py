"""Helpers for the app."""

import numpy as np

def calculate_vwfo(N,current_design_value,filtered_destination_designs_values):
    """Calculate the VWFO value for a given design."""
    sigma = 0
    for destination_design_value in filtered_destination_designs_values:
        sigma += np.sign(destination_design_value - current_design_value)
    vwfo = 1 / (N-1) * sigma
    return vwfo
