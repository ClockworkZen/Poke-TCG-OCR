import base64
import requests
import json
import os
import re
import sys

# Function to read the API key from the configuration file
def read_api_key(config_file):
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found. Exiting...")
        input("Press Enter to exit...")
        sys.exit(1)
    
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('api_key'):
                return line.split('=')[1].strip()
    
    print(f"Error: API key not found in '{config_file}'. Exiting...")
    input("Press Enter to exit...")
    sys.exit(1)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to sanitize file names
def sanitize_filename(filename):
    filename = filename.replace('&', 'and')
    return re.sub(r'[^a-zA-Z0-9 \-_.]', '_', filename)

# Function to process and rename an image file
def process_image(image_path, api_key):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a Pokemon trading card game expert that responds in JSON."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please identify this card. Only return the name of the card, and the series its from."
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

    log_message = "Submitting picture for review..."
    print(log_message)
    with open("Log.txt", "a") as log_file:
        log_file.write(log_message + '\n')
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        
        try:
            content = response_data['choices'][0]['message']['content']
            # Parse the JSON content to extract the card name and series
            card_data = json.loads(content.strip('```json').strip('```'))
            card_name = card_data.get('name', '')
            series = card_data.get('series', '')

            if card_name and series:
                # Sanitize the new file name
                sanitized_name = sanitize_filename(f"{card_name} - {series}.jpg")
                # Rename the original image file in the same directory
                directory, original_file_name = os.path.split(image_path)
                new_image_path = os.path.join(directory, sanitized_name)
                os.rename(image_path, new_image_path)
                rename_message = f"Renamed '{original_file_name}' to '{os.path.basename(new_image_path)}'"
                print(rename_message)
                with open("Log.txt", "a") as log_file:
                    log_file.write(rename_message + '\n')
            else:
                error_message = "Failed to parse the response."
                print(error_message)
                with open("Log.txt", "a") as log_file:
                    log_file.write(error_message + '\n')
        except KeyError:
            error_message = f"Unexpected response format: {response_data}"
            print(error_message)
            with open("Log.txt", "a") as log_file:
                log_file.write(error_message + '\n')
        except json.JSONDecodeError:
            error_message = "Failed to decode the JSON response."
            print(error_message)
            with open("Log.txt", "a") as log_file:
                log_file.write(error_message + '\n')
    else:
        error_message = f"Request failed with status code {response.status_code}"
        print(error_message)
        with open("Log.txt", "a") as log_file:
            log_file.write(error_message + '\n')

def main():
    start_message = "Pokemon AI OCR Renamer is starting up..."
    print(start_message)
    with open("Log.txt", "a") as log_file:
        log_file.write(start_message + '\n')

    config_file = "tcg.cfg"
    api_key = read_api_key(config_file)
    
    import_folder = "Import"
    
    if not os.path.exists(import_folder):
        error_message = f"Error: '{import_folder}' folder not found. Exiting..."
        print(error_message)
        with open("Log.txt", "a") as log_file:
            log_file.write(error_message + '\n')
        input("Press Enter to exit...")
        sys.exit(1)
    
    image_files = [f for f in os.listdir(import_folder) if os.path.isfile(os.path.join(import_folder, f))]
    
    if not image_files:
        error_message = f"No image files found in '{import_folder}' folder. Exiting..."
        print(error_message)
        with open("Log.txt", "a") as log_file:
            log_file.write(error_message + '\n')
        input("Press Enter to exit...")
        sys.exit(1)
    
    for image_file in image_files:
        image_path = os.path.join(import_folder, image_file)
        process_image(image_path, api_key)
    
    completion_message = "Folder processing complete!"
    print(completion_message)
    with open("Log.txt", "a") as log_file:
        log_file.write(completion_message + '\n')
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
