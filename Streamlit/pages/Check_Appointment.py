import streamlit as st
import pandas as pd
from secret.credentials import *
from utils import *
from SQL_connection import *
from streamlit_extras.switch_page_button import switch_page

st.title('Doctor\'s Daily Appointments')

st.title(" ")


if st.button('Show Today\'s Appointments'):
    db_connection = create_server_connection(
        host, username, password, database)
    doctor_id = int(st.session_state['doctor_id'])
    appointments = get_todays_appointments_for_doctor(db_connection, doctor_id)

    if appointments:
        appointments_df = pd.DataFrame(appointments, columns=[
            'AppointmentID', 'PatientID', 'AppointmentStartTime', 'AppointmentStatus', 'ReasonForVisit'])

        appointments_df['AppointmentStartTime'] = appointments_df['AppointmentStartTime'].dt.components.hours.astype(
            str).str.zfill(2) + ':' + appointments_df['AppointmentStartTime'].dt.components.minutes.astype(str).str.zfill(2)

        appointments_df = appointments_df.to_html(index=False, border=0)

        st.title("")

        st.markdown(appointments_df, unsafe_allow_html=True)
    else:
        st.info('No appointments scheduled for today.')


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to Doctor Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "Doctor"
        switch_page("Doctor")
