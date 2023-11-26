import os.path
from threading import Thread

from playsound import playsound


class VoiceProducer:
    out_content_file = "resources/out_content_file.mp3"

    def __init__(self, content):
        self._content = content

    def play(self, filename):
        try:
            playsound(filename)
        finally:
            os.remove(filename)
        return self

    def make(self, thread_run=False):
        filename = os.path.normpath(self.out_content_file)
        with open(filename, "wb") as f:
            f.write(self._content)

        if thread_run:
            t = Thread(target=self.play, args=[filename])
            t.start()
        return self
