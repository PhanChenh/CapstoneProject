# WORKED WELL
import streamlit as st
import pandas as pd
import requests
import time

# Load data file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.write("Original Data")
    st.dataframe(df)

    # Select columns to process
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to preprocess", columns)

    # Hardcoded mapping for the UK regions and countries
    uk_region_to_country = {
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
    cleaning_map = {
        'Cymru / Wales': 'Wales',
        'Northern Ireland / Tuaisceart Éireann': 'Northern Ireland',
        'Alba / Scotland': 'Scotland',
    }

    # Function to get constituent country dynamically using Nominatim
    def get_constituent_country(location):
        if "United Kingdom" not in location:
            return location.split(",")[0]  # Return the name before the comma if not in UK

        for region, country in uk_region_to_country.items():
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

    # Preprocess each selected column
    for column in selected_columns:
        # Add ", United Kingdom" to each selected column
        df[column] = df[column] + ', United Kingdom'

        # Apply the function to get constituent country
        constituent_countries = []
        for location in df[column]:
            country = get_constituent_country(location)
            constituent_countries.append(country)
            time.sleep(1)  # Delay to prevent hitting the rate limit

        df[f'Constituent Country from {column}'] = constituent_countries

        # Clean the constituent country data using the cleaning map
        df[f'Constituent Country from {column}'] = df[f'Constituent Country from {column}'].replace(cleaning_map)

        # Create a new column with "name, <constituent country>"
        df[f'Formatted Location from {column}'] = df[column].str.replace(', United Kingdom', '') + ', ' + df[f'Constituent Country from {column}']

    # Display processed data
    st.write("Processed Data")
    st.dataframe(df)

    # Select columns to delete
    columns_to_delete = st.multiselect("Select columns to delete", df.columns)
    if columns_to_delete:
        df = df.drop(columns=columns_to_delete)

    # Display final data
    st.subheader("Final Data")
    st.dataframe(df)
        
    # Download processed data
    st.download_button("Download Processed Data", data=df.to_csv(index=False), file_name="processed_data.csv")
