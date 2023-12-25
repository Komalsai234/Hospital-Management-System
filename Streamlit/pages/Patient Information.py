import streamlit as st
from datetime import datetime
from secret.credentials import *
from SQL_connection import create_server_connection, execute_query
from utils import get_disease_id
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Patient Information'

st.subheader('Patient Information')
patient_id = int(st.text_input('Patient ID', '0'))
first_name = st.text_input('First Name', '').strip()
last_name = st.text_input('Last Name', '').strip()
gender = st.selectbox('Gender', ['', 'Male', 'Female', 'Other'])
mobile = st.text_input('Mobile', '').strip()
email = st.text_input('Email', '').strip()
dob = st.date_input('Date of Birth', min_value=datetime(
    1900, 1, 1), max_value=datetime.now(), key='dob')
marital_status = st.selectbox(
    'Marital Status', ['', 'Single', 'Married', 'Divorced', 'Widowed'])

st.subheader(" ")

st.subheader('Emergency Contact Information')
ec_email = st.text_input('Emergency Contact Email', '').strip()
ec_mobile = st.text_input('Emergency Contact Mobile Number', '').strip()
ec_relationship = st.text_input('Relationship to Patient', '').strip()

st.subheader(" ")

st.subheader('Patient Address Information')
address = st.text_input('Address', '').strip()
city = st.text_input('City', '').strip()
zipcode = st.text_input('ZipCode', '').strip()
state = st.text_input('State', '').strip()
country = st.text_input('Country', '').strip()

st.subheader(" ")

st.subheader('Patient Medical Background Information')
weight = st.number_input('Weight (in kg)', min_value=0.0, format='%.2f')
blood_group = st.selectbox(
    'Blood Group', ['', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
tobacco_usage = st.checkbox('Tobacco Usage')
alcohol_intake = st.checkbox('Alcohol Intake')
is_diabetic = st.checkbox('Is Diabetic')
is_having_bp = st.checkbox('Is Having Blood Pressure')

st.subheader(" ")
st.subheader('Family Medical History')

# Define your diseases
diseases = [
    'Mental Health Disorder',
    'Colon Cancer',
    'Prostate/Uterine Cancer',
    'Breast Cancer',
    'Lung Cancer',
    'Diabetes',
    'High Blood Pressure',
    'High Cholesterol',
    'Heart Disease/Kidney Disease',
    'Alcohol Issues'
]

col1, col2 = st.columns(2)

checked_diseases = []

with col1:
    for disease in diseases[:5]:
        if st.checkbox(disease, key=disease):
            checked_diseases.append(disease)

with col2:
    for disease in diseases[5:]:
        if st.checkbox(disease, key=disease):
            checked_diseases.append(disease)


st.subheader(" ")
st.subheader('Health Insurance Information')
health_insurance_id = int(st.text_input('Health Insurance ID', '0'))
provider_name = st.text_input('Provider Name', '').strip()
coverage_plan = st.text_input('Coverage Plan', '').strip()
coverage_is_under = st.text_input('Coverage is Under', '').strip()


st.subheader(" ")
submit_button = st.button(label='Submit')

db_connection = create_server_connection(host, username, password, database)


if submit_button:
    if not all([patient_id, first_name, last_name, gender, mobile, email, dob, marital_status, ec_email, ec_mobile, ec_relationship, address, city, zipcode, state, country, weight, blood_group]):
        st.error('Please fill out all fields.')
    elif patient_id == 0:
        st.error('Please Enter Valid Patient ID.')
    else:
        patient_tuple = (patient_id, first_name, last_name, gender,
                         mobile, email, dob, marital_status)
        emergency_contact_tuple = (
            patient_id, ec_email, ec_mobile, ec_relationship)

        patient_address_tuple = (
            patient_id, address, city, zipcode, state, country)

        patient_medical_background_tuple = (
            patient_id, weight, blood_group, tobacco_usage, alcohol_intake, is_diabetic, is_having_bp)

        health_insurance_data = (
            patient_id, health_insurance_id, provider_name, coverage_plan, coverage_is_under)

        insert_patient_query = f"""
                                INSERT INTO Patient (PatientID,FirstName, LastName, Gender, Mobile, Email, DOB, MaritalStatus)
                                            VALUES ('{patient_tuple[0]}', '{patient_tuple[1]}', '{patient_tuple[2]}',
                                                    '{patient_tuple[3]}', '{patient_tuple[4]}', '{patient_tuple[5]}', '{patient_tuple[6]}', '{patient_tuple[7]}');"""

        insert_emergency_contact_query = f"""
                                            INSERT INTO EmergencyContact (PatientID,Email, MobileNumber, RelationshipToPatient)
                                                        VALUES ('{emergency_contact_tuple[0]}', '{emergency_contact_tuple[1]}', '{emergency_contact_tuple[2]}','{emergency_contact_tuple[3]}');
                                        """

        insert_patient_address_query = f"""
                                            INSERT INTO PatientAddress (PatientID, Address, City, ZipCode, State, Country)
                                                        VALUES ('{patient_address_tuple[0]}', '{patient_address_tuple[1]}', '{patient_address_tuple[2]}',
                                                        '{patient_address_tuple[3]}', '{patient_address_tuple[4]}', '{patient_address_tuple[5]}');
                                        """

        insert_patient_medical_background_query = f"""
                                            INSERT INTO PatientMedicalBackground (PatientID, Weight, BloodGroup, TobaccoUsage, AlcoholIntake, IsDiabetic, IsHavingBP)
                                                        VALUES ('{patient_medical_background_tuple[0]}', '{patient_medical_background_tuple[1]}', '{patient_medical_background_tuple[2]}',
                                                                    {patient_medical_background_tuple[3]}, {patient_medical_background_tuple[4]}, '{patient_medical_background_tuple[5]}',
                                                                    {patient_medical_background_tuple[6]});
                                        """

    db_connection = create_server_connection(
        host, username, password, database)

    execute_query(db_connection, insert_patient_query)
    execute_query(db_connection, insert_emergency_contact_query)
    execute_query(db_connection, insert_patient_address_query)
    execute_query(db_connection, insert_patient_medical_background_query)

    for disease_name in checked_diseases:
        disease_id = get_disease_id(db_connection, disease_name)
        if disease_id is not None:
            insert_query = f"""
                INSERT INTO PatientFamilyMedicalBackground (PatientID, DiseaseID)
                        VALUES ({patient_id}, {disease_id});
                    """
            execute_query(db_connection, insert_query)

    if all([patient_id, health_insurance_id, provider_name, coverage_plan, coverage_is_under]):
        insert_health_insurance_query = f"""
                                            INSERT INTO HealthInsurance (PatientID, HealthInsuranceID,ProviderName, CoveragePlan, CoverageIsUnder)
                                                        VALUES ('{health_insurance_data[0]}', '{health_insurance_data[1]}', '{health_insurance_data[2]}',
                                                                    {health_insurance_data[3]}, {health_insurance_data[4]});
                                        """

        execute_query(db_connection, insert_health_insurance_query)


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])


with col2:
    patient_info_back_button = st.button(label='Go Back to Patient Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "Patient"
        switch_page("Patient")
