import kotobridge.model as model
from dataclasses import dataclass
@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str
class Translate:
    def __init__(self, path: str, target_language: str = "en", model_name: str = "large-v3"):
        self.path = path
        self.model = model.Model(model_name).load_model()


    def translate(self):
        result = self.model.transcribe(self.path, task="translate")
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