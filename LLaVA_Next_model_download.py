from transformers import BitsAndBytesConfig, LlavaNextVideoForConditionalGeneration, LlavaNextVideoProcessor
import torch

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-DPO-hf", cache_dir='/home/manish/final/LLaVA-NeXT-Video-7B-DPO-hf')
model = LlavaNextVideoForConditionalGeneration.from_pretrained(
    "llava-hf/LLaVA-NeXT-Video-7B-DPO-hf",
    quantization_config=quantization_config,
    device_map='auto',
    cache_dir='/home/manish/final/LLaVA-NeXT-Video-7B-DPO-hf'
    
)