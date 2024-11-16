import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np

load_dotenv()
API_KEY = os.getenv('MAPS_API')


def fetch_streetview(lat: float, long: float, img_size: tuple, heading=None, pitch=None) -> np.ndarray:

    if img_size[0] > 640 or img_size[1] > 640:
        print("The maximum image size is 640 x 640")
        return np.array([])

    location = f"{lat}, {long}"
    size = f"{img_size[0]}x{img_size[1]}"
    
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
        print("Image fetched successfully")
        return image     

    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return np.array([])


if __name__ == "__main__":
    lat = 42.299387
    long = -71.262765
    size = (640,640)  # Image size
    fetch_streetview(lat=lat,long=long,img_size=size)
