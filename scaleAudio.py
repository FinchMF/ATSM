import argparse
from ATSM import PhaseVocoder, WSOLA, OLA
from ATSM.io.wav import WavIn, WavOut

class ModulatorError(Exception):
    pass

class Modulator(object):

    def __init__(self, input_wav: str, output_wav: str, time_scale: str, speed: float = 0.5):

        self.input_wav: str = input_wav
        self.output_wav: str = output_wav
        self.speed: float = speed
        
        if time_scale.lower() == 'phasevocoder':
            self.converter = PhaseVocoder
        
        elif time_scale.lower() == 'wsola':
            self.converter = WSOLA

        elif time_scale.lower() == 'ola':
            self.converter = OLA

        else:
            raise ModulatorError(f'Time Modulation type not supported: {time_scale}\
                                   please choose from: phasevocoder, wsola, ola')


    def convert(self) -> None:

        with WavIn(self.input_wav) as reader:
            with WavOut(self.output_wav, reader.channels, reader.samplerate) as writer:
                tsm = self.converter(reader.channels, speed=self.speed).convert()
                tsm.run(reader, writer)

if __name__ == '__main__':


    parser: object = argparse.ArgumentParser()

    parser.add_argument('-i', '-audio_in', type=str, help='name of audio file to be modulated')
    parser.add_argument('-o', '-audio_out', type=str, help='name of output file for modulated audio')
    parser.add_argument('-t', '-time_scale_modulator', type=str, help='type of time scale algorithim')
    parser.add_argument('-s', '-speed', type=float, help='rate of modulation')

    args: object = parser.parse_args()

    TSM: Modulator = Modulator(input_wav=args.i, 
                               output_wav=args.o, 
                               time_scale=args.t, 
                               speed=args.s)
    TSM.convert()