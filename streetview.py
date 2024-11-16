import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.getenv('MAPS_API')


def fetch_streetview(location, size, heading=None, pitch=None):
    
    if heading and pitch:
        street_view_url = (
            f"https://maps.googleapis.com/maps/api/streetview"
            f"?size={size}&location={location}&heading={heading}&pitch={pitch}&key={API_KEY}"
        )
    elif heading:
        street_view_url = (
            f"https://maps.googleapis.com/maps/api/streetview"
            f"?size={size}&location={location}&heading={heading}&key={API_KEY}"
        )
    elif pitch:
        street_view_url = (
            f"https://maps.googleapis.com/maps/api/streetview"
            f"?size={size}&location={location}&pitch={pitch}&key={API_KEY}"
        )
    else:
        street_view_url = (
            f"https://maps.googleapis.com/maps/api/streetview"
            f"?size={size}&location={location}&key={API_KEY}"
        )


    response = requests.get(street_view_url)

    if response.status_code == 200:
        img_bytes = response.content #This is a bytes object
        image_stream = BytesIO(img_bytes)
        image_pil = Image.open(image_stream)

        image = np.array(image_pil)
        return image     

    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    location = "42.299387, -71.262765" # Example: Statue of Liberty
    size = "640x640"  # Image size
    fetch_streetview(location, size)
