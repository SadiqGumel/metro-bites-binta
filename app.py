import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIError

# Page Configuration
st.set_page_config(
    page_title="Metro Bites Kano — Binta",
    page_icon="🍲",
    layout="centered"
)

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize client using Groq's OpenAI-compatible endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

MODEL_NAME = "openai/gpt-oss-120b"

# Metro Bites Kano System Prompt
BINTA_SYSTEM_MESSAGE = """
You are Binta, the warm, polite, and efficient AI customer assistant for Metro Bites Kano, a modern takeout restaurant in Nassarawa GRA, Kano.

BUSINESS DETAILS:
- Location: Nassarawa GRA, Kano
- Delivery Areas: Nassarawa, Fagge, and Tarauni ONLY. Never confirm delivery anywhere else.
- Hours: Monday–Saturday: 10:00 AM – 10:00 PM | Sunday: 12:00 PM – 9:00 PM
- Currency: Nigerian Naira (₦)

APPROVED MENU & PRICES:
- Jollof rice with chicken: ₦2,800
- Fried rice with turkey: ₦3,500
- Grilled chicken with chips: ₦3,200
- Chicken shawarma: ₦1,800
- Beef burger with fries: ₦2,500
- Tuwon shinkafa with miyan taushe: ₦2,000
- Small chops pack: ₦1,500

CORE OPERATIONAL RULES:
1. Grounding: Quote prices strictly from the menu above in Naira (₦). Never invent dishes, alter prices, or promise deliveries outside our three designated delivery areas.
2. Safety & Scope: Never give health, medical, or dietary advice (e.g., regarding diabetes or allergies). Politely redirect customer attention back to ordering from Metro Bites Kano.
3. Uncertainty Escalation: If a customer asks a question you do not know or requests a custom meal, say exactly:
   "I'm not entirely certain about that, but let me connect you with a member of our restaurant team right away!"
"""

# Initialize session state for chat and usage telemetry
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# Sidebar with business context and telemetry
with st.sidebar:
    st.header("Metro Bites Kano")
    st.caption("📍 Nassarawa GRA, Kano")
    st.markdown("**Delivery Zones:** Nassarawa, Fagge, Tarauni")
    st.markdown("**Opening Hours:**")
    st.text("Mon–Sat: 10:00 AM – 10:00 PM\nSun: 12:00 PM – 9:00 PM")
    
    st.divider()
    st.subheader("Telemetry (Role 1)")
    st.metric(label="Cumulative Tokens Used", value=st.session_state.total_tokens)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🍲 Metro Bites Kano")
st.caption("Chat with Binta — Customer Service Assistant")

# Display previous conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt input
if prompt := st.chat_input("Ask about our menu, prices, or delivery..."):
    # Append user prompt to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare complete payload with system message
    api_messages = [{"role": "system", "content": BINTA_SYSTEM_MESSAGE}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=api_messages,
                temperature=0.2
            )
            bot_reply = response.choices[0].message.content
            
            # Log telemetry
            if response.usage:
                st.session_state.total_tokens += response.usage.total_tokens

            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except AuthenticationError:
            error_msg = "⚠️ Authentication failed. Check your GROQ_API_KEY in .env."
            message_placeholder.markdown(error_msg)
        except RateLimitError:
            error_msg = "⚠️ Rate limit exceeded. Please wait a moment before trying again."
            message_placeholder.markdown(error_msg)
        except APIError as e:
            error_msg = f"⚠️ Groq API Error: {str(e)}"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            error_msg = f"⚠️ Unexpected error: {str(e)}"
            message_placeholder.markdown(error_msg)