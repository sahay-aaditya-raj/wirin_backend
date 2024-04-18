import geocoder
import webbrowser


def get_current_location() -> dict :
    g = geocoder.ip('me')

    if g.latlng:
        latitude, longitude = g.latlng
        return {"lat":latitude, "long":longitude}
    else:
        return {}


def generate_url(destination: str) -> str:
    destination = destination.replace(" ","+")
    coordinates = get_current_location()
    if coordinates:
        return f"https://www.google.com/maps/dir/?api=1&origin={coordinates['lat']},{coordinates['long']}&destination={destination}&travelmode=driving"
    else:
        return ""


def open_url() -> None:
    webbrowser.open(generate_url("Majestic Metro Station, Bengaluru"))


if __name__ == '__main__':
    open_url()
