
import numpy as np

from ATSM.base import A2S_TSM, Converter
from ATSM.utils import Window as W

class Peaks:

    @staticmethod
    def find(amplitude: np.ndarray) -> np.ndarray:

        padded: np.ndarray = np.concatenate((-np.ones(2), amplitude, -np.ones(2)))

        shifted_l2: np.ndarray = padded[:-4]
        shifted_l1: np.ndarray = padded[1:-3]
        shifted_r1: np.ndarray = padded[3:-1]
        shifted_r2: np.ndarray = padded[4:]

        peaks: np.array = ((amplitude >= shifted_l2) & (amplitude >= shifted_l1)
                            (amplitude >= shifted_r1) & (amplitude >= shifted_r2))

        return peaks

    @staticmethod
    def all(amplitude: np.ndarray) -> np.ndarray:

        return np.ones_like(amplitude, dtype=bool)

    @staticmethod
    def get_closest(peaks: np.ndarray) -> np.ndarray:

        closest_peak: np.ndarray = np.empty_like(peaks, dtype=int)
        previous: int = -1
        for i, is_peak in enumerate(peaks):
            if is_peak:
                if previous >= 0:
                    closest_peak[previous:(previous + i) // 2 + 1]: int = previous
                    closest_peak[(previous + i) // 2 + 1:i]: int = i
                else:
                    closest_peak[:i]: int = i
                previous: int = i
        closest_peak[previous:]: int = previous

        return closest_peak


class PhaseVocoderConverter(Converter):
    pass


class PhaseLocking(object):
    pass

    



