import easyocr
from PIL import Image
import io
import base64
import numpy as np
import re

def extract_text_from_image(image_data):
    # Decode the base64 image data
    image_data = image_data.split(",")[1]  # Remove the metadata part
    image_bytes = base64.b64decode(image_data)
    
    # Open the image using PIL
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert the image to RGB (easyocr requires RGB images)
    image = image.convert('RGB')
    
    # Convert the image to a numpy array
    image_np = np.array(image)
    
    # Use easyocr to extract text from the image
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_np)
    
    # Combine the text from the result
    extracted_text = ' '.join([text for _, text, _ in result])
    
    # Remove all special characters and symbols
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', extracted_text)
    
    return cleaned_text

# def test_extract_text_from_image():
#     # Load an image file
#     with open("isl_translator/ocr1.png", "rb") as image_file:
#         image_bytes = image_file.read()
    
#     # Encode the image to base64
#     image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#     image_data = f"data:image/png;base64,{image_base64}"
    
#     # Call the function to extract text
#     extracted_text = extract_text_from_image(image_data)
    
#     # Print the extracted text
#     print("Extracted Text:", extracted_text)
    
#     # Assert the extracted text (this is a placeholder, adjust as needed)
#     assert extracted_text is not None
#     assert len(extracted_text) > 0

# # Run the test
# if __name__ == "__main__":
#     test_extract_text_from_image()