import streamlit as st
from SQL_connection import create_server_connection
from utils import *
from secret.credentials import *
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Patient_bill'

st.title('Hospital Bill Management')
st.header("")

patient_id = int(st.text_input('Patient ID', '0'))

db_connection = create_server_connection(
    host, username, password, database)

if check_patient_exists(db_connection, patient_id):

    payment_method = st.selectbox(
        'Payment Method', ['', 'Cash', 'Credit Card', 'Insurance'])

    if st.button("Generate Bill"):

        inpatient_id = get_latest_inpatientid(db_connection, patient_id)

        if not check_existing_bill(db_connection, inpatient_id):

            lab_test_summary_query = f"""
                        SELECT 
                            LT.Name AS TestName,
                            COUNT(L.TestID) AS TestCount,
                            SUM(LT.Price) AS TotalCost
                        FROM 
                            Lab L
                        INNER JOIN 
                            LabTest LT ON L.TestID = LT.TestID
                        INNER JOIN 
                            (SELECT 
                                PatientID, 
                                MAX(DateOfAdmission) AS LastAdmissionDate
                            FROM 
                                InPatient
                            WHERE 
                                PatientID = %s
                            GROUP BY 
                                PatientID
                            ) AS RecentStay ON L.PatientID = RecentStay.PatientID
                        WHERE 
                            L.PatientID = %s AND
                            L.TestDateTime >= RecentStay.LastAdmissionDate AND
                            L.TestDateTime <= (SELECT COALESCE(MIN(DateOfDischarge), CURDATE()) FROM InPatient WHERE PatientID = %s AND DateOfAdmission > RecentStay.LastAdmissionDate)
                        GROUP BY 
                            LT.Name;
                        """

            lab_test_summary = execute_read_query(
                db_connection, lab_test_summary_query, (patient_id, patient_id, patient_id))

            df = pd.DataFrame(lab_test_summary, columns=[
                'Test Name', 'Test Count', 'Total Cost'])

            total_cost = (df['Test Count']*df['Total Cost']).sum()

            df.loc[len(df.index)] = ['Total', '', total_cost]

            st.header("Lab Bill")

            st.markdown("""
                            <style>
                    .styled-table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 25px 0;
                        font-size: 0.9em;
                        font-family: Arial, sans-serif;
                        min-width: 400px;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                    }
                    .styled-table thead tr {
                        background-color: #009879; /* Dark teal shade for header */
                        color: #ffffff;
                        text-align: left;
                    }
                    .styled-table th,
                    .styled-table td {
                        padding: 12px 15px;
                        text-align: left;
                    }
                    .styled-table tbody tr {
                        border-bottom: thin solid #dddddd;
                    }
                    .styled-table tbody tr:nth-of-type(even) {
                        background-color: #f3f3f3;
                    }
                    .styled-table tbody tr:last-of-type {
                        background-color: #f9f9f9; /* Light grey for total cost row */
                        color: #333333; /* Darker text for better contrast */
                    }
                    .styled-table tbody tr:last-of-type td {
                        font-weight: bold;
                    }
                    </style>

            """, unsafe_allow_html=True)

            st.write(df.to_html(classes='styled-table', escape=False,
                                index=False), unsafe_allow_html=True)

            room_rent_query = """
                    SELECT 
                        IP.PatientID,
                        R.RoomNumber,
                        RT.TypeName,
                        IP.DateOfAdmission AS LastAdmissionDate,
                        IP.DateOfDischarge AS LastDischargeDate,
                        DATEDIFF(IP.DateOfDischarge, IP.DateOfAdmission) AS StayDuration,
                        RT.RoomRent,
                        (DATEDIFF(IP.DateOfDischarge, IP.DateOfAdmission) * RT.RoomRent) AS TotalRoomRent
                    FROM 
                        InPatient IP
                    JOIN 
                        Room R ON IP.RoomNumber = R.RoomNumber
                    JOIN 
                        RoomType RT ON R.RoomTypeID = RT.RoomTypeID
                    WHERE 
                        IP.PatientID = %s AND IP.DateOfDischarge IS NOT NULL
                    ORDER BY 
                        IP.DateOfAdmission DESC
                    LIMIT 1;
                    """

            room_rent_summary = execute_read_query(
                db_connection, room_rent_query, (patient_id,))

            df_room_rent = pd.DataFrame(room_rent_summary, columns=[
                'PatientID', 'RoomNumber', 'TypeName', 'LastAdmissionDate', 'LastDischargeDate',
                'StayDuration', 'RoomRent', 'TotalRoomRent'])

            df_room_rent.drop(
                ['LastAdmissionDate', 'LastDischargeDate'], axis=1, inplace=True)

            total_room_rent = df_room_rent['TotalRoomRent'].iloc[0]

            stay_duration = df_room_rent['StayDuration'].iloc[0]

            st.header("Room Rent Bill")

            st.markdown("""
                                <style>
                        .styled-table {
                            border-collapse: collapse;
                            width: 100%;
                            margin: 25px 0;
                            font-size: 0.9em;
                            font-family: Arial, sans-serif;
                            min-width: 400px;
                            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                        }
                        .styled-table thead tr {
                            background-color: #009879; /* Dark teal shade for header */
                            color: #ffffff;
                            text-align: left;
                        }
                        .styled-table th,
                        .styled-table td {
                            padding: 12px 15px;
                            text-align: left;
                        }
                        .styled-table tbody tr {
                            border-bottom: thin solid #dddddd;
                        }
                        .styled-table tbody tr:nth-of-type(even) {
                            background-color: #f3f3f3;
                        }
                        .styled-table tbody tr:last-of-type {
                            background-color: #f9f9f9; /* Light grey for total cost row */
                            color: #333333; /* Darker text for better contrast */
                        }
                        .styled-table tbody tr:last-of-type td {
                            font-weight: bold;
                        }
                        </style>

                """, unsafe_allow_html=True)

            st.write(df_room_rent.to_html(classes='styled-table', escape=False,
                                          index=False), unsafe_allow_html=True)

            advance = get_advance_paid(db_connection, patient_id)

            total_bill = total_cost + \
                df_room_rent['TotalRoomRent'].iloc[0] - advance
            st.markdown(f"""
                    <style>
                        .total-bill-container {{
                            padding: 15px;
                            background-color: #f2f2f2;  /* Light grey background */
                            border: 1px solid #ccc;  /* Subtle border */
                            border-radius: 8px;  /* Rounded corners */
                            text-align: center;
                            margin-top: 20px;
                        }}
                        .total-bill-text {{
                            font-size: 1.5em;  /* Larger text */
                            font-weight: bold;
                            color: #333;  /* Dark text color */
                        }}
                    </style>
                    <div class="total-bill-container">
                        <div class="total-bill-text">Total Bill (Net of Advance): Rs { total_bill:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)

            bill_data = (patient_id, inpatient_id, total_room_rent,
                         stay_duration, total_cost, payment_method, total_bill)
            insert_bill_query = f"""
                INSERT INTO Bill (PatientID, InPatientID, RoomRent, NumberOfDaysRoomOccupancy, LabCharge, PaymentMethod, TotalBill)
                VALUES ('{bill_data[0]}','{bill_data[1]}','{bill_data[2]}','{bill_data[3]}','{bill_data[4]}','{bill_data[5]}','{bill_data[6]}')
                """
            execute_query(db_connection, insert_bill_query)
            st.header("")
            st.success('Bill Generated Successfully')

        else:
            st.error(
                "A bill has already been generated for this patient's most recent hospital stay.")


else:
    st.warning("The Patient Doesn't Exsist")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    patient_info_back_button = st.button(label='Go Back to ADMIN Page')
    if patient_info_back_button:
        st.session_state['current_page'] = "ADMIN"
        switch_page("ADMIN")
