# Persona System Frontend

A Streamlit-based frontend for the Persona Generation and Chat system.

## Features

### 🧠 Persona Generator
- Interactive chat interface for generating personas
- Model selection dropdown (GPT-5, GPT-4o) 
- Real-time persona generation with structured output
- Persona registration with custom naming
- Chat history with formatted persona display

### 💬 Persona Chat
- Chat with saved personas in character
- Model and parameter selection (temperature, top-p)
- Streaming responses for real-time conversation
- Persona information display
- Chat history management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key in a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
streamlit run app.py
```

Or use the run script:
```bash
python run.py
```

## Usage

1. **Home Page**: Navigate between the persona generator and chat interfaces
2. **Persona Generator**: 
   - Select your preferred model
   - Enter prompts to generate personas
   - Review the structured persona output
   - Register personas with custom names
3. **Persona Chat**:
   - Select a saved persona from the dropdown
   - Configure model parameters
   - Chat with the persona in character

## File Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `run.py` - Simple run script
- `README.md` - This file

## Notes

- Personas are saved as YAML files in the `personas/` directory, you can directly modify them or create new personas if you like
- The system uses OpenAI's structured output feature for persona generation
- Streaming is implemented for real-time chat responses for the persona chat, but it is not supported for persona generation
