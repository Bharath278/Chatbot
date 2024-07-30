import os
import base64
import streamlit as st
import requests
import json
api_key ="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"

from groq import Groq

client = Groq(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": "You are an helpful AI chatbot"}]
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


# Replace with your actual Bland AI API key
BLAND_AI_API_KEY = "0NMsT3lBn1aKBnmSCNQH3vuyhmsqsz6B"

def make_call(phone_number, script):
    url = "https://api.bland.ai/v1/calls"
    headers = {
        "Authorization": f"Bearer {BLAND_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "phone_number": phone_number,
        "task": script,
        "voice": "male-1",  # You can change this to other available voices
        "reduce_latency": True,
        "record": True
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def get_call_status(call_id):
    url = f"https://api.bland.ai/v1/calls/{call_id}"
    headers = {
        "Authorization": f"Bearer {BLAND_AI_API_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_call(call_id):
    url = f"https://api.bland.ai/v1/calls/{call_id}/analyze"
    headers = {
        "Authorization": f"Bearer {BLAND_AI_API_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

# Example usage
phone_number = "+1234567890"
script = "Hello, this is an AI assistant. How may I help you today?"

# Make a call
call_response = make_call(phone_number, script)
if "id" in call_response:
    call_id = call_response["id"]
    print(f"Call initiated with ID: {call_id}")

    # Check call status
    status = get_call_status(call_id)
    print(f"Call status: {status['status']}")

    # Analyze the call (after it's completed)
    analysis = analyze_call(call_id)
    print("Call analysis:", json.dumps(analysis, indent=2))
else:
    print("Failed to initiate call. Response:", call_response)
