import ast
import fuzzywuzzy
import pandas as pd
import streamlit as st
from fuzzywuzzy import process

st.title("Standardizing Clinic Names")
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    data0 = pd.read_csv(uploaded_file)

    def remove_clinic_dept(text):
        words = text.split()
        # Remove department and join the remaining words
        return ' '.join(words[:-1])

    def get_clinic_dept(text):
        words = text.split()
        # Obtain department
        return words[-1]

    def get_clinic_names_matches(data):
        clinic_names = sorted(data['Clinic Name'].unique().tolist())
        
        for i in range(0, len(clinic_names)):
            clinic_names[i] = remove_clinic_dept(clinic_names[i])
        
        clinic_namesU = sorted(list(set(clinic_names)))

        df1 = clinic_namesU
        df2 = clinic_namesU

        matches_dict = {}

        for ind in range(0, len(clinic_namesU)):
            matches = fuzzywuzzy.process.extract(df1[ind], df2, limit=10)
            highest_score = matches[1:][0][1]
            for m_ind in range(0, len(matches)-1):
                if matches[1:][m_ind][1] == highest_score:
                    key = df1[ind]
                    if key in matches_dict:
                        matches_dict[key].append(matches[1:][m_ind][0])
                    else:
                        matches_dict[key] = [matches[1:][m_ind][0]]
        
        return(matches_dict)

    clin_names_matches = get_clinic_names_matches(data0)
    df = pd.DataFrame(clin_names_matches.items()).rename(columns={0: "Location", 1: "Possible Replacement"})

    # Display the original data
    st.write("Here are the clinic locations and possible replacements:")
    st.write(df)

    # Create two columns in Streamlit
    col1, col2, col3 = st.columns(3)

    # Dictionary to store mappings
    mapping = {}
    keys = [key for key in clin_names_matches]

    # Generate input fields to store in mappings
    for i in range(len(keys)):
        with col1:
            key = st.text_input(f"Location: ", keys[i])
        with col2:
            options = clin_names_matches[keys[i]] + ['Keep as is'] + ['Type in replacement..']
            value = st.selectbox(f"Replace with: ", options=options)
        
        with col3:
            if value ==  'Type in replacement..':
                otherRep = st.text_input(f'Type in replacement..', disabled=False, key=i)
            else:
                otherRep = st.text_input(f'Type in replacement..', disabled=True, key=i)
        
        if value == 'Keep as is':
            mapping[key] = key
        elif value == 'Type in replacement..':
            mapping[key] = otherRep
        else:
            mapping[key] = value

    # Button to generate replacements
    if 'review_replacements' not in st.session_state:
        st.session_state['review_replacements'] = False
    if 'confirm_replacements' not in st.session_state:
        st.session_state['confirm_replacements'] = False

    if st.button("Review replacements"):
        st.session_state['review_replacements'] = True
    
    if st.session_state['review_replacements']:
        # Output selected replacements
        df_rep = df[['Location']].rename(columns={"Location": "Before"})
        df_rep['After'] = df['Location'].replace(mapping)
        st.write(df_rep)

        
        # Button to confirm replacements
        if st.button("Confirm replacements"):
            st.session_state['confirm_replacements'] = True

        if st.session_state['confirm_replacements']:
            # use mappings to replace actual data
            dept_replacements = {'Onc.': 'Oncology'}

            clinic_names0 = data0['Clinic Name'].copy()
            dept_names0 = data0['Clinic Name'].copy()

            for i in range(0, len(clinic_names0)):
                clinic_names0[i] = remove_clinic_dept(clinic_names0[i])
                dept_names0[i] = get_clinic_dept(dept_names0[i])

            clinic_loc = pd.DataFrame(clinic_names0)
            clinic_dept = pd.DataFrame(dept_names0)

            clinic_loc = clinic_loc.replace(mapping)
            clinic_dept = clinic_dept.replace(dept_replacements)

            data1 = data0.copy()
            data1['Clinic Name'] = clinic_loc + ' ' + clinic_dept

            @st.cache_data
            def convert_df(df):
                return df.to_csv().encode("utf-8")

            csv = convert_df(data1)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download mapping file", str(mapping), file_name='clin_names_mapping.txt')
            with col2:
                st.download_button(
                label="Download processed data as CSV",
                data=csv,
                file_name="standardized_clin_names.csv",
                mime="text/csv"
                )
else:
    st.write(" ")