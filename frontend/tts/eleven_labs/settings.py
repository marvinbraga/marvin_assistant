import json
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings:
    """
    A classe Settings é responsável por carregar configurações a partir de um arquivo JSON.
    """

    def __init__(self, name, filename):
        self._name = name
        self._filename = os.path.normpath(filename)
        self._values = self.load_settings()
        self._values["ELEVEN_LABS_API_KEY"] = os.environ["ELEVEN_LABS_API_KEY"]

    @property
    def name(self):
        return self._name

    @property
    def filename(self):
        return self._filename

    @property
    def values(self):
        return self._values

    def load_settings(self) -> dict:
        if os.path.isfile(self._filename):
            with open(self._filename, 'r') as f:
                return json.load(f)
        return {"result": False}

    def get_voice_id(self, name):
        for voice in self._values.get("voices"):
            if voice.get("name") == name:
                return voice.get("voice_id")
        raise Exception("Voice not found.")
