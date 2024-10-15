# Capstone Project

In this project, I focused on de-identifying the 'Location' and 'Performing Lab' columns in accordance with privacy regulations.

## Performing lab:

For the 'Performing Lab' column (which is a rpeated data column, not a unique column), I adhered to privacy-preserving record linkage (PPRL) guidelines. I generated a random encryption key and combined it with the data in the 'Performing Lab' column. This combined data was then hashed using a secure hashing method. This approach is more secure compared to simple hashing alone, as it reduces the risk of re-identification, even if an attacker possesses a potential data list.

Subsequently, I applied pseudonymization to the hashed values by creating a pseudonym matching system. This method allows users and analysts to interpret the data more clearly than using the hash values alone, which typically appear as long strings.

**Note:** While creating an encryption key and matching system might not be ideal for de-identification, I implemented a mechanism to securely remove these elements after their use. This is done by overwriting the key with zeroes, setting it to `None` to clear the computer's memory, and then deleting the variable. Additionally, file permissions can be set to 'execute only' for users once all processes are finalized to enhance security further.

In the Streamlit application, I separated the hash and pseudonym methods to allow flexibility in applying these methods to any column independently. However, the pseudonym method still relies on the hash values, which I believe is an effective approach, as pseudonymization is inherently reversible, unlike hashing (which is a one-way process). This means the pseudonymization process is based on the hash values behind the scenes.

## Location

In compliance with HIPAA guidelines, locations were generalized only when they had a minimum population of 20,000 inhabitants. The dataset provided contained inconsistencies, with some rows at the region level, others at the county level, and some may at various levels of specificity (e.g., city, town, or village).

For example, entries like "Wales" could be ambiguous, as Wales is both a constituent country and a name used for towns or villages in England.

## Location Preprocessing

To preprocess the 'Location' column, run the preprocessing.py file using Streamlit with the following command:
```
streamlit run preprocessing.py
```
Select the dataset you want to preprocess. The data format remains consistent with the original format provided by Zahraa. You will then choose the column (e.g., 'Clinic Location') to preprocess, resulting in two new columns: 'Constituent Country from <Clinic Location>' and 'Formatted Location from <Clinic Location>'. You can delete the 'Constituent Country from <Clinic Location>' and 'Clinic Location' columns, retaining only the 'Formatted Location from <Clinic Location>' for subsequent use in extracting regional information.

**Note:** The preprocessing functionality currently supports locations in the UK. For other countries, the format should be structured as follows: "region//first-level administrative division," "country name."

**Desired format example:**
"North West, England"

"Liverpool, England"

"Kent, England"

"Wales, Wales"

"Northern Ireland, Northern Ireland"

The format should follow this structure: "region/county name/first-level administrative division," "constituent country name" or "region//first-level administrative division," "country name."

## Location format accuracy

After consulting with Zahraa, it was confirmed that the original data could provide exact location details.

**Example:**
268 Belmont Avenue Corner, Fulham Street, Cloverdale WA 6105

154 Newcastle Street, Perth WA 6000

501 George Street, Sydney NSW 2000

1 Avenue Claude Vellefaux, 75010 Paris, France

With this information, it is now possible to extract longitude, latitude, country names, and administrative divisions (e.g., states, suburbs). 


## About the files:
- `ne_10m_admin_0_countries_gbr` folder contains shapefiles with country boundaries.
- `ne_10m_admin_1_states_provinces` folder contains shapefiles with state/province boundaries.
- `requirement.txt` lists all necessary libraries for running the code.
- `preprocessing.py` contains Streamlit code for cleaning and formatting the location column.
- `app.py` contains the main Streamlit code for the application.
- `LocationGeneralizer.py` is a class module for generalizing location columns before exact locations were available.
- `exampleLoc.py` is a Python file for extracting longitude, latitude, country names, and administrative divisions after exact locations were confirmed.
-  `hashingPseudonym.py`  is a class module for the hashing and pseudonymization methods.
-  `SecureDataManager.py` is a class module for securely removing keys and matchings created during the hashing and pseudonymization processes.

## Steps to Execute the Code

Step 1: Navigate to the directory where the files are stored.  
Step 2: Install all required libraries from `requirement.txt` using the command:
```
pip install -r requirements.txt
```
Step 3: Run the code using command: 
```
streamlit run preprocessing.py
```
- Use the command above to format and generalize the location data as described.
- Use the command below to de-identify data for specific columns:
```
streamlit run app.py
```
