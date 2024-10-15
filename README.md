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

For example we have Wales (Wales is a constituent country, but also there's a town/village named Wales in England)

## Location Preprocessing

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

**Desire format:**

"North West, England"
"Liverpool, England"
"Kent, England"
"Wales, Wales"
"Northern Ireland, Northern Ireland"

-> format: "region/county name/first-level of administrative division", "constituent country name" or "region//first-level of administrative division", "country name"

## Location format correctness
After asking clients, we now know that the original data can able to get the exact location. 
**Example:**
268 Belmont Avenue Corner, Fulham Street, Cloverdale WA 6105
154 Newcastle Street, Perth WA 6000
501 George Street, Sydney NSW 2000
1 Avenue Claude Vellefaux, 75010 Paris, France

Since we can get the exact location, we can extract the longitude, lattitude, country name, and hierachy of a country Administrative divisions name (states, surbub,...). 


## About the files:
- ne_10m_admin_0_countries_gbr folder contain shapefile which will have country boundary.
- ne_10m_admin_1_states_provinces folder contain shapefile which will have country states/provinces boundary.
- requirement.txt is a file which contain all neccessary library to run the code.
- preprocessing.py is contain streamlit code that you want to run to clean and format the location columns for later use.
- app.py is contain streamlit code that you want to run.
- LocationGeneralizer.py is class module format file for generalise location column before knowing we can get exact location
- exampleLoc.py is .py file working on extracting longitude, lattitude, country name, and hierachy of a country Administrative divisions name (states, surbub,...) after knowing we can get the exact location.
-  hashingPseudonym.py is class module format file for hashing pseudonym method.
-  SecureDataManager.py is class module format file for securely remove the key and matching created while use hashingPseudonym method.

## Steps to run the code smoothly:
Step 1: Locate to the correct directory where you save these file  
Step 2: Install all neccessary library before you run the code in requirement.txt with command: 
```
pip install -r requirements.txt
```
Step 3: Run the code with command: 
```
streamlit run preprocessing.py
```
- run the command above if you want to get the location format as mention above to generalise
- run the command below to de-identify data with specific column that I have worked on. 
```
streamlit run app.py
```
