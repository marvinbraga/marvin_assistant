import os
from typing import Iterable

import openai
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import BlobLoader, FileSystemBlobLoader, Blob, YoutubeLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


class M4aAudioLoader(BlobLoader):

    def __init__(self, save_dir: str):
        self.save_dir = save_dir

    def yield_blobs(self) -> Iterable[Blob]:
        loader = FileSystemBlobLoader(self.save_dir, glob="*.m4a")
        for blob in loader.yield_blobs():
            yield blob


class AudioTranscript:
    def __init__(self, audio_filename):
        self._audio_filename = audio_filename
        self._docs = None

    @property
    def docs(self):
        return self._docs

    def execute(self):
        blob_loader = M4aAudioLoader(self._audio_filename)
        parser = OpenAIWhisperParser()

        loader = GenericLoader(blob_loader, parser)
        try:
            self._docs = loader.load()
        except Exception as e:
            print(f"Error: {e}")
        return self
