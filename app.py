import streamlit as st
from gradio_client import Client
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CalmzAI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .stTitle {
            color: #2E4057;
            font-family: 'Helvetica Neue', sans-serif;
            margin-bottom: 2rem;
        }
        
        /* Chat container styling */
        .chat-container {
            background-color: #f5f7f9;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Message styling */
        .user-message {
            background-color: #2E4057;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 80%;
            float: right;
            clear: both;
            color: #FFFFFF;
        }
        
        .assistant-message {
            background-color: #E8F1F2;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 80%;
            float: left;
            clear: both;
            color: #1B1B1E;
        }
        
        /* Input box styling */
        .stTextInput {
            border-radius: 20px;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 20px;
            background-color: #2E4057;
            color: white;
            padding: 0.5rem 2rem;
            font-weight: 500;
        }
        
        .stButton>button:hover {
            background-color: #1a242f;
            border-color: #1a242f;
        }
        
        /* Footer styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f5f7f9;
            padding: 10px;
            text-align: center;
            font-size: 0.8rem;
            border-top: 1px solid #e1e4e8;
        }
        
        /* Timestamp styling */
        .timestamp {
            font-size: 0.7rem;
            color: #666;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Hugging Face client for CalmzAI
client = Client("Onoroyiza/Mixtral-chat")

# Initialize conversation history in Streamlit session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# App header with logo
st.title("🤖 CalmzAI Chat")
st.markdown("Welcome to the next generation of AI conversation! Your messages will be remembered within this session.")

# Sidebar with information
with st.sidebar:
    st.header("About CalmzAI")
    st.markdown("""
        CalmzAI is an advanced chatbot powered by the Mixtral model. 
        It can help you with:
        * General conversations
        * Questions and answers
        * Problem-solving
        * And much more!
    """)
    
    # Add usage statistics
    st.subheader("Session Stats")
    st.metric("Messages Sent", len([m for m in st.session_state.conversation_history if m["role"] == "user"]))
    st.metric("AI Responses", len([m for m in st.session_state.conversation_history if m["role"] == "assistant"]))

# Chat interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display the chat history with timestamps
for message in st.session_state.conversation_history:
    timestamp = datetime.now().strftime("%H:%M")
    if message["role"] == "user":
        st.markdown(
            f"""<div class='user-message'>
                {message['content']}
                <div class='timestamp'>{timestamp}</div>
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div class='assistant-message'>
                {message['content']}
                <div class='timestamp'>{timestamp}</div>
            </div>""",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# Input area
with st.container():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_message = st.text_input(
            "",
            placeholder="Type your message here...",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("Send 📤")

# Message processing
if send_button and user_message.strip():
    # Append user message to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_message})
    
    # Check if the user is asking about the creator
    if any(
        phrase in user_message.lower()
        for phrase in ["who created you", "your creator", "who made you", "made you", "created you", "built you", "build you", "what are you", "model are you", "AI are you"]
    ):
        predefined_response = "I was created by Calmz Data Nexus, a hub for innovative AI solutions!"
        st.session_state.conversation_history.append({"role": "assistant", "content": predefined_response})
    else:
        # Format the conversation history
        formatted_history = "\n".join(
            [
                f"User: {msg['content']}" if msg["role"] == "user" else f"CalmzAI: {msg['content']}"
                for msg in st.session_state.conversation_history
            ]
        )
        
        # Send to API with error handling
        try:
            with st.spinner("CalmzAI is thinking..."):
                result = client.predict(
                    message=formatted_history,
                    api_name="/chat"
                )
            st.session_state.conversation_history.append({"role": "assistant", "content": result})
        except Exception as e:
            st.error("Sorry, I couldn't process that request. Please try again.")
            st.error(f"Error details: {str(e)}")

# Footer
st.markdown(
    """
    <div class='footer'>
        Made with ❤️ by <a href='https://github.com/MrCalmz' target='_blank'>Calmz Data Nexus</a> | 
        <a href='https://github.com/MrCalmz' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Clear conversation button in sidebar
if st.sidebar.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.experimental_rerun()
