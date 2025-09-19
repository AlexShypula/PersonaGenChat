from openai import OpenAI
from utils import Persona, PersonaChatResponse
from dotenv import load_dotenv
import os
from datetime import datetime
import yaml
import random
import uuid
from datasets import load_dataset 

load_dotenv()
assert os.getenv("OPENAI_API_KEY") is not None
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODELS = [
    "gpt-5", 
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4o-nano",
]


class BaseLLM: 
    
    def __init__(self, llm_model: str = "gpt-4o-mini"):
        self.llm_model = llm_model
        
    def load_persona(self, persona_id: str):
        with open(f"personas/{persona_id}.yaml", "r") as f:
            return Persona.model_validate(yaml.safe_load(f))
        
    def save_persona(self, persona: Persona, persona_id: str):
        with open(f"personas/{persona_id}.yaml", "w") as f:
            yaml.dump(persona.model_dump(), f)
            
    def get_all_personas(self):
        return [f for f in os.listdir("personas") if f.endswith(".yaml")]
    
    def get_persona_history(self, persona_id: str):
        with open(f"personas/{persona_id}.yaml", "r") as f:
            return yaml.safe_load(f)


class PersonaGenerator(BaseLLM): 
    
    def __init__(self, use_dataset: bool = True, n_example_personas: int = 3, llm_model: str = "gpt-4o-mini"): 
        super().__init__(llm_model)
        self.use_dataset = use_dataset
        self.dataset = load_dataset("nvidia/Nemotron-Personas")["train"] if use_dataset else None
        
        self.n_example_personas = n_example_personas
        assert self.dataset is not None, "Dataset is not loaded"
        assert self.n_example_personas > 0, "Number of example personas must be greater than 0"
        assert self.n_example_personas <= len(self.dataset), "Number of example personas must be less than or equal to the number of personas in the dataset"
        self.example_personas = self.sample_personas(self.n_example_personas)
        self.example_personas_str = "\n".join([f"Example Persona {i+1}: {self.format_persona(persona)}" for i, persona in enumerate(self.example_personas)])
        
        self.message_history = [{"role": "system", "content": f"You are an expert in persona generation. You generate highly realistic personas for customer research. At each iteration, you are expected to either generate from scratch or iterate on the previous persona. Here are the fields and some examples of personas we make: {self.example_personas_str}"}]
        self.last_persona = None
        
    def sample_personas(self, n: int = 3, seed: int = None):
        assert self.dataset is not None, "Dataset is not loaded"
        if seed is not None:
            random.seed(seed)
        indices = random.sample(range(len(self.dataset)), n)
        return [self.dataset[i] for i in indices]
    
    def format_persona(self, persona: dict):
        s = "" 
        for k, v in persona.items():
            s += f"{k}: {v}\n"
        return s
    
    def format_response(self, PersonaChatResponse: PersonaChatResponse):
        s = ""
        for k, v in PersonaChatResponse.model_dump().items():
            s += f"{k}: {v}\n"
        return s
    
    def generate_persona(self, prompt: str, override_openai_model: str = "gpt-4o-mini", n_example_personas: int = 3):
        
        if override_openai_model is not None:
            openai_model = override_openai_model
        else:
            openai_model = self.llm_model
        
        self.message_history.append({"role": "user", "content": prompt})
        response = client.responses.parse(
            model=openai_model,
            input=self.message_history,
            text_format=PersonaChatResponse,
        )
        parsed_response = response.output_parsed
        self.last_persona = parsed_response.persona_response
        self.message_history.append({"role": "assistant", "content": self.format_response(parsed_response)})
        
        return parsed_response.llm_response, parsed_response.persona_response
        
    
    def register_last_persona(self, persona_name: str = None): 
        if self.last_persona is None:
            raise ValueError("No persona to register")
        if persona_name is None:
            persona_name = f"persona_{str(uuid.uuid4())[:8]}"
        persona_id = f"{persona_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs("personas", exist_ok=True)
        with open(f"personas/{persona_id}.yaml", "w") as f:
            yaml.dump(self.last_persona.model_dump(), f)
        return persona_id
    
    # def load_persona(self, persona_id: str):
    #     with open(f"personas/{persona_id}.yaml", "r") as f:
    #         return Persona.model_validate(yaml.load(f))
    
    # def get_all_personas(self):
    #     return [f for f in os.listdir("personas") if f.endswith(".yaml")]
    


class PersonaActor: 
    
    def __init__(self, persona: Persona, persona_id: str = None, llm_model: str = "gpt-4o-mini"):
        self.persona = persona
        self.persona_id = persona_id
        self.llm_model = llm_model
        self.message_history = [{"role": "system", "content": f"This is your detailed persona:  {self.persona.model_dump_json()}. Act and respond as this persona realistically in consumer research discussions. Do not reveal that you are an AI model or that you are acting as this persona. Do not bias your responses to please the researcher. Try to be as realistic as possible in your responses."}]
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def conversation_turn(self, message: str):
        self.message_history.append({"role": "user", "content": message})
        response = self.client.responses.create(
            model=self.llm_model,
            input=self.message_history
        )
        # For Responses API, the response structure is different
        response_content = response.output[0].content[0].text if response.output else ""
        self.message_history.append({"role": "assistant", "content": response_content})
        return response_content
    
    def stream_conversation_turn(self, message: str):
        self.message_history.append({"role": "user", "content": message})
        stream = self.client.responses.create(
            model=self.llm_model,
            input=self.message_history,
            stream=True
        )
        assistant_response = ""
        for event in stream:
            # Handle different event types from the Responses API
            if hasattr(event, 'type'):
                if event.type == 'response.output_text.delta':
                    # This is where the text content comes from
                    if hasattr(event, 'delta') and event.delta:
                        content = event.delta
                        assistant_response += content
                        yield content
                elif event.type == 'response.completed':
                    # Response is complete
                    break
                elif event.type == 'error':
                    # Handle errors
                    raise Exception(f"Streaming error: {event}")
        self.message_history.append({"role": "assistant", "content": assistant_response})
        
    
    