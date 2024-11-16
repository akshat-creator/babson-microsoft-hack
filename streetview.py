import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np
from routing import *

load_dotenv()
API_KEY = os.getenv('MAPS_API')


def fetch_streetview(lat: float, long: float, img_size: tuple, heading=None, pitch=None) -> np.ndarray:
    """
    Fetches a Street View image from the Google Maps API for a specified location and returns it as a NumPy array.

    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
        img_size (tuple): Tuple representing the image size (width, height) in pixels (max: 640x640).
        heading (int, optional): The heading angle of the camera (0 to 360 degrees). Defaults to None.
        pitch (int, optional): The pitch angle of the camera (-90 to 90 degrees). Defaults to None.

    Returns:
        np.ndarray: The fetched image as a NumPy array, or an empty array if the fetch fails.
    
    Raises:
        requests.exceptions.RequestException: If the API request fails or the status code is not 200.
    """
    if img_size[0] > 640 or img_size[1] > 640:
        print("The maximum image size is 640 x 640")
        return np.array([])

    location = f"{lat}, {long}"
    size = f"{img_size[0]}x{img_size[1]}"
    
    # Construct the URL based on available parameters
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
        img_bytes = response.content  # This is a bytes object
        image_stream = BytesIO(img_bytes)
        image_pil = Image.open(image_stream)
        image = np.array(image_pil)
        print("Image fetched successfully")
        return image

    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return np.array([])


def get_path_imgs(start: tuple, end: tuple, num_points=100) -> list:
    """
    Retrieves a series of Street View images along a route from the starting point to the destination.

    Args:
        start (tuple): A tuple representing the starting location (latitude, longitude).
        end (tuple): A tuple representing the destination location (latitude, longitude).
        interval (int, optional): Interval for selecting points along the route. Default is 1 (every point).

    Returns:
        list: A list of Street View images as NumPy arrays along the route.
    
    Raises:
        Exception: If the route directions cannot be fetched or processed.
    """
    ROUTE_API_KEY = load_api_key()
    path_imgs = []

    # Define coordinates and initialize the client
    STARTING_LOCATION = [start[0], start[1]]  # [latitude, longitude]
    DESTINATION_LOCATION = [end[0], end[1]]  # [latitude, longitude]
    coords = [STARTING_LOCATION[::-1], DESTINATION_LOCATION[::-1]]  # [longitude, latitude]
    client = openrouteservice.Client(key=ROUTE_API_KEY)

    # Get directions
    directions_result = get_directions(client, coords)

    # Extract the LineString and interpolate points
    line = LineString(directions_result["features"][0]["geometry"]["coordinates"])
    spaced_points = interpolate_points(line, num_points)

    # Calculate headings for spaced points
    spaced_points_heading = calculate_headings(spaced_points)

    # Save spaced points with headings as GeoJSON
    heading_geojson = geojson.FeatureCollection([
        geojson.Feature(
            properties={"heading": hd["heading"]},
            geometry=Point(hd["coordinates"])
        ) for hd in spaced_points_heading
    ])

    save_geojson(heading_geojson, "spaced_points_with_heading.geojson")
    # Create and save the map
    create_map(
        start_location=STARTING_LOCATION,
        end_location=DESTINATION_LOCATION,
        directions_result=directions_result,
        spaced_points=spaced_points,
        output_file="route_with_interpolated_points.html"
    )
    # Save the original route as GeoJSON
    save_geojson(directions_result, "route.geojson")

    print("Fetching streetview...")
    for point in heading_geojson['features']:
        coord = point['geometry']['coordinates']  # This is long-lat
        heading = point['properties']['heading']  # 1 - 360

        cur_pos_img = fetch_streetview(lat=coord[1], long=coord[0], img_size=(640, 640), heading=heading)
        path_imgs.append(cur_pos_img)

    return path_imgs


if __name__ == "__main__":
    start = (42.356280, -71.062290)
    end = (42.35155, -71.05818)

    get_path_imgs(start, end, num_points=50)
