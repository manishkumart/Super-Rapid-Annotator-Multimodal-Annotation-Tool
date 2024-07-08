import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from pydantic import BaseModel
import json
import warnings
from fastapi import FastAPI
from typing import Dict

# Ignore warnings
warnings.filterwarnings(action='ignore')

# Set random seed
torch.random.manual_seed(0)

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

generation_args = {
    "max_new_tokens": 50,
    "return_full_text": False,
    "temperature": 0.1,
    "do_sample": True
}

class LLMHelper:
    def __init__(self, pipeline):
        self.chatbot = pipeline

    def generate_logic(self, llm_output: str):
        prompt = f"""
        Provide the response in json string for the below keys and context based on the description: '{llm_output}'.
        
        Screen.interaction_yes: This field indicates whether there was an interaction of the person with a screen during the activity. A value of 1 means there was screen interaction (Yes), and a value of 0 means there was no screen interaction (No).
        Hands.free: This field indicates whether the person's hands were free during the activity. A value of 1 means the person was not holding anything (Yes), indicating free hands. A value of 0 means the person was holding something (No), indicating the hands were not free.
        Indoors: This field indicates whether the activity took place indoors. A value of 1 means the activity occurred inside a building or enclosed space (Yes), and a value of 0 means the activity took place outside (No).
        Standing: This field indicates whether the person was standing during the activity. A value of 1 means the person was standing (Yes), and a value of 0 means the person was not standing (No).
        """

        messages = [
            {"role": "system", "content": "Please answer questions just based on this information: " + llm_output},
            {"role": "user", "content": prompt},
        ]

        response = self.chatbot(messages, **generation_args)
        generated_text = response[0]['generated_text']
        # Extract JSON from the generated text
        start_index = generated_text.find('{')
        end_index = generated_text.rfind('}') + 1
        json_str = generated_text[start_index:end_index]
        return json_str

class VideoAnalysis(BaseModel):
    screen_interaction_yes: int
    hands_free: int
    indoors: int
    standing: int

    @classmethod
    def from_llm_output(cls, llm_output: str, generated_logic: str) -> 'VideoAnalysis':
        # Parse the generated logic (assuming it's a JSON string)
        logic_dict = json.loads(generated_logic)
        
        return cls(
            screen_interaction_yes=logic_dict.get("Screen.interaction_yes", 0),
            hands_free=logic_dict.get("Hands.free", 0),
            indoors=logic_dict.get("Indoors", 0),
            standing=logic_dict.get("Standing", 0)
        )

# Define the model path
model_path = "model_path"

# Load the model and pipeline
pipe = ModelLoader.load_model(model_path)
llm_helper = LLMHelper(pipe)

# Initialize FastAPI
app = FastAPI()

class LLMInput(BaseModel):
    llm_output: str

@app.post("/process_llm_output/")
def process_llm_output(input: LLMInput) -> Dict:
    # Generate the logic from the LLM output
    generated_logic = llm_helper.generate_logic(input.llm_output)
    
    # Create the structured output
    structured_output = VideoAnalysis.from_llm_output(input.llm_output, generated_logic)
    
    # Return the structured output as a dictionary
    return structured_output.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200)


