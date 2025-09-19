# Persona Generator and Chat - Quick Start Guide

Create a persona in the format of [Nemotron Personas](https://huggingface.co/datasets/nvidia/Nemotron-Personas) with ChatGPT, modify it / iterate on it, save it, and chat with it.

### Step 1: Get Your API Keys

#### OpenAI API Key
1. Go to [OpenAI's website](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-...`)


#### Hugging Face Token
1. Go to [Hugging Face tokens page](https://huggingface.co/settings/tokens)
2. Sign up or log in
3. Click "New token"
4. Choose **"Read"** permission (sufficient for this app)
5. Copy the token (starts with `hf_...`)

### Step 2: Set Up Your API Keys
Create a file called `.env` in this folder and add:
```
OPENAI_API_KEY=your_openai_key_here
HF_TOKEN=your_hf_token_here
```
(Replace with your actual keys)

### Step 3: Start the App
**Choose your method:**

#### 🖱️ **Easiest: Double-Click Method**
- **Windows**: Double-click `start_personas.bat`
- **Mac**: 
  - **Option 1**: Run `python create_mac_app.py` then double-click "Persona System.app"
  - **Option 2**: Double-click `start_personas.py` (if Python is set as default)
  - **Option 3**: Open Terminal and run `bash start_personas.sh`
- **Linux**: Double-click `start_personas.sh`
- **Any OS**: Run `python start_personas.py`

**Note** you do not need to give your email to streamlit when it prompts you with ```If you'd like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank.```

<!-- #### 🖥️ **Desktop Shortcut**
1. Run: `python create_desktop_shortcut.py`
2. Double-click the shortcut on your desktop -->

#### 💻 **Command Line** (if you prefer)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## 🎉 That's It!

Your browser should open automatically to `http://localhost:8501`

If not, try to open up that in your browser. On the first time you run it, it may take a minute or two to download the NemoTron personas dataset, and each time you try to create a new persona there will be some latency to wait for OpenAI to generate a new persona for you. 

## 🆘 Troubleshooting

### "Python not found"
- Install Python from [python.org](https://python.org)
- Make sure to check "Add to PATH" during installation

### "Module not found" errors
The launcher scripts will automatically install required packages, but if you get errors:
```bash
pip install -r frontend/requirements.txt
```

### API Key Issues
- Make sure your `.env` file is in the main project folder (same level as this README)
- Check that your API key is correct and has credits
- The key should start with `sk-`

### Port Already in Use
If you get a port error, try:
```bash
streamlit run app.py --server.port 8502
```

## 🎭 Complete Workflow: From Creation to Chat

### Phase 1: Creating Your First Persona 🧠

1. **Start the App**: Use any method above to launch the system
2. **Navigate to Persona Generator**: Click "🧠 Persona Generator" from the home page
3. **Choose Your Model**: Select from available models (gpt-5, gpt4o, etc..) 
4. **Create Initial Persona**: Enter a prompt describing a high-level persona in your target audience / target stakeholder group:
   ```
   Generate a persona of a procurement decision maker at a major retailer like Costco
   ```
5. **Review the Generated Persona**: The system creates a detailed persona with:
   - Core personality traits
   - Professional background
   - Sports/fitness interests
   - Arts and culture preferences
   - Travel style
   - Culinary tastes
   - Skills and expertise
   - Career goals and ambitions
   - Structured lists of interests and skills

### Phase 2: Iterating and Refining 🔄

6. **Iterate on Your Persona**: After the first generation, the prompt changes to allow iteration:
   ```
   Make them more 10 years older and more conservative in their outloook.
   ```
   Or create variations:
   ```
   Keep the marketing background and make them more in touch with the Gen-Z demographic 
   ```
7. **Multiple Iterations**: Keep refining until you get one or more personas you are happy with.

### Phase 3: Saving Your Persona 💾

9. **Save When Ready**: Once you're happy with a persona, use the save section:
   - Give it a name: you will load it later for the chat feature
   - You can leave blank for auto-generated name
   - Click "💾 Save Persona"
10. **Confirmation**: You'll see "✅ Persona saved as: [name]" and guidance to find it in Persona Chat

11. **Note on Generating Multiple Personas** The persona generator only remembers the most recently proposed persona. If you like it, save it. Note as well that creating more personas is not mutually exclusive: after you save a persona, you can continue to ask ChatGPT to continue iterating on it until you get a new persona that you are happy with.

### Phase 4: Chatting with Your Persona 💬

11. **Navigate to Persona Chat**: Click "💬 Persona Chat" from the home page
12. **Select Your Persona**: Choose from the dropdown of saved personas
13. **Configure Chat Settings**:
    - Choose your preferred model
    - Adjust temperature for creativity level
14. **Start Chatting**: Begin conversations however you like! 
    
15. **Realistic Responses**: The persona is instructed to respond in character, drawing from their detailed background. They are also instructed to be realistic, but of course take it with a grain of salt. 

### Phase 5: Advanced Usage 🚀

16. **Create Multiple Personas**: Build a library for different research needs:
    - Different stakeholders
    - Various industries 
17. **A/B Testing**: Compare how different personas respond to the same questions
18. **Market Research**: Use personas to test product ideas, marketing messages, or user experiences
19. **Iterative Improvement**: If you want to make fine-grained improvements / changes to personas, you can directly modify them in /frontend/personas and add/delete the text. You can also copy that back into the persona generator if you want to use that as a beginning for new personas.

## 🎯 Example Complete Workflow

**Goal**: Create a persona for testing a new fitness app

1. **Generate**: "Create a busy working parent interested in fitness but struggling with time"
2. **Iterate**: "Make them more tech-savvy and add experience with fitness apps"
3. **Refine**: "Add that they prefer home workouts due to childcare constraints"
4. **Save**: Name it "Busy_Parent_Fitness"
5. **Chat**: Test questions about the fitness app:
   - "What's your biggest challenge with staying fit?"
   - "How do you currently track your workouts?"
   - "What would make you choose one fitness app over another?"


**Need Help?** Try to create an issue on GitHub.
