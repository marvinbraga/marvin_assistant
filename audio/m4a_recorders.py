import os.path

from audio.abstract_recorders import AbstractAudioRecorder
from pydub import AudioSegment
import wave


class M4aRecorder(AbstractAudioRecorder):
    COMMAND_OUTPUT_FILENAME = "resources/command.m4a"

    def _save(self):
        temp_filename = os.path.normpath("resources/temp.wav")
        try:
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self._channels)
                wf.setsampwidth(self._audio_interface.get_sample_size(self._format))
                wf.setframerate(self._rate)
                wf.writeframes(b''.join(self._frames))

            sound = AudioSegment.from_wav(temp_filename)
            sound.export(self.COMMAND_OUTPUT_FILENAME, format="mp4", codec="aac")
        finally:
            os.remove(temp_filename)
        return self
