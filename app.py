import os
import re

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from api.weather import get_weather


# -----------------------------
# Load environment variables
# -----------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Check Hugging Face token
# -----------------------------

if not HF_TOKEN:
    st.error("Hugging Face token not found. Check your .env file.")
    st.stop()


# -----------------------------
# Hugging Face client
# -----------------------------

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)


# -----------------------------
# Nova UI
# -----------------------------

st.title("🤖 Nova AI")
st.caption("Your intelligent AI assistant with real-time weather")


# -----------------------------
# Chat history
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Detect weather questions
# -----------------------------

def is_weather_question(text):

    weather_words = [
        "weather",
        "temperature",
        "rain",
        "raining",
        "forecast",
        "climate",
        "humidity",
        "wind"
    ]

    text = text.lower()

    return any(word in text for word in weather_words)


# -----------------------------
# Extract city from question
# -----------------------------

def extract_city(text):

    patterns = [
        r"weather in ([a-zA-Z\s]+)",
        r"temperature in ([a-zA-Z\s]+)",
        r"weather at ([a-zA-Z\s]+)",
        r"temperature at ([a-zA-Z\s]+)",
        r"forecast for ([a-zA-Z\s]+)"
    ]

    text = text.lower()

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            city = match.group(1).strip()

            # Remove common words if included
            city = re.sub(
                r"\b(today|tomorrow|now|please)\b",
                "",
                city
            ).strip()

            return city

    return None


# -----------------------------
# Chat input
# -----------------------------

user_input = st.chat_input(
    "Ask Nova anything..."
)


if user_input:

    # Show user message

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # -----------------------------
    # WEATHER API
    # -----------------------------

    if is_weather_question(user_input):

        city = extract_city(user_input)

        with st.chat_message("assistant"):

            if city:

                with st.spinner("Checking the weather..."):

                    try:

                        weather_result = get_weather(city)

                        st.markdown(weather_result)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": weather_result
                        })

                    except Exception as e:

                        error_message = (
                            "Sorry, I couldn't get the weather right now."
                        )

                        st.error(error_message)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_message
                        })

            else:

                message = (
                    "Please mention a city. For example: "
                    "**What's the weather in Chennai?**"
                )

                st.info(message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": message
                })


    # -----------------------------
    # NORMAL AI QUESTION
    # -----------------------------

    else:

        with st.chat_message("assistant"):

            with st.spinner("Nova is thinking..."):

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Nova, a helpful AI assistant. "
                                    "Give clear, accurate and simple answers. "
                                    "Help with programming, computer science, "
                                    "academics, projects and general questions."
                                )
                            },
                            *st.session_state.messages
                        ],
                        max_tokens=512,
                        temperature=0.7
                    )

                    answer = response.choices[0].message.content

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(f"AI Error: {e}")