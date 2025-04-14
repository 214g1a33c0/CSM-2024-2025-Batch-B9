from flask import Flask, render_template, jsonify, request
from isl_translator.isl_translator_complete import translate_text_to_sign
import  io, base64, re,os,requests
from googletrans import Translator
from PIL import Image
import numpy as np
import azure.cognitiveservices.speech as speechsdk
import uuid
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
app = Flask(__name__)


# Azure Speech Service configuration
API_KEY = "vFqRoqGUdqgh1zFbSd6vMQARp1CW5xPvO5mvpVrDajSBLsIyYhliJQQJ99BCACYeBjFXJ3w3AAAYACOGggm4"
REGION = "eastus"

#Image configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load Azure credentials from environment variables
Imagesubscription_key = '4NcomHCOmMiz4S3uRGnu2pOXHtDeqUrk2AGVru079QD6cPhWgFDiJQQJ99BCACYeBjFXJ3w3AAAFACOG18F0'
Imageendpoint = 'https://ocrisl.cognitiveservices.azure.com/'

# Initialize Azure Computer Vision client
credentials = CognitiveServicesCredentials(Imagesubscription_key)
client = ComputerVisionClient(Imageendpoint, credentials)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/voice_to_sign')
def voice_to_sign():
    return render_template('voice_to_sign.html')

@app.route('/voice_to_text')
def voice_to_text():
    return render_template('voice_to_text.html')

@app.route('/text_to_sign')
def text_to_sign():
    return render_template('text_to_sign.html')

@app.route('/image_to_sign',methods=['GET', 'POST'])
def image_to_text():
    image_src = None
    extracted_text = None
    message = None

    if request.method == 'POST':
        file = request.files.get('file')
        url = request.form.get('url')

        # Process uploaded file
        if file and file.filename != '':
            # Generate a unique filename
            unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            image_src = f'/{app.config["UPLOAD_FOLDER"]}/{unique_filename}'

            try:
                with open(file_path, 'rb') as image_stream:
                    ocr_result = client.recognize_printed_text_in_stream(
                        image_stream, language='en', detect_orientation=True
                    )
                if ocr_result.regions:
                    extracted_text = extract_text_from_ocr_result(ocr_result)
                else:
                    message = "No text detected in the image."
            except Exception as e:
                message = f"Error processing image: {str(e)}"

        # Process image URL
        elif url:
            image_src = url
            try:
                ocr_result = client.recognize_printed_text(
                    url, language='en', detect_orientation=True
                )
                if ocr_result.regions:
                    extracted_text = extract_text_from_ocr_result(ocr_result)
                else:
                    message = "No text detected in the image."
            except Exception as e:
                message = f"Error processing URL: {str(e)}"

        # Handle case where neither file nor URL is provided
        else:
            message = "Please provide an image file or URL."

    # Render the template with results
    return render_template(
        'image_to_sign.html',
        image_src=image_src,
        extracted_text=extracted_text,
        message=message
    )


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input_text = data.get('text', '')
    output_paths = translate_text_to_sign(input_text)
    
    
    print("Generated paths:", output_paths)
    
    images_html = ''.join([
        f'<img src="/static/{path}" alt="ISL Sign" >'
        for path in output_paths
    ])
    
    return jsonify({'html': images_html})




@app.route('/get-token', methods=['GET'])
def get_token():
    url = f"https://{REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        token = response.text
        return jsonify({"token": token, "region": REGION})
    else:
        return jsonify({"error": "Failed to fetch token"}), 500
    



# Function to extract text from OCR result
def extract_text_from_ocr_result(ocr_result):
    extracted_text = []
    for region in ocr_result.regions:
        for line in region.lines:
            line_text = ' '.join([word.text for word in line.words])
            extracted_text.append(line_text)
    return '\n'.join(extracted_text)

# Main route for handling GET and POST requests



if __name__ == '__main__':
    app.run(debug=True)