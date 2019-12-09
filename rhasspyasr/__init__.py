"""Classes for automated speech recognition."""
from abc import ABC, abstractmethod
import typing

import attr


@attr.s
class Transcription:
    """Result of speech to text."""

    # Final transcription text
    text: str = attr.ib()

    # Likelihood of transcription 0-1, 1 being sure
    likelihood: float = attr.ib()

    # Seconds it took to do transcription
    transcribe_seconds: float = attr.ib()

    # Duration of the transcribed WAV audio
    wav_seconds: float = attr.ib()


class Transcriber(ABC):
    """Base class for Kaldi transcribers."""

    @abstractmethod
    def transcribe_wav(self, wav_data: bytes) -> typing.Optional[Transcription]:
        """Speech to text from WAV data."""
        pass
