import threading
from abc import ABCMeta, abstractmethod

# sudo apt install python3-pyaudio portaudio19-dev
import pyaudio


class AbstractAudioRecorder(metaclass=ABCMeta):
    COMMAND_OUTPUT_FILENAME = None

    def __init__(self, audio_format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024, audio_interface=None):
        self._format = audio_format
        self._channels = channels
        self._rate = rate
        self._chunk = chunk
        self._audio_interface = audio_interface or pyaudio.PyAudio()
        self._frames = []
        self._recording = False
        self._stream = None
        self._record_thread = None

    def start_recording(self):
        self._frames = []
        self._recording = True
        self._stream = self._audio_interface.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
        )
        self._record_thread = threading.Thread(target=self._record)
        self._record_thread.start()

    def stop_recording(self):
        self._recording = False
        self._record_thread.join()
        self._stream.stop_stream()
        self._stream.close()

    def _record(self):
        while self._recording:
            data = self._stream.read(self._chunk)
            self._frames.append(data)

    @abstractmethod
    def _save(self):
        pass

    def save(self):
        if self.COMMAND_OUTPUT_FILENAME is None:
            assert "Você deve informar um nome para o arquivo no atributo 'COMMAND_OUTPUT_FILENAME'."
        self._save()
        return self
