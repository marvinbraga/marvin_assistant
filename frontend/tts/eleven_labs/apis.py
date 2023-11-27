import json
import os.path

import requests


class ElevenLabsApi:

    def __init__(self, settings, stability=0.15, similarity_boost=0.5, language="portuguese"):
        self._name = settings.name
        self._settings = settings
        self._stability = stability
        self._similarity_boost = similarity_boost
        self._language = language

    def get_audio(self, message):
        payload = {
            "text": message,
            "model_id": "eleven_multilingual_v2",
            "language": self._language,
            "voice_settings": {
                "stability": self._stability,
                "similarity_boost": self._similarity_boost,
            }
        }

        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": self._settings.values["ELEVEN_LABS_API_KEY"],
            "Content-Type": "application/json",
        }

        voice = self._settings.get_voice_id(self._name)
        response = requests.post(
            f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?optimize_streaming_latency=0',
            json=payload,
            headers=headers,
        )
        if response.status_code == 200 and response.content:
            return response

        raise Exception(f"Problemas com o áudio - {response.status_code}.")

    def list(self):
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {
            "Accept": "application/json",
            "xi-api-key": self._settings.values["ELEVEN_LABS_API_KEY"],
        }
        response = requests.get(url, headers=headers)
        if response.status_code < 400:
            json_content = json.dumps(response.json(), indent=4)
            with open(os.path.normpath(self._settings.filename), 'w') as f:
                f.write(json_content)

            result = [voice["name"] for voice in response.json()["voices"]]
            return result

        return response.text


if __name__ == '__main__':
    from frontend.tts.eleven_labs.settings import Settings

    # Para criar seu arquivo de voices.
    _settings = Settings(name="Bella", filename="../../resources/voices.json")
    print(ElevenLabsApi(settings=_settings).list())

