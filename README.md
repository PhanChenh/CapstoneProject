# Capstone Project

In here, I've worked on Location and Performing lab columns to de-identify.

## Performing lab:

For Performing lab, according to PPRL information.

I generate a random encryption key, then combine the data in performing lab with that encryption key.
After that, I use hash method to hash that combine.
This is more secure comparing to use hash method only (reduce re-identify risk even if the attacker has a potential data list) 

After that, I create a pseudonym matching to apply pseudonym method on hash value above.
This will help user/ analysis have a clear view of their data more than look at hash value (a long string)

**Note:** 
As you noted that I did create a key and a matching which is not a good idea for de-identify.

But I've set a code to delete the key and matching after use right after that by overwrite the key with 0, set it to None to clear the computer memory, and then delete the variable. 
We can set the file permission to only be executed for user after we finalise everything to enhance the security. 

In streamlit, I separate the hash and pseudonym methods so that it can be apply to any columns with separate methods.

But for pseudonym methods, it still attach to hash value, which I think this is a good idea to keep it like that 
since pseudonym is not a one-way process like hashing (Pseudonymization is reversible). 
(Hash does not relate to pseudonym, but pseudonym will process on hash value behind the scenes).

## Location
Following HIPAA guidelines, we can only generalise the location which have at least 20,000 inhabitants. 

The data we were provided is quite a mess, some rows are region level, some are county level or I don't know if its a city/town/or village level to begin with.

For example we have Wales (Wales is a constituent country, but also there's a town/village named Wales in England) -> need to ask back.

Moreover, as Zahraa said that the dataset is about the UK only. So I'm wondering if we can do some preprocessing for the location to make it able to generalise. 

**Example format:**

"North West, England"

"Liverpool, England"

"Kent, England"

"Wales, Wales"

"Northern Ireland, Northern Ireland"

-> format: "region/county name/first-level of administrative division", "constituent country name" or "region//first-level of administrative division", "country name"

**Note:** 
As the code I provided works on this format: "region/county name", "constituent country name" so I've provided a sample data.csv for you to have a look.

In generalisation method, I created 4 different level: country name, constituent country name, region name, county name.

As I've checked, all county in the UK have population above 20,000 so it should be fine if we can make this far 
(but I'm not sure about the data so the county level is still inappropriate).

## Location Problem Solved

Now you can run the preprocessing.py file on streamlit to do the location column preprocessing.
Run the code with command: 
```
streamlit run preprocessing.py
```
Choose the data you want to preprocess, the data format in here remains the same as the original data that Zahraa gave us. 

Then you will want to choose column (e.g. Clinic Location) to preprocesing, you will get 2 column name: Constituent Country from <Clinic Location> and Formatted Location from <Clinic Location>.

You can choose delete column Constituent Country from <Clinic Location> and Clinic Location since we only need Formatted Location from <Clinic Location> for later use to extract region name. 

**Note:**

The preprocessing part is only for The UK. other country should follow this format: "region//first-level of administrative division", "country name"

## About the files:
- ne_10m_admin_0_countries_gbr folder contain shapefile which will have country boundary.
- ne_10m_admin_1_states_provinces folder contain shapefile which will have country states/provinces boundary.
- gadm41_GBR_shp folder contain shapefile which will have county in The UK boundary.
- capstone.csv is the file that we were provided (I changed the name).
- data.csv is a sample file which have location column was formatted for generalise method.
- requirement.txt is a file which contain all neccessary library to run the code.
- preprocessing.py is contain streamlit code that you want to run to clean and format the location columns for later use.
- app.py is contain streamlit code that you want to run.
- capstoneapp_V1.py is Kim's work on Clinic Name, you can have a look if you want. 

## Steps to run the code smoothly:
Step 1: Locate to the correct directory where you save these file  
Step 2: Install all neccessary library before you run the code in requirement.txt with command: 
```
pip install -r requirements.txt
```
Step 3: Run the code with command: 
```
streamlit run app.py
```
