import torch
import whisper
import psutil
from faster_whisper import WhisperModel
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


    def load_model(self):
        self.detect_system_specs()
        print(f"Using device: {self.specs['device']}")
        print(f"System VRAM: {self.specs['vram']}")
        print(f"System RAM: {self.specs['ram']}")
        print(f"System CPU: {self.specs['cpu']}")

        self.model = whisper.load_model(self.model_name, device=self.specs['device'])
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
            return torch.backends.mps.get_device_properties(0).total_memory
        elif self.specs["device"] == "cuda":
            return torch.cuda.get_device_properties(0).total_memory
        else:
            return None

    def detect_system_ram(self):
        return psutil.virtual_memory().total
    
    def detect_system_cpu(self):
        return psutil.cpu_count(logical=True)
    
    def convert_bytes_to_gb(self, bytes_value):
        return round(bytes_value / (1024 ** 3), 2)