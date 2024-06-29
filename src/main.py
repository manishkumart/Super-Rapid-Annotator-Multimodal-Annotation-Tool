import warnings
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from model_loader import ModelLoader
from llm_helper import LLMHelper
from video_analysis import VideoAnalysis

# Ignore warnings
warnings.filterwarnings(action='ignore')

# Define the model path
model_path = "MODEL_PATH"

# Load the model and pipeline
pipe = ModelLoader.load_model(model_path)
llm_helper = LLMHelper(pipe)

# Initialize FastAPI
SLLM_Output_app = FastAPI()

class LLMInput(BaseModel):
    llm_output: str

@SLLM_Output_app.post("/process_llm_output/")
def process_llm_output(input: LLMInput) -> Dict:
    # Generate the logic from the LLM output
    generated_logic = llm_helper.generate_logic(input.llm_output)
    
    # Create the structured output
    structured_output = VideoAnalysis.from_llm_output(input.llm_output, generated_logic)
    
    # Return the structured output as a dictionary
    return structured_output.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(SLLM_Output_app, host="0.0.0.0", port=8000)
