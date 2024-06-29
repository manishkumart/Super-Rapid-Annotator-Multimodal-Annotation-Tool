import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class ModelLoader:
    _model = None
    _tokenizer = None
    _pipe = None

    @classmethod
    def load_model(cls, model_path):
        if cls._model is None or cls._tokenizer is None:
            cls._model = AutoModelForCausalLM.from_pretrained(
                model_path,
                device_map="cuda",
                torch_dtype="auto",
                trust_remote_code=True,
            )
            cls._tokenizer = AutoTokenizer.from_pretrained(model_path)
            cls._pipe = pipeline(
                "text-generation",
                model=cls._model,
                tokenizer=cls._tokenizer,
            )
        return cls._pipe
