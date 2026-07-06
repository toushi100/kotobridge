import torch
import whisper

class Model:
    def __init__(self, model_name: str="large-v3-turbo"):
        self.model_name = model_name
        self.model = None
        


    def load_model(self):
        self.device = self.detect_device()
        print(f"Using device: {self.device}")
        self.model = whisper.load_model(self.model_name, device=self.device)
        print(f"Model Name: {self.model_name}")
        return self.model

    def detect_device(self):
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"