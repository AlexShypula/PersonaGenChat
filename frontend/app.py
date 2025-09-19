import streamlit as st
import sys
import os
import time

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from llm import PersonaGenerator, PersonaActor, BaseLLM, MODELS
from utils import Persona

# Page configuration
st.set_page_config(
    page_title="Persona System",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'persona_generator' not in st.session_state:
    st.session_state.persona_generator = None
if 'persona_actor' not in st.session_state:
    st.session_state.persona_actor = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'generator_history' not in st.session_state:
    st.session_state.generator_history = []

def main():
    st.title("🎭 Persona System")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
        if st.button("🧠 Persona Generator", use_container_width=True):
            st.session_state.page = 'generator'
        if st.button("💬 Persona Chat", use_container_width=True):
            st.session_state.page = 'chat'
    
    # Route to appropriate page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'generator':
        show_persona_generator()
    elif st.session_state.page == 'chat':
        show_persona_chat()

def show_home():
    st.header("Welcome to the Persona System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Persona Generator")
        st.write("Create realistic personas for customer research using AI. Generate detailed character profiles with professional, personal, and lifestyle attributes.")
        if st.button("Go to Persona Generator", key="home_generator", use_container_width=True):
            st.session_state.page = 'generator'
            st.rerun()
    
    with col2:
        st.subheader("💬 Persona Chat")
        st.write("Chat with your created personas! Select any saved persona and have realistic conversations for market research and user testing.")
        if st.button("Go to Persona Chat", key="home_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()

def show_persona_generator():
    st.header("🧠 Persona Generator")
    
    # Model selection
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_model = st.selectbox(
            "Select Model",
            MODELS,
            index=1,  # Default to gpt-4o-mini
            key="generator_model"
        )
    
    with col2:
        if st.button("Reset Chat", key="reset_generator"):
            st.session_state.persona_generator = None
            st.session_state.generator_history = []
            st.rerun()
    
    # Initialize generator if needed
    if st.session_state.persona_generator is None or st.session_state.persona_generator.llm_model != selected_model:
        with st.spinner("Initializing persona generator..."):
            try:
                st.session_state.persona_generator = PersonaGenerator(llm_model=selected_model)
                if not st.session_state.generator_history:
                    st.success("Persona generator initialized!")
            except Exception as e:
                st.error(f"Failed to initialize generator: {str(e)}")
                return
    
    # Display chat history
    for i, (prompt, response, persona) in enumerate(st.session_state.generator_history):
        with st.container():
            st.markdown(f"**User:** {prompt}")
            st.markdown(f"**Assistant:** {response}")
            
            # Format and display the persona
            st.subheader("Generated Persona:")
            persona_dict = persona.model_dump()
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Core Persona:**", persona_dict.get('persona', 'N/A'))
                st.write("**Professional:**", persona_dict.get('professional_persona', 'N/A'))
                st.write("**Sports:**", persona_dict.get('sports_persona', 'N/A'))
                st.write("**Arts:**", persona_dict.get('arts_persona', 'N/A'))
            
            with col2:
                st.write("**Travel:**", persona_dict.get('travel_persona', 'N/A'))
                st.write("**Culinary:**", persona_dict.get('culinary_persona', 'N/A'))
                st.write("**Skills:**", persona_dict.get('skills_and_expertise', 'N/A'))
                st.write("**Career Goals:**", persona_dict.get('career_goals_and_ambitions', 'N/A'))
            
            # Skills and interests lists
            if persona_dict.get('skills_and_expertise_list'):
                st.write("**Skills List:**", ", ".join(persona_dict['skills_and_expertise_list']))
            if persona_dict.get('hobbies_and_interests_list'):
                st.write("**Interests List:**", ", ".join(persona_dict['hobbies_and_interests_list']))
            if persona_dict.get('hobbies_and_interests'):
                st.write("**Hobbies & Interests:**", persona_dict['hobbies_and_interests'])
            
            # Registration section - make it more prominent
            st.markdown("---")
            st.subheader("💾 Save This Persona")
            st.markdown("**Want to chat with this persona later?** Save it to use in the Persona Chat feature!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                persona_name = st.text_input(
                    f"Give your persona a name (optional)", 
                    key=f"name_{i}", 
                    placeholder="e.g., 'Marketing_Mike' or leave empty for auto-generated name",
                    help="This name will help you identify the persona in the chat interface"
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                if st.button(f"💾 Save Persona", key=f"register_{i}", type="primary", use_container_width=True):
                    try:
                        # Set the last persona to the one we want to register
                        st.session_state.persona_generator.last_persona = persona
                        persona_id = st.session_state.persona_generator.register_last_persona(persona_name if persona_name else None)
                        st.success(f"✅ Persona saved as: **{persona_id}**")
                        st.info("💬 You can now find this persona in the **Persona Chat** section!")
                    except Exception as e:
                        st.error(f"❌ Failed to save persona: {str(e)}")
            
            st.divider()
    
    # Input for new prompt - change text based on whether we have history
    with st.form("generator_form"):
        if st.session_state.generator_history:
            # After first turn - encourage iteration
            prompt_label = "Iterate on your persona or create a new one:"
            prompt_placeholder = "e.g., 'Make them more extroverted and add cooking skills' or 'Generate a completely different persona: a retired teacher who loves gardening'"
            button_text = "Iterate/Generate"
        else:
            # First turn - initial generation
            prompt_label = "Enter your persona generation prompt:"
            prompt_placeholder = "e.g., 'Generate a tech-savvy millennial who works in marketing and loves outdoor activities'"
            button_text = "Generate Persona"
        
        prompt = st.text_area(
            prompt_label,
            placeholder=prompt_placeholder,
            height=100
        )
        submitted = st.form_submit_button(button_text)
        
        if submitted and prompt:
            if st.session_state.persona_generator is None:
                st.error("Persona generator not initialized. Please wait and try again.")
                return
            
            # Show loading state
            with st.spinner("Waiting on LLM response... this can take a while (up to1-2 minutes)"):
                try:
                    response, persona = st.session_state.persona_generator.generate_persona(prompt, selected_model)
                    st.session_state.generator_history.append((prompt, response, persona))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating persona: {str(e)}")

def show_persona_chat():
    st.header("💬 Persona Chat")
    
    # Get available personas
    base_llm = BaseLLM()
    try:
        available_personas = base_llm.get_all_personas()
    except:
        available_personas = []
    
    if not available_personas:
        st.warning("No personas found. Please create some personas first using the Persona Generator.")
        return
    
    # Settings sidebar
    with st.sidebar:
        st.subheader("Chat Settings")
        
        # Persona selection
        selected_persona_file = st.selectbox(
            "Select Persona",
            available_personas,
            key="chat_persona"
        )
        
        # Model settings
        selected_model = st.selectbox(
            "Select Model",
            MODELS,
            index=1,
            key="chat_model"
        )
        
        
        if st.button("Reset Chat", key="reset_chat"):
            st.session_state.persona_actor = None
            st.session_state.chat_history = []
            st.rerun()
    
    # Initialize persona actor
    if (st.session_state.persona_actor is None or 
        st.session_state.persona_actor.llm_model != selected_model or
        st.session_state.persona_actor.persona_id != selected_persona_file):
        
        try:
            with st.spinner("Loading persona..."):
                persona_id = selected_persona_file.replace('.yaml', '')
                persona = base_llm.load_persona(persona_id)
                st.session_state.persona_actor = PersonaActor(
                    persona=persona,
                    persona_id=persona_id,
                    llm_model=selected_model
                )
                st.success(f"Loaded persona: {persona_id}")
        except Exception as e:
            st.error(f"Failed to load persona: {str(e)}")
            return
    
    # Display persona info
    if st.session_state.persona_actor:
        with st.expander("Current Persona Info"):
            persona_dict = st.session_state.persona_actor.persona.model_dump()
            st.write("**Core Persona:**", persona_dict.get('persona', 'N/A'))
            st.write("**Professional:**", persona_dict.get('professional_persona', 'N/A'))
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and stream response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Stream the response
                for chunk in st.session_state.persona_actor.stream_conversation_turn(prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
