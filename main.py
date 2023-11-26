from assistants.voice_assistant import VoiceAssistant
from audio.basics import AudioRecorder
from audio.m4a_recorders import M4aRecorder


def main():
    assistant = VoiceAssistant(
        audio_recorder=AudioRecorder(recorder=M4aRecorder()),
    )
    assistant.run()


if __name__ == "__main__":
    main()
