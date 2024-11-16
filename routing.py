import math
import os
import folium
import geojson
import numpy as np
import openrouteservice
from shapely.geometry import LineString, Point
from dotenv import load_dotenv


def load_api_key():
    """Load the OpenRouteService API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")
    if not api_key:
        raise EnvironmentError("OpenRouteService API key is not set.")
    return api_key


def get_directions(client, coords, profile="foot-walking"):
    """
    Fetch directions between two points using OpenRouteService.

    Args:
        client (openrouteservice.Client): OpenRouteService client instance.
        coords (list): List of [longitude, latitude] coordinate pairs.
        profile (str): Routing profile (e.g., "foot-walking", "driving-car").

    Returns:
        dict: GeoJSON result from the OpenRouteService directions API.
    """
    return client.directions(
        coordinates=coords, profile=profile, format="geojson", geometry=True, units="m"
    )


def calculate_heading(point1, point2):
    """
    Calculate the heading (bearing) between two geographical points.

    Args:
        point1 (tuple): (longitude, latitude) of the first point.
        point2 (tuple): (longitude, latitude) of the second point.

    Returns:
        int: Heading in degrees (1 to 360), where 0 is North and 180 is South.
    """
    lon1, lat1 = math.radians(point1[0]), math.radians(point1[1])
    lon2, lat2 = math.radians(point2[0]), math.radians(point2[1])

    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)

    initial_bearing = math.atan2(x, y)
    compass_bearing = (math.degrees(initial_bearing) + 360) % 360

    # Convert to integer and ensure 1 to 360 (inclusive)
    return int(round(compass_bearing)) if round(compass_bearing) > 0 else 360


def interpolate_points(line, num_points=100):
    """
    Interpolate evenly spaced points along a LineString.

    Args:
        line (LineString): Shapely LineString geometry.
        num_points (int): Number of points to interpolate.

    Returns:
        list: List of Shapely Point objects representing interpolated points.
    """
    spacing_distance = line.length / num_points
    distances_on_line = np.arange(0, 1, spacing_distance / line.length)
    return [line.interpolate(distance, normalized=True) for distance in distances_on_line]


def calculate_headings(spaced_points):
    """
    Calculate heading directions for a list of evenly spaced points.

    Args:
        spaced_points (list): List of Shapely Point objects.

    Returns:
        list: List of dictionaries with point coordinates and heading.
    """
    heading_data = [
        {
            "coordinates": [spaced_points[i].x, spaced_points[i].y],
            "heading": calculate_heading(
                (spaced_points[i].x, spaced_points[i].y),
                (spaced_points[i + 1].x, spaced_points[i + 1].y),
            ),
        }
        for i in range(len(spaced_points) - 1)
    ]
    # Add the last point with no heading
    heading_data.append(
        {
            "coordinates": [spaced_points[-1].x, spaced_points[-1].y],
            "heading": None,
        }
    )
    return heading_data


def save_geojson(data, file_name):
    """
    Save data to a GeoJSON file.

    Args:
        data (dict or geojson.FeatureCollection): Data to save.
        file_name (str): File name for saving the GeoJSON file.
    """
    with open(file_name, "w") as f:
        geojson.dump(data, f)
    print(f"GeoJSON saved to '{file_name}'")


def create_map(start_location, end_location, directions_result, spaced_points, output_file):
    """
    Create a Folium map with the route and interpolated points.

    Args:
        start_location (list): Starting location [latitude, longitude].
        end_location (list): Destination location [latitude, longitude].
        directions_result (dict): GeoJSON result of the route.
        spaced_points (list): List of Shapely Point objects.
        output_file (str): File name for saving the map as HTML.
    """
    m = folium.Map(location=start_location, zoom_start=15)

    # Add the original LineString to the map
    folium.GeoJson(directions_result).add_to(m)

    # Add markers for the interpolated points
    for point in spaced_points:
        folium.Marker(location=[point.y, point.x], tooltip="Interpolated Point").add_to(m)

    # Add markers for the starting and destination locations
    folium.Marker(location=start_location, tooltip="Start").add_to(m)
    folium.Marker(location=end_location, tooltip="Destination").add_to(m)

    # Save the map to an HTML file
    m.save(output_file)
    print(f"Map saved to '{output_file}'")


def main():
    # Load API key
    api_key = load_api_key()

    # Define coordinates and initialize the client
    STARTING_LOCATION = [42.356280, -71.062290]  # [latitude, longitude]
    DESTINATION_LOCATION = [42.35155, -71.05818]  # [latitude, longitude]
    coords = [[-71.062290, 42.356280], [-71.05818, 42.35155]]  # [longitude, latitude]
    client = openrouteservice.Client(key=api_key)

    # Get directions
    directions_result = get_directions(client, coords)

    # Extract the LineString and interpolate points
    line = LineString(directions_result["features"][0]["geometry"]["coordinates"])
    spaced_points = interpolate_points(line)

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


if __name__ == "__main__":
    main()