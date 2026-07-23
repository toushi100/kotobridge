from dataclasses import dataclass

import torch
import whisper
import psutil
from faster_whisper import WhisperModel
import mlx_whisper  as MLXWhisper

@dataclass(frozen=True)
class ModelType:
    FASTER_WHISPER = "faster-whisper"
    WHISPER = "whisper"
    MLX_WHISPER = "mlx-whisper"
class Model:
    def __init__(self, model_name: str="large-v3-turbo"):
        self.model_name = model_name
        self.model = None
        self.specs = {
            "device": None,
            "vram": None,
            "ram": None,
            "cpu": None
        }



    def load_model(self,type: ModelType = ModelType.FASTER_WHISPER):
        self.detect_system_specs()
        print(f"Using device: {self.specs['device']}")
        print(f"System VRAM: {self.specs['vram']}")
        print(f"System RAM: {self.specs['ram']}")
        print(f"System CPU: {self.specs['cpu']}")
        if type == ModelType.FASTER_WHISPER:
            return self.load_faster_whisper()
        elif type == ModelType.WHISPER:
            return self.load_whisper()
        elif type == ModelType.MLX_WHISPER:
            return self.load_mlx_whisper()
        else:
            raise ValueError(f"Invalid model type: {type}")

    def load_faster_whisper(self):
        self.model = WhisperModel(self.model_name, device=self.specs['device'], compute_type="float16")
        print(f"Model Name: {self.model_name}")
        return self.model
    
    def load_whisper(self):
        self.model = whisper.load_model(self.model_name, device=self.specs['device'])
        print(f"Model Name: {self.model_name}")
        return self.model

    def load_mlx_whisper(self):
        self.model = MLXWhisper
        print(f"Model Name: {self.model_name}")
        return self.model
    
    def detect_system_specs(self):
        self.specs = {
            "device": self.detect_device(),
            "vram": self.convert_bytes_to_gb(self.detect_system_vram()),
            "ram": self.convert_bytes_to_gb(self.detect_system_ram()),
            "cpu": self.detect_system_cpu()
        }
    def detect_device(self):
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    def detect_system_vram(self):
        if self.specs["device"] == None:
            self.specs["device"] = self.detect_device()
        if self.specs["device"] == "mps":
            return 0
        elif self.specs["device"] == "cuda":
            return torch.cuda.get_device_properties(0).total_memory
        else:
            return None
        
    def clear_cache(self):
        print(f"Clearing cache for device: {self.specs['device']}")
        if self.specs["device"] == "cuda":
            torch.cuda.empty_cache()
        elif self.specs["device"] == "mps":
            # MPS does not have a direct equivalent to empty_cache, but you can try to free up memory by deleting tensors and calling gc.collect()
            import gc
            gc.collect()
        else:
            pass  # No cache clearing needed for CPU

    def detect_system_ram(self):
        return psutil.virtual_memory().total
    
    def detect_system_cpu(self):
        return psutil.cpu_count(logical=True)
    
    def convert_bytes_to_gb(self, bytes_value):
        return round(bytes_value / (1024 ** 3), 2)