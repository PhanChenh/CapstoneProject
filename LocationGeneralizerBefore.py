import pandas as pd
import geopandas as gpd
import re

class LocationGeneralizer:
    def __init__(self, country_shapefile, region_shapefile):
        # Load shapefiles
        self.gdf0 = gpd.read_file(country_shapefile)
        self.gdf1 = gpd.read_file(region_shapefile)

        # Extract necessary information for constituent countries
        self.uk = self.gdf0[self.gdf0['ADMIN'] == 'United Kingdom']
        woe_note = self.uk['WOE_NOTE'].unique()[0]
        self.constituent_countries = self.extract_constituent_countries(woe_note)

    def extract_constituent_countries(self, woe_note):
        countries = re.findall(r'(?<=countries of\s)(.*?)(?=\.\s|$)', woe_note)
        if countries:
            countries = [re.sub(r'\s*\(.*?\)', '', country).strip() for country in countries[0].split(',')]
            return [country.replace('and ', '').strip('.').strip() for country in countries]
        return []

    def get_country(self, location, uk_unique_admins):
        country_name = location.split(',')[1].strip()
        if country_name in uk_unique_admins:
            return country_name
        if country_name in self.constituent_countries:
            return "United Kingdom"
        return "Unknown"

    def get_constituent_country(self, location):
        loc_parts = location.split(', ')
        country_name = loc_parts[1].strip()
        if country_name in self.constituent_countries:
            return country_name
        return None

    def get_region(self, location):
        loc_parts = location.split(', ')
        loc_name = loc_parts[0].strip()
        country_name = loc_parts[1].strip()
        
        if country_name in self.constituent_countries:
            regions = self.gdf1[self.gdf1['admin'] == 'United Kingdom']
        elif country_name in self.gdf1['admin'].values:
            regions = self.gdf1[self.gdf1['admin'] == country_name]
        else:
            return loc_name + ' ' + country_name 
        
        if loc_name in regions['name'].values:
            region_row = regions[regions['name'] == loc_name]
            if not region_row.empty and 'region' in region_row.columns and not pd.isnull(region_row['region'].values[0]):
                return region_row['region'].values[0] + ' ' + country_name
        
        return loc_name + ' ' + country_name 

    def apply_generalization(self, df, column, selected_methods):
        if 'Generalize to Country Name' in selected_methods:
            uk_unique_admins = self.gdf0['ADMIN'].unique()
            df[f'{column} Country'] = df[column].apply(lambda loc: self.get_country(loc, uk_unique_admins))

        if 'Generalize to Constituent Country Name' in selected_methods:
            df[f'{column} Constituent Country'] = df[column].apply(lambda loc: self.get_constituent_country(loc))

        if 'Generalize to Region Name' in selected_methods:
            df[f'{column} Region'] = df[column].apply(lambda loc: self.get_region(loc))
        
        return df
