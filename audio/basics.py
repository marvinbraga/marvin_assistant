from audio.abstract_recorders import AbstractAudioRecorder
from audio.players import AudioPlayer


class AudioRecorder:
    SOUND_BEEP = "resources/beep_short.mp3"

    def __init__(self, recorder: AbstractAudioRecorder):
        self._recorder = recorder
        self._is_recording = True

    @property
    def is_recording(self):
        return self._is_recording

    @property
    def recorder(self):
        return self._recorder

    def start(self):
        AudioPlayer(self.SOUND_BEEP).execute()
        self._is_recording = True
        self._recorder.start_recording()
        return self

    def stop(self):
        self._is_recording = False
        self._recorder.stop_recording()
        self._recorder.save()
        AudioPlayer(self.SOUND_BEEP).execute()
        return self
