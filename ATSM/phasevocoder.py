"""
module containing PhaseVocoder algorithim
"""
import numpy as np
from ATSM.base import A2S_TSM, Converter
from ATSM.utils import Windows as W

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
    
    def __init__(self, channels: int, frame_length: int, 
                       analysis_hop: int, synthesis_hop: int, 
                       peak_finder: object):

        self.__chanels: int = channels
        self.__frame_length: int = frame_length
        self.__analysis_hop: int = analysis_hop
        self.__synthesis_hop: int = synthesis_hop
        self.__find_peaks: object = peak_finder

        self.__center_freq: np.ndarray = np.fft.rfftfreq(frame_length) * 2 * np.pi
        fft_length: int = len(self.__center_freq)

        self.__first: bool = True

        self.__previous_phase: np.ndarry = np.empty([channels, fft_length])
        self.__output_phase: np.ndarry = np.empty([channels, fft_length])

        self.__buffer: np.ndarray = np.empty(fft_length)


    @property
    def channels(self) -> int:
        return self.__channels

    @property
    def frame_length(self) -> int:
        return self.__frame_length

    @property
    def analysis_hop(self) -> int:
        return self.__analysis_hop
    
    @analysis_hop.setter
    def analysis_hop(self, analysis_hop: int):
        self.__analysis_hop: int = analysis_hop

    @property
    def synthesis_hop(self) -> int:
        return self.__synthesis_hop

    @property
    def find_peaks(self) -> object:
        return self.__find_peaks

    @property
    def center_freq(self) -> np.ndarray:
        return self.__center_freq

    @property
    def buffer(self) -> np.ndarray:
        return self.__buffer

    @property
    def first(self) -> bool:
        return self.__first
    
    @first.setter
    def first(self, first: bool) -> None:
        self.__first: bool = first

    @property
    def previous_phase(self) -> np.ndarray:
        return self.__previous_phase
    
    @previous_phase.setter
    def previous_shape(self, phase: np.ndarray):
        self.__previous_shape: np.ndarray = phase

    @property
    def output_phase(self) -> np.ndarray:
        return self.__output_phase

    @output_phase.setter
    def output_phase(self, phase: np.ndarray):
        self.__output_phase: np.ndarray = phase


    def clear(self):
        self.__first: bool = True

    def convert_frame(self, frame: np.ndarray) -> np.ndarray:

        for k in range(0, self.channels):

            stft: np.ndarray = np.fft.rfft(frame[k])
            amplitude: np.ndarray = np.abs(stft)
            phase: np.ndarray = np.angle(stft)
            del stft

            peaks: np.ndarray = self.find_peaks(amplitude)
            closest_peak: np.ndarray = Peaks.get_closest(peaks=peaks)

            if self.first:
                # ignore first frame
                self.output_phase[k, :] = phase
            else:
                # find phase increment
                self.buffer[peaks] = (
                    phase[peaks] - self.previous_phase[k, peaks] -
                    self.analysis_hop * self.center_freq[peaks]
                )
                # unwrap the phase increment
                self.buffer[peaks] += np.pi
                self.buffer[peaks] %= 2 * np.pi
                self.buffer[peaks] -= np.pi
                # find instantaneous frequency 
                self.buffer[peaks] /= self.analysis_hop
                self.buffer[peaks] += self.center_freq[peaks]
                self.buffer[peaks] *= self.synthesis_hop

                self.output_phase[k][peaks] += self.buffer[peaks]
                # phase locking
                self.output_phase[k] = (
                    self.output_phase[k][closest_peak] +
                    phase - phase[closest_peak]
                ) 

                # find the new stft
                output_stft = amplitude * np.exp(1j * self.output_phase[k])

                frame[k, :] = np.fft.irfft(output_stft).real

            self.previous_shape[k, :] = phase
            del phase
            del amplitude

        self.first = False

        return frame

    def set_analysis_hop(self, analysis_hop: int):
        self.__analysis_hop: int = analysis_hop


class PhaseLocking(object):
    
    NONE: int = 0

    IDENTITY: int = 1

    @classmethod
    def from_str(cls, name: str):

        if name.lower() == 'none':
            strategy = cls.NONE
        elif name.lower() == 'identity':
            strategy = cls.IDENTITY

        else:
            raise ValueError(f'Invalid phase locking name: "{name}"')

class PhaseVocoder(PhaseVocoderConverter):

    def __init__(self, channels: int, speed: float = 1., 
                       frame_length: int = 2048, analysis_hop: int = None,
                       synthesis_hop: int = None, phase_locking: int = PhaseLocking.IDENTITY):

        self.__channels: int = channels
        self.__speed: float = speed
        self.__frame_length: int = frame_length
        self.__analysis_hop: int = analysis_hop
        self.__synthesis_hop: int = synthesis_hop
        self.__phase_locking: int = phase_locking

    @property
    def channels(self) -> int:
        return self.__channels

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def frame_length(self) -> int:
        return self.__frame_length

    @property
    def analysis_hop(self) -> int:
        return self.__analysis_hop

    @analysis_hop.setter
    def analysis_hop(self, analysis_hop: int):
        self.__analysis_hop: int = analysis_hop

    @property
    def synthesis_hop(self) -> int:
        return self.__synthesis_hop

    @synthesis_hop.setter
    def synthesis_hop(self, synthesis_hop: int):
        self.__synthesis_hop: int = synthesis_hop 

    @property
    def phase_locking(self) -> int:
        return self.__phase_locking

    @phase_locking.setter
    def phase_locking(self, phase_locking: int):
        self.__phase_locking: int = phase_locking

    @property
    def converter(self) -> Converter:
        return self.__converter

    @property
    def analysis_window(self) -> np.ndarray:
        return self.__analysis_window

    @property
    def synthesis_window(self) -> np.ndarray:
        return self.__synthesis_window


    def setVariables(self) -> None:

        if self.synthesis_hop is None:
            self.synthesis_hop: int = self.frame_length // 4

        if self.analysis_hop is None:
            self.analysis_hop: int = int(self.synthesis_hop * self.speed)

        self.__analysis_window: np.ndarray = W.hanning(self.frame_length)
        self.__synthesis_window: np.ndarray = W.hanning(self.frame_length)

        if self.phase_locking == PhaseLocking.IDENTITY:
            peak_finder: object = Peaks.all

        elif self.phase_locking == PhaseLocking.NONE:
            peak_finder: object = Peaks.find

        else:
            raise ValueError(
                f'Invalid phase_locking value: "{self.phase_locking}"'
            )    

        super().__init__(channels=self.channels, frame_length=self.frame_length,
                         analysis_hop=self.analysis_hop, synthesis_hop=self.analysis_hop,
                         peak_finder=peak_finder)
        
        self.__converter: Converter = super()

    def convert(self) -> A2S_TSM:

        self.setVariables()

        return A2S_TSM(
            self.converter, self.channels, self.frame_length,
            self.analysis_hop, self.synthesis_hop,
            self.analysis_window, self.synthesis_window
        )