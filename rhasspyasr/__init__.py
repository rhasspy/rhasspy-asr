"""Classes for automated speech recognition."""
import typing
from abc import ABC, abstractmethod

import attr


@attr.s(auto_attribs=True, slots=True)
class Transcription:
    """Result of speech to text."""

    # Final transcription text
    text: str

    # Likelihood of transcription 0-1, 1 being sure
    likelihood: float

    # Seconds it took to do transcription
    transcribe_seconds: float

    # Duration of the transcribed WAV audio
    wav_seconds: float


class Transcriber(ABC):
    """Base class for speech to text transcribers."""

    @abstractmethod
    def transcribe_wav(self, wav_data: bytes) -> typing.Optional[Transcription]:
        """Speech to text from WAV data."""

    @abstractmethod
    def transcribe_stream(
        self,
        audio_stream: typing.Iterable[bytes],
        sample_rate: int,
        sample_width: int,
        channels: int,
    ) -> typing.Optional[Transcription]:
        """Speech to text from an audio stream."""

    @abstractmethod
    def stop(self):
        """Stop the transcriber."""
