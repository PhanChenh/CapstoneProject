import requests
import re

# Function to clean addresses
def clean_address(address):
    # Remove unnecessary details like shop or unit numbers
    address = re.sub(r'Shop \d+/?\d*', '', address, flags=re.IGNORECASE)
    address = re.sub(r'Unit \d+/?\d*', '', address, flags=re.IGNORECASE)

    # Clean the address by removing excessive whitespace
    address = re.sub(r'\s+', ' ', address).strip()
    
    return address

# Function to get coordinates and additional data from OpenCage
def get_coordinates_opencage(address):
    api_key = "4cb57eedf2b84b82940a0b5423fee563"  # Replace with your OpenCage API key
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': address,
        'key': api_key,
        'no_annotations': 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Print the entire response for debugging
    print("API Response:", data)

    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        
        # Extract additional geographic information
        components = data['results'][0]['components']
        country_name = components.get('country', None)
        constituent_country_name = components.get('state', None)  # Administrative level 1
        administrative_level_1 = components.get('suburb', None)  # Depending on the country, it could also be 'state' or similar
        region = components.get('region', 'N/A')  # Extract region if available

        return latitude, longitude, country_name, constituent_country_name, administrative_level_1, region
    else:
        return None, None, None, None, None, None

# Example addresses for testing
addresses = [
    "Shop 2/154 Newcastle St, Perth WA 6000, Australia",
    "321 Abernethy Rd, Cloverdale WA 6105, Australia",
    "39 Belvidere St, Belmont WA 6104, Australia",
    "55 Boulevard du Château, 92200 Neuilly-sur-Seine, France",
    "20 Devonshire Place, London W1G 6BW, United Kingdom",
    "58 Howard Street, Belfast BT1 6PJ, United Kingdom",
    "Llwynhendy Road, Llwynhendy, Llanelli SA14 9BN, United Kingdom"
]

# Loop through addresses and get coordinates
for addr in addresses:
    cleaned_address = clean_address(addr)
    print(f"Cleaned Address: {cleaned_address}")
    latitude, longitude, country_name, constituent_country_name, administrative_level_1, region = get_coordinates_opencage(cleaned_address)
    
    if latitude is not None and longitude is not None:
        print(f"Address: {cleaned_address}\n"
              f"Latitude: {latitude}, Longitude: {longitude}\n"
              f"Country Name: {country_name}, Constituent Country Name: {constituent_country_name}, "
              f"Administrative Level 1: {administrative_level_1}, Region: {region}\n")
    else:
        print(f"Failed to get coordinates for address: {cleaned_address}\n")
