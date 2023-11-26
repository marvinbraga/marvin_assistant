import os.path

from frontend.audio.abstract_recorders import AbstractAudioRecorder
from pydub import AudioSegment
import wave


class Mp3Recorder(AbstractAudioRecorder):
    COMMAND_OUTPUT_FILENAME = "frontend/resources/command.mp3"

    def _save(self):
        temp_filename = os.path.normpath("frontend/resources/temp.wav")
        try:
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self._channels)
                wf.setsampwidth(self._audio_interface.get_sample_size(self._format))
                wf.setframerate(self._rate)
                wf.writeframes(b''.join(self._frames))

            sound = AudioSegment.from_wav(temp_filename)
            sound.export(os.path.normpath(self.COMMAND_OUTPUT_FILENAME), format="mp3")
        finally:
            os.remove(temp_filename)
        return self
