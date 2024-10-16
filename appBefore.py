import streamlit as st
import pandas as pd
import geopandas as gpd
import re
import hashlib  # Import hashlib for hashing
from shapely.geometry import Point
import hashlib
import random
import string
import gc

#THE COMPLETE ONE - should I delete the county name? 
# Load shapefiles (Update paths as necessary)
country_shapefile = 'ne_10m_admin_0_countries_gbr/ne_10m_admin_0_countries_gbr.shp'
region_shapefile = 'ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'

# Load GeodataFrames
gdf0 = gpd.read_file(country_shapefile)
gdf1 = gpd.read_file(region_shapefile)

# Extract necessary information for constituent countries
uk = gdf0[gdf0['ADMIN'] == 'United Kingdom']
woe_note = uk['WOE_NOTE'].unique()[0]
constituent_countries = re.findall(r'(?<=countries of\s)(.*?)(?=\.\s|$)', woe_note)
if constituent_countries:
    constituent_countries = [re.sub(r'\s*\(.*?\)', '', country).strip() for country in constituent_countries[0].split(',')]
    constituent_countries = [country.replace('and ', '').strip('.').strip() for country in constituent_countries]
else:
    constituent_countries = []

# Function to retrieve country name
def get_country(location, uk_unique_admins, constituent_countries):
    country_name = location.split(',')[1].strip()
    if country_name in uk_unique_admins:
        return country_name
    if country_name in constituent_countries:
        return "United Kingdom"
    return "Unknown"

# Function to retrieve constituent country name
def get_constituent_country(location, constituent_countries):
    loc_parts = location.split(', ')
    country_name = loc_parts[1].strip()
    if country_name in constituent_countries:
        return country_name
    return None

# Function to retrieve region or original name
def get_region(location):
    loc_parts = location.split(', ')
    loc_name = loc_parts[0].strip()  # Get the name before the comma
    country_name = loc_parts[1].strip()  # Get the country name after the comma
    
    # Check if the country is a constituent country of the UK
    if country_name in constituent_countries:
        regions = gdf1[gdf1['admin'] == 'United Kingdom']
    elif country_name in gdf1['admin'].values:
        regions = gdf1[gdf1['admin'] == country_name]
    else:
        return loc_name + ' ' + country_name 
    
    # Check if loc_name is in the unique regions of the filtered GeoDataFrame
    if loc_name in regions['name'].values:
        region_row = regions[regions['name'] == loc_name]
        
        # Check if the 'region' field exists and is not empty
        if not region_row.empty and 'region' in region_row.columns and not pd.isnull(region_row['region'].values[0]):
            return region_row['region'].values[0] + ' ' + country_name
        
    # If no region data, return loc_name + country_name
    return loc_name + ' ' + country_name 


# Function to generate a random encryption key
def generate_encryption_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # 16 characters long key

# Function to hash a value with an encryption key
def hash_value_with_key(value, key):
    value_with_key = f'{value}_{key}'
    return hashlib.sha256(value_with_key.encode()).hexdigest()

# Function to generate a pseudonym with the column name
def generate_pseudonym(index, column_name):
    return f'{column_name}_{chr(65 + index)}'  # Pseudonyms like columnName_A, columnName_B, etc.

# Generalization Methods
def apply_generalization(df, column, selected_methods):
    if 'Generalize to Country Name' in selected_methods:
        uk_unique_admins = gdf0['ADMIN'].unique()
        df[f'{column} Country'] = df[column].apply(lambda loc: get_country(loc, uk_unique_admins, constituent_countries))
    
    if 'Generalize to Constituent Country Name' in selected_methods:
        df[f'{column} Constituent Country'] = df[column].apply(lambda loc: get_constituent_country(loc, constituent_countries))
    
    if 'Generalize to Region Name' in selected_methods:
        df[f'{column} Region'] = df[column].apply(lambda loc: get_region(loc))
    
    if 'Generalize to County Name' in selected_methods:
        df[f'{column} County'] = df[column].apply(lambda loc: get_county_or_district(loc, gdf_county))
    
    return df

