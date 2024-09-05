from pprint import pprint
from functools import partial
from geopy.geocoders import Nominatim

# Initialize the geolocator with a user-agent
geolocator = Nominatim(user_agent="myGeoVergil")

# Define a partial function to specify the language
geocode = partial(geolocator.geocode, language="en")


def get_place_bounds(place_name):
    # Geocode the place
    location = geocode(place_name)

    if location is None:
        raise Exception("No location found for the given place name.")

    # Extract bounding box details
    bbox = location.raw.get("boundingbox")

    if bbox is None:
        raise Exception(
            "No bounding box information available for the given place name."
        )

    # Convert bounding box coordinates to float
    min_latitude = float(bbox[0])
    max_latitude = float(bbox[1])
    min_longitude = float(bbox[2])
    max_longitude = float(bbox[3])

    return {
        "min_latitude": min_latitude,
        "max_latitude": max_latitude,
        "min_longitude": min_longitude,
        "max_longitude": max_longitude,
    }


def main(place_name="varanasi"):
    # Get the bounds
    bounds = get_place_bounds(place_name)

    # Print the results
    print("Min Latitude:", bounds["min_latitude"])
    print("Max Latitude:", bounds["max_latitude"])
    print("Min Longitude:", bounds["min_longitude"])
    print("Max Longitude:", bounds["max_longitude"])

    # Optionally print raw location data
    location = geolocator.geocode(place_name).raw
    pprint(location)

    return (
        bounds["min_latitude"],
        bounds["max_latitude"],
        bounds["min_longitude"],
        bounds["max_longitude"],
    )


if __name__ == "__main__":
    # Call main function with default value
    main()
