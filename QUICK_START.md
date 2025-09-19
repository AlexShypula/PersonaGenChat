# 🎭 Persona System - Quick Start Guide

## 🚀 Super Easy Setup (3 Steps!)

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
HUGGINGFACE_HUB_TOKEN=your_hf_token_here
```
(Replace with your actual keys)

### Step 3: Start the App
**Choose your method:**

#### 🖱️ **Easiest: Double-Click Method**
- **Windows**: Double-click `start_personas.bat`
- **Mac**: 
  - **Option 1**: Double-click `start_personas.command` (opens Terminal)
  - **Option 2**: Run `python create_mac_app.py` then double-click "Persona System.app"
  - **Option 3**: Double-click `start_personas.py` (if Python is set as default)
- **Linux**: Double-click `start_personas.sh`
- **Any OS**: Run `python start_personas.py`

#### 🖥️ **Desktop Shortcut**
1. Run: `python create_desktop_shortcut.py`
2. Double-click the shortcut on your desktop

#### 💻 **Command Line** (if you prefer)
```bash
cd frontend
streamlit run app.py
```

## 🎉 That's It!

Your browser should open automatically to `http://localhost:8501`

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

## 🎭 How to Use

1. **Home Page**: Choose between Persona Generator or Persona Chat
2. **Persona Generator**: Create detailed AI personas for research
3. **Persona Chat**: Chat with your saved personas
4. **Save Personas**: Register personas to use them later in chat

## 💡 Tips

- Start with the Persona Generator to create some personas
- Save interesting personas with memorable names
- Use the chat feature to test your personas
- Try different models to see which works best for your use case

---

**Need Help?** Check the main README.md or create an issue on GitHub!
