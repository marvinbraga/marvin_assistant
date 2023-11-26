import wave

from audio.abstract_recorders import AbstractAudioRecorder


class WaveRecorder(AbstractAudioRecorder):
    COMMAND_OUTPUT_FILENAME = "resources/command.wav"

    def _save(self):
        with wave.open(self.COMMAND_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self._channels)
            wf.setsampwidth(self._audio_interface.get_sample_size(self._format))
            wf.setframerate(self._rate)
            wf.writeframes(b''.join(self._frames))
        return self
