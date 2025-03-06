import streamlit as st
from typing import List, Dict, Optional
import json
from pilotingpromptpro import PilotingPromptPro

def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pilot" not in st.session_state:
        st.session_state.pilot = PilotingPromptPro()
    if "awaiting_clarification" not in st.session_state:
        st.session_state.awaiting_clarification = False
    if "original_request" not in st.session_state:
        st.session_state.original_request = ""
    if "intent_analysis" not in st.session_state:
        st.session_state.intent_analysis = {}
    if "clarification_responses" not in st.session_state:
        st.session_state.clarification_responses = {}
    if "last_optimized_prompt" not in st.session_state:
        st.session_state.last_optimized_prompt = ""
    if "show_execute_button" not in st.session_state:
        st.session_state.show_execute_button = False

def display_chat_messages() -> None:
    """
    Display all messages in the chat history.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_message(role: str, content: str) -> None:
    """
    Add a message to the chat history and display it.
    
    Args:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The content of the message
    """
    st.session_state.messages.append({"role": role, "content": content})
    
def process_user_message(user_message: str) -> None:
    """
    Process a user message and get the appropriate response.
    
    Args:
        user_message (str): The message from the user
    """
    # Add user message to chat and display it immediately
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Clear any previous clarification state if this is a new request
    if not st.session_state.awaiting_clarification:
        st.session_state.original_request = user_message
        st.session_state.clarification_responses = {}
    
    # Display thinking indicator in a separate assistant message
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("🤔 Thinking...")
        
        # Process the input
        if st.session_state.awaiting_clarification:
            # Store the clarification response
            questions = st.session_state.intent_analysis.get("clarification_questions", [])
            if questions:
                st.session_state.clarification_responses[questions[0]] = user_message
            
            # Get response with clarifications
            response, _, needs_clarification = st.session_state.pilot.process_input(
                st.session_state.original_request, 
                st.session_state.clarification_responses
            )
            
            # Reset clarification state
            st.session_state.awaiting_clarification = False
        else:
            # Get initial response
            response, intent_analysis, needs_clarification = st.session_state.pilot.process_input(user_message)
            st.session_state.intent_analysis = intent_analysis
            st.session_state.awaiting_clarification = needs_clarification
            
            # Extract the optimized prompt if present
            if not needs_clarification and "```" in response:
                prompt_start = response.find("```") + 3
                prompt_end = response.find("```", prompt_start)
                if prompt_start > 3 and prompt_end > prompt_start:
                    st.session_state.last_optimized_prompt = response[prompt_start:prompt_end].strip()
                    st.session_state.show_execute_button = True
                    
            # Check if there's an error message in the response
            if "system error occurred" in response.lower() or "isn't your fault" in response.lower():
                # Add a more prominent apology for system errors
                response = "⚠️ " + response
        
        # Display the response
        thinking_placeholder.empty()
        st.markdown(response)
    
    # Add assistant message to chat history
    add_message("assistant", response)

def execute_optimized_prompt() -> None:
    """
    Execute the last optimized prompt and display the result.
    """
    with st.chat_message("assistant"):
        execution_placeholder = st.empty()
        execution_placeholder.markdown("⚙️ Executing your optimized prompt...")
        
        try:
            # Execute the prompt with a timeout
            response = st.session_state.pilot.execute_prompt(st.session_state.last_optimized_prompt)
            
            if response:
                execution_placeholder.empty()
                st.markdown("### AI Response to Your Optimized Prompt")
                st.markdown(response)
                
                # Add execution result to chat history
                add_message("assistant", f"### AI Response to Your Optimized Prompt\n\n{response}")
            else:
                execution_placeholder.markdown("⚠️ Error executing your prompt. Please try again.")
                
        except Exception as e:
            execution_placeholder.markdown(f"⚠️ Error: {str(e)}. Please try again or modify your prompt.")
    
    # Hide the execute button after use
    st.session_state.show_execute_button = False

def main():
    # Page configuration
    st.set_page_config(
        page_title="Piloting Prompt Pro",
        page_icon="✈️",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("✈️ Piloting Prompt Pro")
    if not st.session_state.messages:
        st.write("""
        Welcome to Piloting Prompt Pro! I'll help transform your simple requests into optimized prompts for AI systems.
        Just tell me what you're trying to accomplish, and I'll do the prompt engineering for you.
        """)
    
    # Sidebar with information
    with st.sidebar:
        st.header("About Piloting Prompt Pro")
        st.write("""
        Piloting Prompt Pro is an automated prompt engineering assistant that helps you get better results from AI systems.
        
        Instead of worrying about how to phrase your prompts, just tell Piloting Prompt Pro what you're trying to accomplish, 
        and it will create an optimized prompt for you.
        """)
        
        st.header("How it works")
        st.write("""
        1. **You provide a goal** - Tell Piloting Prompt Pro what you want to achieve
        2. **Clarification (if needed)** - Piloting Prompt Pro might ask follow-up questions to create a better prompt
        3. **Get your optimized prompt** - Piloting Prompt Pro generates an expertly crafted prompt
        4. **Execute the prompt** - See the results of your optimized prompt
        """)
        
        st.header("Example Requests")
        st.write("""
        Try asking:
        - "Help me write a persuasive email to my team about a new initiative"
        - "I need to create a data visualization of sales trends"
        - "Create a character for my fantasy novel"
        """)
        
        # Add a clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.awaiting_clarification = False
            st.session_state.original_request = ""
            st.session_state.intent_analysis = {}
            st.session_state.clarification_responses = {}
            st.session_state.last_optimized_prompt = ""
            st.session_state.show_execute_button = False
            st.rerun()
    
    # Display chat interface
    display_chat_messages()
    
    # Display execute button if an optimized prompt is available
    if st.session_state.show_execute_button:
        col1, col2 = st.columns([3, 1])
        with col2:
            st.button("Execute This Prompt", on_click=execute_optimized_prompt, type="primary")
        with col1:
            st.info("👆 Click to see what the AI would generate with your optimized prompt", icon="ℹ️")
    
    # Chat input
    user_input = st.chat_input("What do you want AI to help you with?")
    if user_input:
        process_user_message(user_input)

if __name__ == "__main__":
    main()