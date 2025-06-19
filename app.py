# app.py
from flask import Flask, render_template_string
import os

# Initialize the Flask application
app = Flask(__name__)

# Basic HTML template for the web page
# This template will display the greeting message and an image
# retrieved from environment variables, populated by Azure Key Vault.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure App with Blob Image</title>
    <!-- Tailwind CSS CDN for basic styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for the app */
        body {
            font-family: 'Inter', sans-serif; /* Using Inter font */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh; /* Full viewport height */
            background-color: #f0f4f8; /* Light background color */
            color: #334155; /* Default text color */
        }
        .container {
            background-color: #ffffff; /* White container background */
            padding: 2.5rem; /* Ample padding */
            border-radius: 1rem; /* Rounded corners for the container */
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* Soft shadow */
            text-align: center; /* Center align text */
            max-width: 90%; /* Max width for responsiveness */
            width: 700px; /* Fixed width for larger screens */
        }
        h1 {
            color: #1e293b; /* Darker heading color */
            margin-bottom: 1.5rem; /* Space below heading */
            font-weight: 800; /* Extra bold */
            font-size: 2.5rem; /* Larger font size */
        }
        p {
            color: #475569; /* Paragraph text color */
            line-height: 1.6; /* Improved readability */
            font-size: 1.25rem; /* Larger paragraph font */
            font-style: italic; /* Italic for the greeting */
            margin-bottom: 1rem;
        }
        .image-container {
            margin-top: 2rem;
            background-color: #e2e8f0;
            padding: 1rem;
            border-radius: 0.5rem;
            display: inline-block; /* To contain the image well */
        }
        .fetched-image {
            max-width: 100%; /* Ensure image is responsive */
            height: auto; /* Maintain aspect ratio */
            border-radius: 0.5rem; /* Rounded corners for the image */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* Subtle shadow */
            object-fit: contain; /* Ensure the image fits within its bounds */
            max-height: 400px; /* Limit height for larger images */
        }
        .image-label {
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: block;
        }
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .container {
                width: 95%; /* Adjust width for smaller screens */
                padding: 1.5rem;
            }
            h1 {
                font-size: 2rem;
            }
            p {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Secure App!</h1>
        <p>"{{ greeting_message }}"</p>

        <div class="image-container">
            <span class="image-label">Your Secure Image from Blob Storage:</span>
            {% if image_url %}
                <img src="{{ image_url }}" alt="Image from Secure Blob Storage" class="fetched-image">
            {% else %}
                <p class="text-red-500">Image URL could not be constructed. Check environment variables.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """
    Renders the home page of the application.
    It retrieves 'GREETING_MESSAGE', 'BLOB_STORAGE_URL', and 'BLOB_SAS_TOKEN'
    from environment variables.
    It then constructs the full URL for the image using the base URL and SAS token.
    """
    # Attempt to retrieve the greeting message from environment variables.
    greeting_message = os.environ.get('GREETING_MESSAGE', 'Default Message: Greeting not configured or loaded.')
    
    # Retrieve the base Blob Storage URL and the SAS token.
    blob_storage_url = os.environ.get('BLOB_STORAGE_URL')
    blob_sas_token = os.environ.get('BLOB_SAS_TOKEN')
    
    image_url = None
    if blob_storage_url and blob_sas_token:
        # Construct the full image URL by appending the SAS token.
        
        image_url = f"{blob_storage_url}?{blob_sas_token}"
    
    # Render the HTML template, passing the greeting message and the constructed image URL.
    return render_template_string(HTML_TEMPLATE, 
                                  greeting_message=greeting_message,
                                  image_url=image_url)

if __name__ == '__main__':
    # Run the Flask application for local development.
    # The host '0.0.0.0' makes the app accessible from any IP address.
    # The port is taken from the 'PORT' environment variable if available, otherwise defaults to 5000.
    # debug=True enables debugging features but should be set to False in production.
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
