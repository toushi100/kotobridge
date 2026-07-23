from os import path

from .model import Model, ModelType
from dataclasses import dataclass
from ollama import Client

@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str

class Translate:
    def __init__(self, model_name: str = "large-v3", language: str = "auto"):
        self.model = Model(model_name)
        self.loaded_model = self.model.load_model(type=ModelType.MLX_WHISPER)

        # self.clear_cache = self.model.clear_cache()
        self.path = None

    def transcribe(self, path: str):
        self.path = path
        path_or_hf= 'mlx-community/whisper-large-v3-mlx'
        result = self.loaded_model.transcribe(
            path,
            path_or_hf_repo=path_or_hf,
            language="ja",
                fp16=False,
    verbose=True,
    temperature=0.0,
    # beam_size=5,
    # best_of=5,
    condition_on_previous_text=True,
    initial_prompt=(
        "Japanese anime subtitles. "
        "Dialogue between characters. "
        "Japanese names and honorifics such as -san, -kun, -sama, -chan. "
        "Senpai, Sensei."
    ),

                                    )
        
        print(f"Translated text: {result}")
        
        raw_segments = result.get("segments", [])
        segments = [
        TranscriptSegment(
            start=float(segment["start"]),
            end=float(segment["end"]),
            text=str(segment["text"]),
        )
        for segment in raw_segments
    ]
        
        transcription_output_path = self.path.replace(".mp4", ".ja.srt").replace(".mkv", ".ja.srt").replace(".avi", ".ja.srt")
        self.write_srt_file(segments, transcription_output_path)
        # self.clear_cache
        
        return result

    def format_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def write_srt_file(self, segments, transcription_output_path):
        with open(transcription_output_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments, start=1):
                start_time = self.format_time(segment.start)
                end_time = self.format_time(segment.end)
                srt_file.write(f"{i}\n{start_time} --> {end_time}\n{segment.text}\n\n")
                
        print(f"SRT file written to: {transcription_output_path}")

