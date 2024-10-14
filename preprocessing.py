import pandas as pd
import requests
import time

class DataProcessor:
    def __init__(self):
        # Hardcoded mapping for the UK regions and countries
        self.uk_region_to_country = {
            # Wales
            'Wales': 'Wales',
            'North Wales': 'Wales',
            'Mid Wales': 'Wales',
            'South West Wales': 'Wales',
            'South East Wales': 'Wales',

            # Northern Ireland
            'Northern Ireland': 'Northern Ireland',

            # Scotland
            'Scotland': 'Scotland',
            'Campbeltown': 'Scotland',
            'Highland': 'Scotland',
            'Islay': 'Scotland',
            'Lowland': 'Scotland',
            'Speyside': 'Scotland',

            # England
            'England': 'England',
            'Greater London': 'England',
            'South East': 'England',
            'South': 'England',
            'West': 'England',
            'West Midlands': 'England',
            'Midlands': 'England',
            'North West': 'England',
            'North East': 'England',
            'Yorkshire and the Humber': 'England',
            'East Midlands': 'England',
            'East of England': 'England',
            'Yorkshire and Humber': 'England',
        }

        # Cleaning map for standardized constituent country names
        self.cleaning_map = {
            'Cymru / Wales': 'Wales',
            'Northern Ireland / Tuaisceart Éireann': 'Northern Ireland',
            'Alba / Scotland': 'Scotland',
        }

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def get_constituent_country(self, location):
        if "United Kingdom" not in location:
            return location.split(",")[0]  # Return the name before the comma if not in UK

        for region, country in self.uk_region_to_country.items():
            if region in location:
                return country
        
        # If not found in the mapping, call the API
        try:
            headers = {
                'User-Agent': 'DataProcessor/1.0 (my_email@gmail.com)'
            }
            response = requests.get(f"https://nominatim.openstreetmap.org/search?q={location}&format=json&addressdetails=1", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data:
                address = data[0].get('address', {})
                country = address.get('country', 'Unknown')
                state = address.get('state', 'Unknown')
                
                if 'United Kingdom' in country:
                    return state if state else "Unknown"
                return country
        except Exception as e:
            print(f"Error while fetching data for {location}: {e}")
        
        return "Unknown"

    def preprocess_columns(self, df, selected_columns):
        for column in selected_columns:
            # Add ", United Kingdom" to each selected column
            df[column] = df[column] + ', United Kingdom'

            # Apply the function to get constituent country
            constituent_countries = []
            for location in df[column]:
                country = self.get_constituent_country(location)
                constituent_countries.append(country)
                time.sleep(1)  # Delay to prevent hitting the rate limit

            df[f'Constituent Country from {column}'] = constituent_countries

            # Clean the constituent country data using the cleaning map
            df[f'Constituent Country from {column}'] = df[f'Constituent Country from {column}'].replace(self.cleaning_map)

            # Create a new column with "name, <constituent country>"
            df[f'Formatted Location from {column}'] = df[column].str.replace(', United Kingdom', '') + ', ' + df[f'Constituent Country from {column}']

        return df

    def delete_columns(self, df, columns_to_delete):
        return df.drop(columns=columns_to_delete)

    def save_data(self, df, file_path):
        df.to_csv(file_path, index=False) 
