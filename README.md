# Pokemon AI OCR Renamer

This script uses OpenAI's GPT-4o model to rename images of Pokémon trading cards based on their contents. The script processes images in a specified directory, submits them to the OpenAI API for identification, and renames the files based on the card name and series.

## Features

- Automatically detects and processes images in the `Import` folder.
- Submits each image to OpenAI for identification.
- Renames images based on the identified card name and series.
- Logs errors and key steps in the process to `Log.txt`.

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)

## Setup

1. Download the script file.
2. Ensure you have an OpenAI API key and create the following tcg.cfg in the same directory as the script:
   ```
   <config>
    <api_key>your-api-key-here</api_key>
   </config>
3. Create an Import folder in the same directory as the script and place the images you want to process in this folder.

## Usage
Run the script:

`python Pokemon_TCG_OCR.py`

The script will process all images in the Import folder, rename them, and log the process.
The console will display the renaming steps and prompt you to press Enter to exit when processing is complete.

## Error Handling
If the Import folder is not found, the script will display an error message and exit.
If no image files are found in the Import folder, the script will display an error message and exit.
All errors encountered during processing are logged to Log.txt.

## Example
Given an image test.jpg in the Import folder, if the card is identified as "Pikachu" from the "Base Set 2" series, the file will be renamed to Pikachu - Base Set 2.jpg.

## Contributing
Feel free to submit issues or pull requests if you have suggestions for improvements or find any bugs.

## License
This project is licensed under the MIT License.
