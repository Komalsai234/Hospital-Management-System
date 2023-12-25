import streamlit as st
from SQL_connection import create_server_connection, execute_query
import datetime
from secret.credentials import *
from utils import *
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Room'


st.title('Hospital Room Management')

st.subheader('Room Availability Summary')
room_type = st.selectbox('Select the Room Type', [
                         '', 'Standard', 'Deluxe', 'Suite', 'Executive', 'General-Ward'])

db_connection = create_server_connection(
    host, username, password, database)

if st.button('Check Room Availability'):
    if room_type:
        room_numbers = get_available_rooms(db_connection, room_type)

        if room_numbers:
            st.subheader(f"Total available rooms: {len(room_numbers)}")
            room_numbers_str = ', '.join(
                [str(number) for number in room_numbers])
            st.text(f"Available Room Numbers: {room_numbers_str}")
        else:
            st.subheader("No available rooms for the selected room type.")
    else:
        st.warning("Please select a room type to check availability.")


st.header("")

st.subheader('Admit a Patient')
patient_id_admit = int(st.text_input('Enter Patient ID', '0'))
selected_room_type = st.selectbox('Select Room Type', [
    '', 'Standard', 'Deluxe', 'Suite', 'Executive', 'General-Ward'])

if selected_room_type:
    room_numbers = get_available_rooms(db_connection, selected_room_type)
    room_number_admit = st.selectbox(
        "Select the Room number", ['']+room_numbers)
admit_date = st.date_input(
    'Date of Admission', value=datetime.datetime.now().date())
advance_payment = float(st.number_input(
    'Advance Payment', min_value=0.0, step=0.01))


if st.button('Admit Patient'):
    if check_patient_exists(db_connection, patient_id_admit):
        admit_date = admit_date.strftime(
            '%Y-%m-%d') if isinstance(admit_date, datetime.date) else str(admit_date)
        admit_patient_data = (
            patient_id_admit, room_number_admit, admit_date, advance_payment)
        admit_query = f"""
        INSERT INTO InPatient (PatientID, RoomNumber, DateOfAdmission, Advance)
        VALUES ('{admit_patient_data[0]}', '{admit_patient_data[1]}', '{admit_patient_data[2]}', '{admit_patient_data[3]}');
        """
        execute_query(db_connection, admit_query)
        st.success("Patient Admitted Successfully")

    else:
        st.error("The Patient Information Doesn't exsist for given ID")

st.header("")
st.subheader('Discharge a Patient')
patient_id = int(st.text_input('Patient ID', '0'))
inpatient_id_discharge = int(st.text_input(
    'Enter In-Patient ID for Discharge', '0'))

discharge_date = st.date_input(
    'Date of Discharge', value=datetime.datetime.now().date())

if st.button('Discharge Patient'):
    if validate_inpatient_id(db_connection, patient_id, inpatient_id_discharge):
        admit_date = admit_date.strftime(
            '%Y-%m-%d') if isinstance(admit_date, datetime.date) else str(admit_date)
        discharge_query = f"UPDATE InPatient SET DateOfDischarge = '{discharge_date}' WHERE InPatientID = {inpatient_id_discharge}"
        execute_query(db_connection, discharge_query)
        st.success("Patient discharged successfully.")
    else:
        st.error("Please enter a valid In-Patient ID.")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to ADMIN Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "ADMIN"
        switch_page("ADMIN")
