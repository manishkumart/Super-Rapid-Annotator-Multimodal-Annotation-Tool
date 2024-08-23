# Importing the requirements
import torch
from transformers import AutoModel, AutoTokenizer
import spaces
from src.utils import encode_video


# Device for the model
device = "cuda"

# Load the model and tokenizer
model = AutoModel.from_pretrained(
    "openbmb/MiniCPM-V-2_6",
    trust_remote_code=True,
    attn_implementation="sdpa",
    torch_dtype=torch.bfloat16,
)
model = model.to(device=device)
tokenizer = AutoTokenizer.from_pretrained(
    "openbmb/MiniCPM-V-2_6", trust_remote_code=True
)
model.eval()


# @spaces.GPU(duration=20)
def describe_video(video, question):
    """
    Describes a video by generating an answer to a given question.

    Args:
        - video (str): The path to the video file.
        - question (str): The question to be answered about the video.

    Returns:
        str: The generated answer to the question.
    """
    # Encode the video frames
    frames = encode_video(video)

    # Message format for the model
    msgs = [{"role": "user", "content": frames + [question]}]

    # Set decode params for video
    params = {
        "use_image_id": False,
        "max_slice_nums": 1,  # Use 1 if CUDA OOM and video resolution > 448*448
    }

    # Generate the answer
    answer = model.chat(
        image=None,
        msgs=msgs,
        tokenizer=tokenizer,
        sampling=True,
        stream=True,
        top_p=0.8,
        top_k=100,
        temperature=0.7,
        repetition_penalty=1.05,
        max_new_tokens=2048,
        system_prompt="You are an AI assistant specialized in visual content analysis. Given a video and a related question, analyze the video thoroughly and provide a precise and informative answer based on the visible content. Ensure your response is clear, accurate, and directly addresses the question.",
        **params
    )

    # Return the answer
    return "".join(answer)
