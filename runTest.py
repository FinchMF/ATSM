from ATSM import PhaseVocoder, OLA
from ATSM.io.wav import WavIn, WavOut

input_filename = '/Users/finchmf/coding/brooksAudio/Beach_House_Space_Song.wav'
output_filename = 'example_V.wav'

with WavIn(input_filename) as reader:
    with WavOut(output_filename, reader.channels, reader.samplerate) as writer:
        tsm = PhaseVocoder(channels=reader.channels, speed=0.5).convert()
        tsm.run(reader, writer)
