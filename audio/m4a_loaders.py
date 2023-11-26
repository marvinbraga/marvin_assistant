from typing import Iterable

from langchain.document_loaders import BlobLoader, Blob, FileSystemBlobLoader


class M4aAudioLoader(BlobLoader):

    def __init__(self, save_dir: str):
        self.save_dir = save_dir

    def yield_blobs(self) -> Iterable[Blob]:
        loader = FileSystemBlobLoader(self.save_dir, glob="*.m4a")
        for blob in loader.yield_blobs():
            yield blob
