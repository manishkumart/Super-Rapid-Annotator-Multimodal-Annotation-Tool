import json
from pydantic import BaseModel

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
