from pydantic import BaseModel
import json

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
