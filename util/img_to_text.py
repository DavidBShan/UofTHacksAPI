import base64
import requests
import os
import cohere
import time
from elevenlabs import generate, play, set_api_key, save, Voice, VoiceSettings

openai_api_key = os.environ["OPENAI_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]
elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]
set_api_key(elevenlabs_api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def get_image_description(image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What's in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def get_narraration(text):
    co = cohere.Client(cohere_api_key) # This is your trial API key
    response = co.generate(
    model='command',
    prompt=text + '\nMake a script in the tone of David attenborough regarding this image. The user wants to feel nostaligic. focus on quirky details. Just give me the story, no intro or closure.',
    max_tokens=500,
    temperature=1,
    k=0,
    stop_sequences=[],
    return_likelihoods='NONE')
    return ('Prediction: {}'.format(response.generations[0].text))

desc = get_image_description("IMG_5562.JPG")
narration = get_narraration(desc)

voice = generate(
    text=narration[12:],
    voice= Voice(
        voice_id = 'GEM8FZRZ0Q7qZPaI8pju',
        settings=VoiceSettings(stability=0.3, similarity_boost=0.5, style=0.25, use_speaker_boost=True)
    )
)
save(voice,'./audio/test.mp3')