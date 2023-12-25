from pymongo import MongoClient
import gridfs
from pymongo import MongoClient
import streamlit as st
from SQL_connection import create_server_connection, execute_query
from utils import *
from secret.credentials import *
from streamlit_extras.switch_page_button import switch_page

st.title('Patient Lab Reports')

patient_id = int(st.text_input('Enter Patient ID', '0'))

db_connection = create_server_connection(host, username, password, database)

patient_exsist = check_patient_exists(db_connection, patient_id)

if patient_exsist:
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

    st.header('Upload Lab Report')
    uploaded_file = st.file_uploader(
        "Upload File", type=['pdf', 'jpg', 'jpeg', 'png'])

    if st.button('Upload'):
        if uploaded_file is not None:
            file_id = fs.put(uploaded_file, filename=uploaded_file.name)

            patient_data = db.lab_reports.find_one({"patient_id": patient_id})

            test_name_db = list(selected_test.split("-"))[0]

            test_time = lab_dict[test_name_db.strip()]

            if patient_data:
                db.lab_reports.update_one(
                    {"patient_id": patient_id},
                    {"$push": {"tests": {
                        "test_name": test_name_db.strip(),
                        "test_datetime": test_time,
                        "file_id": file_id
                    }}}
                )
            else:
                db.lab_reports.insert_one({
                    "patient_id": patient_id,
                    "tests": [{
                        "test_name": test_name_db.strip(),
                        "test_datetime": test_time,
                        "file_id": file_id
                    }]
                })

            st.success('File uploaded successfully.')
        else:
            st.error('Please provide all required inputs.')

else:
    st.warning("The Patient ID Doesn't Exsist")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to ADMIN Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "ADMIN"
        switch_page("ADMIN")
