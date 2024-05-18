import os
import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()  

# URL for the translation API
url = "https://api.sunbird.ai/tasks/nllb_translate"

# Retrieve the access token from environment variables
access_token = os.getenv("AUTH_TOKEN")
if not access_token:
    print("Error: Access token not found in environment variables. Please set AUTH_TOKEN in your .env file.")
    exit(1)

# Function to call the Sunbird AI translation endpoint
def translate_text(source_lang, target_lang, text):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "source_language": source_lang,
        "target_language": target_lang,
        "text": text,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for non-2xx responses
        response_json = response.json()
        translated_text = response_json['output']['data'].get('translated_text')
        return translated_text
    except requests.exceptions.RequestException as e:
        print("Error calling translation API:", e)
        return None
    except KeyError as e:
        print("Error parsing translation response:", e)
        return None

# Function to prompt user for input and handle translation
def translate():
    language_codes = {
        "English": "eng",
        "Luganda": "lug",
        "Runyankole": "nyn",
        "Acholi": "ach",
        "Ateso": "teo",
        "Lugbara": "lgg"
    }

    # Prompt for source language
    print("Please choose the source language: (one of English, Luganda, Runyankole, Ateso, Lugbara or Acholi)")
    source_lang = input("Your Input: ")

    # Prompt for target language
    print("Please choose the target language: (one of English, Luganda, Runyankole, Ateso, Lugbara or Acholi)")
    target_lang = input("Your Input: ")

    # Prompt for text to translate
    print("Enter the text to translate:")
    text = input("Your Input: ")

    # Ensure valid language selection
    if source_lang not in language_codes or target_lang not in language_codes:
        print("(your program): Invalid language selection. Please choose valid languages.")
        return

    # Ensure source and target languages are different
    if source_lang == target_lang:
        print("(your program): Source and target languages must be different.")
        return

    # Call the translation API using the translate_text function
    translated_text = translate_text(language_codes[source_lang], language_codes[target_lang], text)

    # Display the translated text
    if translated_text:
        print(f"Translation: {translated_text}")
    else:
        print("Translation: Translation failed.")

if __name__ == "__main__":
    translate()
