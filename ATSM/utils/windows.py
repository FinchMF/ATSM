
import numpy as np

class Windows:

    @staticmethod
    def apply(buffer: np.ndarray, window: np.ndarray) -> None:

        if window is None:
            return

        for channel in buffer:
            channel *= window

    @staticmethod
    def hanning(length: int) -> np.ndarray:

        if length <= 0:
            return np.zeros(0)

        time = np.arange(length)
        return 0.5 * (1 - np.cos(2 * np.pi * time / length))

    @staticmethod
    def product(window_1: np.ndarray, window_2: np.ndarray) -> (np.ndarray, None):

        if window_1 is None:
            W: np.ndarray = window_2

        elif window_2 is None:
            W: np.ndarray = window_1

        else:
            W: np.ndarray = window_1 * window_2 
        
        return W