from datetime import datetime
import streamlit as st
import pandas as pd
from SQL_connection import create_server_connection
from secret.credentials import *
from utils import *
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Doctor Patient Info'

st.title('Patient Information for doctor')

db_connection = create_server_connection(host, username, password, database)

patient_id = int(st.text_input('Enter Patient ID', '0'))


if st.button('Get Patient Information'):

    if check_patient_exists(db_connection, patient_id):

        patient_info = get_patient_details(db_connection, patient_id)
        if patient_info:
            patient_info_df = pd.DataFrame([patient_info[0]], columns=[
                'First Name', 'Last Name', 'Gender', 'DOB', 'Marital Status'])

            patient_info_df = patient_info_df.to_html(index=False, border=0)

            st.subheader('Patient Information')
            st.markdown(patient_info_df, unsafe_allow_html=True)

        else:
            st.warning("No Patient Information Available")

        medical_info = get_patient_medical_info(db_connection, patient_id)
        if medical_info:
            medical_background_df = pd.DataFrame([medical_info[0]], columns=[
                'Weight', 'Blood Group', 'Tobacco Usage', 'Alcohol Intake', 'Diabetic', 'Blood Pressure Issues'])

            boolean_columns = ['Tobacco Usage', 'Alcohol Intake',
                               'Diabetic', 'Blood Pressure Issues']
            for col in boolean_columns:
                medical_background_df[col] = medical_background_df[col].map(
                    map_boolean_to_string)

            medical_background_df_html = medical_background_df.to_html(
                index=False)

            st.title("")
            st.subheader('Medical Background')
            st.markdown(medical_background_df_html, unsafe_allow_html=True)

        else:
            st.warning("No Patient Medical Background Information Available")

        family_medical_info = get_patient_family_medical_info(
            db_connection, patient_id)

        if family_medical_info:
            family_diseases = family_medical_info[0][0]
            family_medical_background_df = pd.DataFrame(
                [[family_diseases]], columns=['Family Medical History'])

            html = family_medical_background_df.to_html(index=False)

            st.title("")

            st.subheader('Family Medical History')
            st.markdown(html, unsafe_allow_html=True)

        else:
            st.warning("No Family Medical Background Information Available")

    else:
        st.error('No patient information found for the given ID.')

st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to Doctor Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "Doctor"
        switch_page("Doctor")
