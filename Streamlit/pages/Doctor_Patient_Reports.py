import base64
from pymongo import MongoClient
import gridfs
from pymongo import MongoClient
import streamlit as st
from SQL_connection import create_server_connection
from utils import *
from secret.credentials import *
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Doctor_Patient_Reports'


st.title('Patient Lab Reports')

patient_id = int(st.text_input('Enter Patient ID', '0'))

db_connection = create_server_connection(host, username, password, database)

if check_patient_exists(db_connection, patient_id):
    lab_tests = get_patient_test_details(db_connection, patient_id)
    lab_dict = dict(lab_tests)

    if lab_tests:
        test_options = [""]+[
            f"{test[0]} - {test[1].strftime('%Y-%m-%d %H:%M:%S')}" for test in lab_tests]
        selected_test = st.selectbox("Select a Lab Test", test_options)

    else:
        st.write("No recent lab tests found for the given Patient ID.")

    client = MongoClient(
        "mongodb+srv://saianurag234:hanuman2004@hms.1pift0p.mongodb.net/?retryWrites=true&w=majority")
    db = client.Hospital_Management
    fs = gridfs.GridFS(db)

    if st.button('Retrieve'):
        if patient_id and selected_test:
            selected_test = list(selected_test.split("-"))[0].strip()
            patient_data = db.lab_reports.find_one(
                {"patient_id": patient_id, "tests.test_name": selected_test})

            if check_patient_exists(db_connection, patient_id):
                for test in patient_data['tests']:
                    if test['test_name'] == selected_test:
                        file_id = test['file_id']
                        break

                if file_id:
                    file_data = fs.get(file_id).read()
                    file_extension = fs.get(
                        file_id).filename.split('.')[-1].lower()
                    st.title(" ")

                    if file_extension in ['jpg', 'jpeg', 'png']:
                        st.image(file_data)
                    elif file_extension == 'pdf':
                        base64_pdf = base64.b64encode(
                            file_data).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.error(
                        'No data found for the given Patient ID and Test Name.')

            else:
                st.warning("The Patient ID Doesn't Exsist")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])
with col2:
    patient_info_back_button = st.button(label='Go Back to Doctor Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "Doctor"
        switch_page("Doctor")
