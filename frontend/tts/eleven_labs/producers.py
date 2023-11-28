import os.path
import uuid


class VoiceProducer:

    def __init__(self, content, remove_after=False):
        self._remove_after = remove_after
        self._content = content
        self.out_content_file = f"resources/out_content_{uuid.uuid4()}.mp3"

    def make(self, thread_run=False):
        filename = os.path.normpath(self.out_content_file)
        with open(filename, "wb") as f:
            f.write(self._content)
        return self
