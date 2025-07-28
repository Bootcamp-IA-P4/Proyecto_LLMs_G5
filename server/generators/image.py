import os
import datetime
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import fal_client

# Load environment variables from .env file
load_dotenv()

def generate_image_fal_ai(
    topic: str,
    platform: str,
    voice: str,
    company_info: str = "",
    language: str = "en"
) -> str:
    """
    Generates an image using the fal.ai API.
    Saves the image to a file and returns its URL.
    """
    # Construct the prompt for fal.ai
    prompt = (
        f"Ultra-realistic, highly detailed illustration for {platform}. "
        f"Topic: {topic}. "
        f"Audience/Voice: {voice}. "
    )
    if company_info:
        prompt += f"Company info: {company_info}. "
    prompt += (
        "cinematic, sharp focus, 8k resolution, masterpiece, professional quality."
    )

    # Call fal.ai API
    handler = fal_client.submit(
        "fal-ai/flux/dev",
        arguments={"prompt": prompt},
    )
    result = handler.get()
    image_url_from_fal = result["images"][0]["url"]
    # Download the image from the URL provided by fal.ai
    image_response = requests.get(image_url_from_fal)
    image_response.raise_for_status()
    image = Image.open(BytesIO(image_response.content))

    # Define the directory to save images
    # This path is relative to the project root
    # We need to go up two directories from image.py (server/generators) to the project root,
    # then navigate to client/static/generated_images
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    output_dir = os.path.join(project_root, "client", "static", "generated_images")
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(output_dir, filename)

    # Save the image
    image.save(file_path)

    # Return the URL relative to the static files served by FastAPI
    # This URL is relative to the 'static' directory configured in FastAPI
    image_url = f"/static/generated_images/{filename}"
    return image_url