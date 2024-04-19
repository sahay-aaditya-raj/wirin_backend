import requests
import math

def fetch_directions(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Return JSON data directly
        else:
            print(f"Error: Unable to fetch directions. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def calculate_distance(start_longitude, start_latitude, end_longitude, end_latitude):
    """
    Calculate the distance between two coordinates using the Haversine formula.
    """
    # Convert coordinates from degrees to radians
    start_longitude_rad = math.radians(start_longitude)
    start_latitude_rad = math.radians(start_latitude)
    end_longitude_rad = math.radians(end_longitude)
    end_latitude_rad = math.radians(end_latitude)

    # Haversine formula
    delta_longitude = end_longitude_rad - start_longitude_rad
    delta_latitude = end_latitude_rad - start_latitude_rad
    a = math.sin(delta_latitude / 2) ** 2 + math.cos(start_latitude_rad) * math.cos(end_latitude_rad) * math.sin(delta_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Radius of the Earth in kilometers
    distance = R * c

    return distance

def calculate_direction(start_longitude, start_latitude, end_longitude, end_latitude):
    """
    Calculate cardinal direction based on the coordinates.
    """
    # Calculate the differences in longitude and latitude
    delta_longitude = end_longitude - start_longitude
    delta_latitude = end_latitude - start_latitude

    # Determine cardinal direction for longitude
    if delta_longitude > 0:
        longitude_direction = "east"
    elif delta_longitude < 0:
        longitude_direction = "west"
    else:
        longitude_direction = ""

    # Determine cardinal direction for latitude
    if delta_latitude > 0:
        latitude_direction = "north"
    elif delta_latitude < 0:
        latitude_direction = "south"
    else:
        latitude_direction = ""

    # Combine longitude and latitude directions
    if longitude_direction and latitude_direction:
        direction = f"{latitude_direction}-{longitude_direction}"
    elif longitude_direction:
        direction = longitude_direction
    elif latitude_direction:
        direction = latitude_direction
    else:
        direction = "unknown"

    return direction

def calculate_angle(prev_coordinates, current_coordinates, next_coordinates):
    # Convert coordinates to radians
    prev_lon, prev_lat = math.radians(prev_coordinates[0]), math.radians(prev_coordinates[1])
    curr_lon, curr_lat = math.radians(current_coordinates[0]), math.radians(current_coordinates[1])
    next_lon, next_lat = math.radians(next_coordinates[0]), math.radians(next_coordinates[1])

    # Calculate vectors from the current coordinate to the previous and next coordinates
    x_prev = prev_lon - curr_lon
    y_prev = prev_lat - curr_lat
    x_next = next_lon - curr_lon
    y_next = next_lat - curr_lat

    # Calculate dot product and cross product of the vectors
    dot_product = x_prev * x_next + y_prev * y_next
    cross_product = x_prev * y_next - y_prev * x_next

    # Calculate angle between the vectors
    angle_radians = math.atan2(cross_product, dot_product)
    angle_degrees = math.degrees(angle_radians)

    # Determine the direction of turn relative to the current position
    if angle_degrees < -20 and angle_degrees > -150:
        dir = "left"
    elif angle_degrees > 20 and angle_degrees < 150:
        dir = "right"
    elif angle_degrees > -20 and angle_degrees < 20:
        dir = "back"
    else:
        dir = "straight"
    return dir

def create_instructions(coordinates):
    instructions = []
    prev_direction = None
    for i in range(len(coordinates) - 1):
        start_longitude, start_latitude = coordinates[i]
        end_longitude, end_latitude = coordinates[i + 1]

        current_direction = calculate_direction(start_longitude, start_latitude, end_longitude, end_latitude)
        distance = calculate_distance(start_longitude, start_latitude, end_longitude, end_latitude)
        if prev_direction is None:
            instructions.append(f"From {coordinates[i]} to {coordinates[i + 1]}: Head {current_direction} towards the destination for {distance:.2f} kilometers.")
        else:
            dir = calculate_angle(coordinates[i - 1], coordinates[i], coordinates[i + 1])

            if dir == 'back':
                instructions.append(f"At {coordinates[i]}, make a U-turn and continue for {distance:.2f} kilometers.")
            elif dir == 'right':
                instructions.append(f"At {coordinates[i]}, turn right and continue for {distance:.2f} kilometers.")
            elif dir == 'left':
                instructions.append(f"At {coordinates[i]}, turn left and continue for {distance:.2f} kilometers.")
            else:
                instructions.append(f"At {coordinates[i]}, continue straight for {distance:.2f} kilometers.")
        prev_direction = current_direction

    return instructions

def create_instructions(coordinates):
    instructions = []
    prev_direction = None
    total_distance = 0  # Initialize total distance
    for i in range(len(coordinates) - 1):
        start_longitude, start_latitude = coordinates[i]
        end_longitude, end_latitude = coordinates[i + 1]

        distance = calculate_distance(start_longitude, start_latitude, end_longitude, end_latitude)
        total_distance += distance  # Add the distance to the total

        current_direction = calculate_direction(start_longitude, start_latitude, end_longitude, end_latitude)

        if prev_direction is None:
            instructions.append(f"From {coordinates[i]} to {coordinates[i + 1]}: Head {current_direction} towards the destination for {distance:.2f} kilometers.")
        else:
            dir = calculate_angle(coordinates[i - 1], coordinates[i], coordinates[i + 1])

            if dir == 'back':
                instructions.append(f"At {coordinates[i]}, make a U-turn and continue for {distance:.2f} kilometers.")
            elif dir == 'right':
                instructions.append(f"At {coordinates[i]}, turn right and continue for {distance:.2f} kilometers.")
            elif dir == 'left':
                instructions.append(f"At {coordinates[i]}, turn left and continue for {distance:.2f} kilometers.")
            else:
                instructions.append(f"At {coordinates[i]}, continue straight for {distance:.2f} kilometers.")
        prev_direction = current_direction

    # Add total distance to the last instruction
    instructions.append(f"Total distance traveled: {total_distance:.2f} kilometers.")

    return instructions


def model(start_longitude, start_latitude, end_longitude, end_latitude):
    # Replace '<UserAccessToken />' with your actual Mapbox access token
    access_token = ''  # Replace this with your actual access token

    # # Prompt user for starting and ending coordinates
    # start_longitude = float(input("Enter the starting longitude: "))
    # start_latitude = float(input("Enter the starting latitude: "))
    # end_longitude = float(input("Enter the ending longitude: "))
    # end_latitude = float(input("Enter the ending latitude: "))

    # Construct the API URL with coordinates and access token
    api_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_longitude},{start_latitude};{end_longitude},{end_latitude}?geometries=geojson&access_token={access_token}"

    # Fetch directions
    directions_data = fetch_directions(api_url)
    if directions_data:
        # Extract coordinates from geometry.coordinates
        coordinates = directions_data["routes"][0]["geometry"]["coordinates"]

        # Create instructions
        instructions = create_instructions(coordinates)

        # Print instructions
        for instruction in instructions:
            print(instruction)
    else:
        print("Error: Unable to fetch directions.")