# Hashing Function
def apply_hashing(df, column, encryption_key):
    if encryption_key:
        df[f'{column} Hashed'] = df[column].apply(lambda loc: hash_value_with_key(loc, encryption_key))
    return df

# Secure removal function
def secure_remove_key_and_mapping(encryption_key):
    # Securely remove the encryption key
    encryption_key = '0' * len(encryption_key)  # Overwrite with zeros
    encryption_key = None  # Clear from memory
    del encryption_key  # Delete the variable

# Streamlit UI
st.title("Location Data Generalization")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file with location data", type=["csv"])

if uploaded_file is not None:
    # Load uploaded file
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(df)

    # Select columns for generalization
    column_options = df.columns.tolist()
    selected_generalize_columns = st.multiselect("Choose columns for generalization", column_options)

    # Select columns for hashing
    selected_hash_columns = st.multiselect("Choose columns for hashing", column_options)

    # Select columns for pseudonymization
    selected_pseudonym_columns = st.multiselect("Choose columns for pseudonymization", column_options)

    # Display generalization options
    generalize_options = [
        'Generalize to Country Name',
        'Generalize to Constituent Country Name',
        'Generalize to Region Name'
    ]
    selected_generalize_methods = st.multiselect("Choose generalization methods", generalize_options)

    # Generate encryption key for hashing and pseudonymization
    encryption_key = generate_encryption_key()

    # Apply generalization methods
    if selected_generalize_columns and selected_generalize_methods:
        for column in selected_generalize_columns:
            if column in df.columns:
                if 'Generalize to Country Name' in selected_generalize_methods:
                    uk_unique_admins = gdf0['ADMIN'].unique()
                    df[f'{column} Country'] = df[column].apply(lambda loc: get_country(loc, uk_unique_admins, constituent_countries))
                if 'Generalize to Constituent Country Name' in selected_generalize_methods:
                    df[f'{column} Constituent Country'] = df[column].apply(lambda loc: get_constituent_country(loc, constituent_countries))
                if 'Generalize to Region Name' in selected_generalize_methods:
                    df[f'{column} Region'] = df[column].apply(lambda loc: get_region(loc))


    # Apply hashing
    if selected_hash_columns:
        for column in selected_hash_columns:
            if column in df.columns:
                df[f'{column} Hashed'] = df[column].apply(lambda loc: hash_value_with_key(loc, encryption_key))

    # Apply pseudonymization
    pseudonym_mapping = None  # Initialize pseudonym_mapping as None
    if selected_pseudonym_columns:
        pseudonym_mapping = {}  # Initialize only if pseudonymization is selected
        for column in selected_pseudonym_columns:
            if column in df.columns:
                unique_labs = df[column].unique()
                for index, lab in enumerate(unique_labs):
                    hashed_value = hash_value_with_key(lab, encryption_key)
                    pseudonym_mapping[hashed_value] = generate_pseudonym(index, column)
                df[f'{column} Pseudonymized'] = df[column].apply(lambda loc: pseudonym_mapping[hash_value_with_key(loc, encryption_key)])

        # Securely delete pseudonym_mapping after pseudonymization
        pseudonym_mapping.clear()  # Clear the dictionary contents
        pseudonym_mapping = None  # Overwrite reference with None to remove from memory
        del pseudonym_mapping  # Explicitly delete the variable

    # Display the updated DataFrame with all columns
    st.write("Data after Generalization, Hashing, and Pseudonymization:")
    st.dataframe(df)

    # Securely remove the encryption key and pseudonym mapping after processing
    secure_remove_key_and_mapping(encryption_key)

    # Allow the user to choose columns to delete
    columns_to_delete = st.multiselect("Choose columns to delete from the output", df.columns.tolist())

    # Drop the selected columns
    if columns_to_delete:
        df.drop(columns=columns_to_delete, inplace=True)

    # Download button for the updated data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Updated Data",
        data=csv,
        file_name="updated_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to proceed.")
