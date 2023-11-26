import os

from assistants.voice_assistant import VoiceAssistant
from audio.basics import AudioRecorder
from audio.m4a_loaders import M4aAudioLoader
from audio.m4a_recorders import M4aRecorder
from tts.eleven_labs.apis import ElevenLabsApi
from tts.eleven_labs.settings import Settings


def main():
    # Áudio recorder.
    recorder = M4aRecorder()
    save_dir = os.path.dirname(recorder.COMMAND_OUTPUT_FILENAME)
    # Áudio TTS API.
    # Recupera o áudio da API.
    tts_api = ElevenLabsApi(settings=Settings(name="Bella", filename="resources/voices.json"))
    # Inicializando o assistente.
    assistant = VoiceAssistant(
        audio_recorder=AudioRecorder(recorder=recorder),
        audio_loader=M4aAudioLoader(save_dir=save_dir),
        tts_api=tts_api,
    )
    assistant.run()


if __name__ == "__main__":
    main()
