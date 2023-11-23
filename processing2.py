#the provided text file appears to be a plain text 
#extraction from a PDF document, likely a form or 
# application with various sections such as general information, r
# isk assessment, claims & insurance history, and declarations. H
# owever, this text extraction doesn't contain the actual radio b
# uttons (or checkboxes) typically found in forms. Instead, it incl
# udes placeholders or annotations where these radio buttons might
# have been in the original PDF.

# Analyzing radio buttons in a PDF can be challenging due to several factors:

# Non-Textual Elements: Radio buttons are graphical elements, not text. 
# Text extraction tools often ignore these non-textual components or 
# treat them as images, making it hard to interpret their state (checked 
                                                               
# or unchecked) from a text-only perspective.
import fitz  # PyMuPDF
from PIL import Image
import json

pdf_path =  r'C:\Users\raeme\Onedrive\Documents\Career\1Club\projpt2\lockapp.pdf'

def pdf_to_images(pdf_path, output_json):
    pdf_document = fitz.open(pdf_path)
    images_data = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        
        # Convert PDF page to image
        image = page.get_pixmap()
        image_path = f"page_{page_number + 1}.png"
        image.save(image_path)

        # Add image information to the list
        images_data.append({"page": page_number + 1, "image_path": image_path})

    pdf_document.close()

    # Create pairs of images for each page
    pairs = []
    for i in range(0, len(images_data), 2):
        image1_info = images_data[i]
        pair = {"image1": image1_info["image_path"]}
        
        # Check if there is another image to add to the pair
        if i + 1 < len(images_data):
            image2_info = images_data[i + 1]
            pair["image2"] = image2_info["image_path"]
        
        pairs.append(pair)

    # Save pairs information to JSON file
    with open(output_json, 'w') as json_file:
        json.dump(pairs, json_file, indent=2)

    return pairs

output_json = "output_images.json"  # Replace with your desired JSON output file path

result_pairs = pdf_to_images(pdf_path, output_json)
print("JSON output:", json.dumps(result_pairs, indent=2))

import requests

def ocr_image(image_path):
    # Tesseract OCR API endpoint
    api_url = "https://api.ocr.space/parse/image"

    # ctual API key from OCR.space
    api_key = 'your_api_key'

    # Set up the request headers
    headers = {'apikey': api_key}

    # Read the image file
    with open(image_path, 'rb') as image_file:
        files = {'file': (image_path, image_file, 'image/png')}
        
        # Make a POST request to the OCR API
        response = requests.post(api_url, headers=headers, files=files)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            return result['ParsedResults'][0]['ParsedText']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

# Example usage
image_path = ""
result_text = ocr_image(image_path)

if result_text:
    print("OCR Result:")
    print(result_text)
