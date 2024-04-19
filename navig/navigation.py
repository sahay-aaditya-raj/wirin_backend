import asyncio
import aiohttp
import osmnx as ox
import networkx as nx
from openai import OpenAI
from geopy.geocoders import MapBox
from geopy.exc import GeocoderAuthenticationFailure
from collections import OrderedDict

# Function to fetch data from Mapbox API with advanced caching
class LRUCache:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.cache = OrderedDict()  # Initialize the cache dictionary here

    def get(self, key):
        if key in self.cache:
            # Move the accessed key to the end to mark it as most recently used
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def put(self, key, value):
        if key in self.cache:
            # If key already exists, move it to the end to mark it as most recently used
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # If the cache is full, remove the least recently used item (first item)
            self.cache.popitem(last=False)
        self.cache[key] = value

async def get_openai_response(prompt):
  client = OpenAI(api_key="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")  
  response = await client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
          {
              "role": "user",
              "content": prompt
          }
      ],
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7
    ) 
  return response.choices[0].message.content.strip()

def get_coordinates(location_name, api_key):
    geocoder = MapBox(api_key=api_key)
    try:
        location = geocoder.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except GeocoderAuthenticationFailure as e:
        print(f"Authentication error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

async def fetch_osmnx_data(G, source_coords, dest_coords, cache=None):
    if cache is None:
        cache = LRUCache()
    cache_key = f"{source_coords},{dest_coords}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    # Compute the shortest path
    try:
        source_node = ox.nearest_nodes(G, source_coords[1], source_coords[0])
        dest_node = ox.nearest_nodes(G, dest_coords[1], dest_coords[0])
        route = nx.shortest_path(G, source=source_node, target=dest_node, weight='length')

        route_length = nx.shortest_path_length(G, source=source_node, target=dest_node, weight='length')

        return route, route_length
    except nx.NetworkXNoPath:
        print("No path found between the source and destination.")
        return None, None

async def main():
    location_name = input("Enter a destination: ")
    source_name = input("Enter the source: ")
    api_key = 'pk.eyJ1IjoibWh1emFpZiIsImEiOiJjbHY1ZHdyY3QwMXdiMmpuejU3aTlyNGRmIn0.hTBH1a_vQP9cQmOeTjikCA'  # Replace with your Mapbox API key

    source_coords = get_coordinates(source_name, api_key)
    dest_coords = get_coordinates(location_name, api_key)
    if source_coords and dest_coords:
        print(f"Coordinates for source ({source_name}): {source_coords}")
        print(f"Coordinates for destination ({location_name}): {dest_coords}")

        # Download street network data
        G = ox.graph_from_point(source_coords, network_type='drive')

        # Fetch route using OSMnx
        route, route_length = await fetch_osmnx_data(G, source_coords, dest_coords)
        if route:
            # Convert node IDs to coordinates for better readability
            route_coords = [(G.nodes[node]['x'], G.nodes[node]['y']) for node in route]

            print(f"Route: {route_coords}")
            print(f"Estimated distance: {route_length:.2f} meters")

            # Use OpenAI to craft a response 
            prompt = f"You requested directions to {location_name} using OSMnx data.\nRoute: {route_coords}\nEstimated distance: {route_length:.2f} meters. Would you like to know more about {location_name}?"
            openai_response = await get_openai_response(prompt)
            print(openai_response)
        else:
            print("Failed to retrieve directions from OSMnx.")
    else:
        print("Failed to retrieve coordinates.")

# Run the main loop synchronously
if __name__ == "__main__":
    client = OpenAI(api_key="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")  
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main())
