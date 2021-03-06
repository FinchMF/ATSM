"""
module containing window operations 
"""

import numpy as np

class Windows:
    """object to house to window operations"""
    @staticmethod
    def apply(buffer: np.ndarray, window: np.ndarray) -> None:
        """function to set buffer to window"""
        if window is None:
            return

        for channel in buffer:
            channel *= window

    @staticmethod
    def hanning(length: int) -> np.ndarray:
        """function for hanning operation"""
        if length <= 0:
            return np.zeros(0)

        time = np.arange(length)
        return 0.5 * (1 - np.cos(2 * np.pi * time / length))

    @staticmethod
    def product(window_1: np.ndarray, window_2: np.ndarray) -> (np.ndarray, None):
        """function for production operation of two windows"""
        if window_1 is None:
            return window_2

        if window_2 is None:
            return window_1

        return window_1 * window_2