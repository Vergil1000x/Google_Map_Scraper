from geopy.geocoders import Nominatim
from functools import partial

# Initialize the geocoder
geolocator = Nominatim(user_agent="myGeoVergil")

# Define partial functions to specify the language for geocoding
geocode = partial(geolocator.geocode, language="en")
reverse_geocode = partial(geolocator.reverse, language="en")


def validate_location(lat, lon, place_name):
    try:
        # Perform reverse geocoding to get the address of the coordinate
        reverse_location = reverse_geocode((lat, lon))

        if reverse_location:
            # Check if the place name is part of the reverse geocoded address
            if place_name.lower() in reverse_location.address.lower():
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        return False


def main(place_name, latitude, longitude):
    if validate_location(latitude, longitude, place_name):
        return True
    else:
        return False


if __name__ == "__main__":
    # This block will only run if this file is executed directly
    import sys

    if len(sys.argv) == 4:
        result = main(sys.argv[1], sys.argv[2], sys.argv[3])
        print(result)
    else:
        print("Please provide two integer arguments.")
