
import torch
import whisper
from dataclasses import dataclass
@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str
class Translate:
    def __init__(self, path: str, target_language: str = "en",model: str = "whisper"):
        self.path = path
        self.target_language = target_language
        self.model = model


    def translate(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu" 
        self.device = "cuda" if torch.cuda.is_available() else self.device
        print(f"Using device: {self.device}")
        self.whisper = whisper.load_model("large-v3", device=self.device)
        result = self.whisper.transcribe(self.path,task="translate")
        print(f"Translated text: {result['text']}")
        print(f"Translated text: {result['language']}")
        raw_segments = result.get("segments", [])
        segments = [
        TranscriptSegment(
            start=float(segment["start"]),
            end=float(segment["end"]),
            text=str(segment["text"]),
        )
        for segment in raw_segments
    ]
        print(f"result keys: {result.keys()}")
        print(f"Segments: {segments}")
        return result