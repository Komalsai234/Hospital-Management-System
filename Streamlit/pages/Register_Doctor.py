import streamlit as st
from datetime import datetime
from secret.credentials import *
from SQL_connection import create_server_connection, execute_query
from utils import get_department_id
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Register_Doctor'

st.subheader('Register a New Doctor')
doctor_name = st.text_input('Doctor Name', '').strip()
dob = st.date_input('Date of Birth', min_value=datetime(
    1900, 1, 1), max_value=datetime.now())
gender = st.selectbox('Gender', ['', 'Male', 'Female', 'Other'])
qualification = st.text_input('Qualification', '').strip()
department = st.selectbox('Department', ['', 'Cardiology', 'Neurology', 'Oncology',
                          'ENT', 'Orthopedics', 'Dental', 'Gastroenterology', 'Dermatology'])
experience = st.number_input(
    'Years of Experience', min_value=0, max_value=80, step=1)
is_active = st.checkbox('Is Active', value=True)

st.subheader(" ")
submit_button = st.button(label='Submit')

db_connection = create_server_connection(
    host, username, password, database)

if submit_button:
    if not all([doctor_name, dob, gender, qualification, department, experience, is_active]):
        st.error('Please fill out all fields.')
    else:
        doctor_department_id = get_department_id(db_connection, department)

        health_insurance_data = (
            doctor_name, dob, gender, qualification, doctor_department_id, experience, is_active)

        if doctor_department_id is not None:
            insert_doctor_query = f"""
                INSERT INTO Doctor (DoctorName, DateOfBirth, DoctorGender, DoctorQualification, DoctorDepartmentID, YearOfExperience, IsActive)
                VALUES ('{health_insurance_data[0]}', '{health_insurance_data[1]}', '{health_insurance_data[2]}', '{health_insurance_data[3]}', {health_insurance_data[4]}, {health_insurance_data[5]}, {health_insurance_data[6]});
            """

        execute_query(db_connection, insert_doctor_query)

st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to ADMIN Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "ADMIN"
        switch_page("ADMIN")
