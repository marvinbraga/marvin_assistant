import os
import wave

from frontend.audio.abstract_recorders import AbstractAudioRecorder


class WaveRecorder(AbstractAudioRecorder):
    COMMAND_OUTPUT_FILENAME = "frontend/resources/command.wav"

    def _save(self):
        with wave.open(os.path.normpath(self.COMMAND_OUTPUT_FILENAME), 'wb') as wf:
            wf.setnchannels(self._channels)
            wf.setsampwidth(self._audio_interface.get_sample_size(self._format))
            wf.setframerate(self._rate)
            wf.writeframes(b''.join(self._frames))
        return self
