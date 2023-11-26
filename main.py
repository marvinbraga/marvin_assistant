import os

from assistants.voice_assistant import VoiceAssistant
from audio.basics import AudioRecorder
from audio.m4a_loaders import M4aAudioLoader
from audio.m4a_recorders import M4aRecorder


def main():
    recorder = M4aRecorder()
    save_dir = os.path.dirname(recorder.COMMAND_OUTPUT_FILENAME)
    # Inicializando o assistente.
    assistant = VoiceAssistant(
        audio_recorder=AudioRecorder(recorder=recorder),
        audio_loader=M4aAudioLoader(save_dir=save_dir)
    )
    assistant.run()


if __name__ == "__main__":
    main()
