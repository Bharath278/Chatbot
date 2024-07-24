import os
import base64
import streamlit as st
import requests
api_key ="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"

from groq import Groq

client = Groq(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": "You are an helpful AI chatbot for my bakery which sells cakes and customer calls you to enquire about the price . Prices are chesscake-100 rupee venilla cake-200 raspberry cake-300 . Respond to queries with short sentences"}]
    messages = system_message + messages
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    answer = ""
    for chunk in completion:
        answer += (chunk.choices[0].delta.content or "")

    return answer

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        response_format="verbose_json",
        )
        print(transcription.text)
    return transcription.text

def text_to_speech(input_text):
    # response = client.audio.speech.create(
    #     model="tts-1",
    #     voice="nova",
    #     input=input_text
    # )
    webm_file_path = "temp_audio_play.mp3"
    # with open(webm_file_path, "wb") as f:
    #     response.stream_to_file(webm_file_path)
    # return webm_file_path
    # Define the API endpoint
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
    # Set your Deepgram API key
    api_key = "d0bb2feaed19db16d51f005d35a79cb5c97801df"
    # Define the headers
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "text": input_text
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
    # Save the response content to a file
        with open(webm_file_path, "wb") as f:
            f.write(response.content)
        return webm_file_path
    else:
        print(f"Error: {response.status_code} - {response.text}")

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)