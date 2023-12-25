import streamlit as st
from datetime import datetime
from secret.credentials import *
from SQL_connection import create_server_connection, execute_query
from utils import *
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.title('Doctor Prescription')
patient_id = int(st.text_input('Enter Patient ID', '0'))
st.subheader(" ")

db_connection = create_server_connection(
    host, username, password, database)

if check_patient_exists(db_connection, patient_id):
    if patient_id:
        prescription_details = get_patient_prescriptions(
            db_connection, patient_id)

        if prescription_details:
            st.subheader('Latest Appointment and Prescription Details')
            appointments_df = pd.DataFrame(prescription_details, columns=[
                'Appointment ID', 'Appointment Date', 'Prescribed Date', 'Medicine Name', 'Medicine Dosage', 'Medicine Duration', 'Prescription Status'])

            appointments_df = appointments_df.to_html(
                index=False, border=0)

            st.title("")

            st.markdown(appointments_df, unsafe_allow_html=True)

            st.title("")
            st.header("")

            continue_previous = st.checkbox(
                'Continue with the previous prescription?', True)

            if continue_previous:
                st.info("Continuing with the previous Prescription")

            else:
                update_prescription_status(
                    db_connection, patient_id)
                st.success(
                    "Previous prescriptions have been discontinued.")

        medicine_list = get_medicines_list(db_connection)

        medicine_names = ['']+[item[1] for item in medicine_list]

        prescription_entries = []

        st.title("")
        st.header("")

        with st.form(key='prescription_form'):
            st.write("Enter Prescription Details")
            # Create multiple input sets for medicine name, dosage, and duration
            for i in range(5):  # Adjust the range to allow for more or fewer entries
                col1, col2, col3 = st.columns(3)
                with col1:
                    medicine_name = st.selectbox(
                        f'Medicine {i+1}', medicine_names, key=f'medicine_{i}')
                with col2:
                    dosage = st.text_input(
                        f'Dosage {i+1}', key=f'dosage_{i}')
                with col3:
                    duration = st.text_input(
                        f'Duration {i+1}', key=f'duration_{i}')
                # Add the details to the prescription_entries list
                prescription_entries.append(
                    {'medicine_name': medicine_name, 'dosage': dosage, 'duration': duration})

            submit_button = st.form_submit_button(
                label='Submit Prescription')

        if submit_button:

            for entry in prescription_entries:
                if entry['medicine_name'] and entry['dosage'] and entry['duration']:
                    medicine_id = get_medicine_id(
                        db_connection, entry['medicine_name'])

                    prescription_data = (
                        patient_id, medicine_id, entry['dosage'], entry['duration'], prescription_details[0][0])

                    insert_patient_precription(
                        db_connection, prescription_data)

            st.success("Prescription added successfully.")

    else:
        st.warning(
            'No Appointments and Prescriptions found for this patient.')
else:
    st.warning("The Patient Doesn't Exsist")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_prescription_back_button = st.button(
        label='Go Back to Doctor Page')
    if patient_prescription_back_button:
        st.session_state['current_page'] = "Doctor"
        switch_page("Doctor")
