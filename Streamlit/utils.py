from datetime import timedelta
from SQL_connection import execute_query
import streamlit as st
import datetime


def map_boolean_to_string(value):
    return 'Yes' if value == 1 else 'No'


def check_patient_exists(db_connection, patient_id):
    patient_id_query = "SELECT EXISTS(SELECT 1 FROM Patient WHERE PatientID = %s)"

    is_exsist = execute_read_query(
        db_connection, patient_id_query, (patient_id,))
    if is_exsist[0][0]:
        return True
    else:
        return False


def check_doctor_exists(db_connection, doctor_id):
    doctor_id_query = "SELECT EXISTS(SELECT 1 FROM Doctor WHERE DoctorID = %s)"

    is_exsist = execute_read_query(
        db_connection, doctor_id_query, (doctor_id,))
    if is_exsist[0][0]:
        return True
    else:
        return False


def check_existing_bill(connection, inpatient_id):
    query = "SELECT COUNT(*) FROM Bill WHERE InPatientID = %s"
    result = execute_read_query(connection, query, (inpatient_id,))
    return result[0][0] > 0


def get_latest_inpatientid(db_connection, patient_id):
    inpatient_id_query = "SELECT InPatientID FROM InPatient WHERE PatientID = %s ORDER BY DateOfAdmission DESC LIMIT 1"
    inpatient_id = execute_read_query(
        db_connection, inpatient_id_query, (patient_id,))[0][0]

    return inpatient_id


def validate_inpatient_id(connection, inpatient_id, patient_id):
    query = "SELECT COUNT(*) FROM InPatient WHERE InPatientID = %s AND PatientID = %s"
    result = execute_read_query(connection, query, (inpatient_id, patient_id))
    if result[0][0] == 1:
        return True
    else:
        return False


def get_medicine_names(db_connection):
    query = "SELECT Name FROM Medicine"
    results = execute_read_query(db_connection, query, ())
    medicine_names = [result[0] for result in results]

    return medicine_names


def get_disease_id(db_connection, disease_name):
    query = "SELECT DiseaseID FROM Disease WHERE DiseaseName = %s"
    results = execute_read_query(db_connection, query, (disease_name,))

    if results:
        return results[0][0]
    else:
        return None


def get_department_id(db_connection, department_name):
    query = "SELECT DepartmentID FROM DoctorDepartment WHERE DepartmentName = %s"
    results = execute_read_query(db_connection, query, (department_name,))

    if results:
        return results[0][0]
    else:
        return None


def get_test_id(db_connection, test_name):
    query = "SELECT TestID FROM LabTest WHERE Name = %s"
    results = execute_read_query(db_connection, query, (test_name,))

    if results:
        return results[0][0]
    else:
        return None


def get_available_rooms(db_connection, room_type):
    room_number = []
    query = """
            SELECT RoomNumber
            FROM 
                Room r
                JOIN RoomType rt ON r.RoomTypeID = rt.RoomTypeID
            WHERE 
                rt.TypeName = %s AND r.Status = 'Available';
            """
    result = execute_read_query(db_connection, query, (room_type,))
    for results in result:
        room_number.append(results[0])
    return room_number


def get_medicine_stock(connection, search_term):
    search_term_like = f"%{search_term}%"
    query = """
    SELECT m.Name, p.QuantityAvailable, m.manufacturer_name, m.Price
    FROM Medicine m
    INNER JOIN Pharmacy p ON m.MedicineID = p.MedicineID
    WHERE m.Name LIKE %s;
    """
    return execute_read_query(connection, query, (search_term_like,))


def get_medicine_available(db_connection, medicine_id):
    query = "SELECT QuantityAvailable FROM Pharmacy WHERE MedicineID = %s"
    results = execute_read_query(db_connection, query, (medicine_id,))

    if results:
        return results[0][0]
    else:
        return None


def update_stock(connection, medicine_id, quantity):
    query = f"""
    UPDATE Pharmacy
    SET QuantityAvailable = {quantity}
    WHERE MedicineID = {medicine_id}
    """

    return execute_query(connection, query)


def add_medicine(connection, name, description, quantity_in_sheets, price):
    query = """
    INSERT INTO Medicine (Name, Description, QuantityInSheets, Price)
    VALUES (%s, %s, %s, %s);
    """
    return execute_query(connection, query, (name, description, quantity_in_sheets, price))


def get_doctors_id(db_connection, doctor_name):
    doctor_name = doctor_name.split(".")[1].strip()
    doctor_id_query = "SELECT DoctorID FROM Doctor WHERE DoctorName = %s;"
    doctor_id = execute_read_query(
        db_connection, doctor_id_query, (doctor_name,))[0][0]

    return doctor_id


def book_appointment(db_connection, patient_id, doctor_name, appointment_date, selected_slot, reason_for_visit):
    doctor_id = get_doctors_id(db_connection, doctor_name)

    formatted_date = appointment_date.strftime(
        '%Y-%m-%d') if isinstance(appointment_date, datetime.date) else str(appointment_date)

    if isinstance(selected_slot, tuple) and len(selected_slot) > 0:
        selected_slot = selected_slot[0]
    formatted_slot = selected_slot.strftime('%H:%M:%S') if isinstance(
        selected_slot, datetime.time) else str(selected_slot)

    booking_query = f"""
    INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentStartTime, AppointmentStatus, ReasonForVisit)
    VALUES ({patient_id}, {doctor_id}, '{formatted_date}', '{formatted_slot}', 'Scheduled', '{reason_for_visit}');
    """
    execute_query(db_connection, booking_query)


def get_advance_paid(db_connection, patient_id):
    advance_query = "SELECT Advance FROM InPatient WHERE PatientID = %s ORDER BY DateOfAdmission DESC LIMIT 1"
    advance_payment = execute_read_query(
        db_connection, advance_query, (patient_id,))
    advance = advance_payment[0][0] if advance_payment else 0

    return advance


def get_patient_details(db_connection, patient_id):
    patient_info_query = """
    SELECT FirstName, LastName, Gender, DOB, MaritalStatus
    FROM Patient
    WHERE PatientID = %s;
    """
    return execute_read_query(db_connection, patient_info_query, (patient_id,))


def get_patient_medical_info(db_connection, patient_id):
    medical_background_query = """
    SELECT Weight, BloodGroup, TobaccoUsage, AlcoholIntake, IsDiabetic, IsHavingBP
    FROM PatientMedicalBackground
    WHERE PatientID = %s;
    """
    return execute_read_query(db_connection, medical_background_query, (patient_id,))


def get_patient_family_medical_info(db_connection, patient_id):

    family_medical_background_query = """
    SELECT GROUP_CONCAT(DiseaseName SEPARATOR ', ') AS FamilyDiseases
    FROM PatientFamilyMedicalBackground
    JOIN Disease ON PatientFamilyMedicalBackground.DiseaseID = Disease.DiseaseID
    WHERE PatientFamilyMedicalBackground.PatientID = %s
    GROUP BY PatientFamilyMedicalBackground.PatientID;
    """
    return execute_read_query(db_connection, family_medical_background_query, (patient_id,))


def get_todays_appointments_for_doctor(connection, doctor_id):
    today = datetime.now().date()
    query = """
    SELECT AppointmentID, PatientID, AppointmentDate, AppointmentStartTime, AppointmentStatus, ReasonForVisit
    FROM Appointment
    WHERE DoctorID = %s AND AppointmentDate = %s;
    """
    return execute_read_query(connection, query, (doctor_id, today))


def get_todays_appointments_for_doctor(connection, doctor_id):
    query = """
    SELECT AppointmentID, PatientID, AppointmentStartTime, AppointmentStatus, ReasonForVisit
    FROM Appointment
    WHERE DoctorID = %s AND AppointmentDate = CURDATE();
    """
    return execute_read_query(connection, query, (doctor_id,))


def get_medicines_list(db_connection):
    query = "SELECT MedicineID, Name FROM Medicine ORDER BY Name;"
    return execute_query_medcine(db_connection, query)


def get_patient_prescriptions(db_connection, patient_id):
    query = """
    SELECT 
        ap.AppointmentID,
        ap.AppointmentDate,  
        pr.PrescribedDate, 
        m.Name AS MedicineName, 
        pr.MedicineDosage, 
        pr.MedicineDuration, 
        pr.PrescriptionStatus
    FROM 
        Appointment ap
    LEFT JOIN Prescription pr ON ap.AppointmentID = pr.AppointmentID
    LEFT JOIN Medicine m ON pr.MedicineID = m.MedicineID
    WHERE 
        ap.PatientID = %s
    ORDER BY 
        ap.AppointmentDate DESC, pr.PrescribedDate DESC;
    """
    return execute_read_query(db_connection, query, (patient_id,))


def update_prescription_status(db_connection, patient_id):
    status_update_query = f"""
                UPDATE Prescription
                SET PrescriptionStatus = 'Discontinued'
                WHERE PatientID = {patient_id};
            """

    execute_query(db_connection, status_update_query)


def insert_patient_precription(db_connection, prescription_data):
    prescription_insert_query = f"""
        INSERT INTO Prescription (PatientID, MedicineID, MedicineDosage, MedicineDuration, AppointmentID,PrescriptionStatus) 
        VALUES ({prescription_data[0]}, {prescription_data[1]}, '{prescription_data[2]}', '{prescription_data[3]}', {prescription_data[4]},'Active');
    """
    execute_query(db_connection, prescription_insert_query)


def get_medicine_id(db_connection, medicine_name):
    medicine_id_query = f"SELECT MedicineID FROM Medicine WHERE Name = %s"
    medicine_id = execute_read_query(
        db_connection, medicine_id_query, (medicine_name,))[0][0]

    return medicine_id


def get_patient_test_details(db_connection, patient_id):
    lab_test_query = """
    SELECT 
        LT.Name AS TestName, 
        L.TestDateTime
    FROM 
        Lab L
    INNER JOIN 
        LabTest LT ON L.TestID = LT.TestID
    WHERE 
        L.PatientID = %s AND
        L.TestDateTime >= CURDATE() - INTERVAL 730 DAY
    ORDER BY 
        L.TestDateTime DESC
    """
    lab_tests = execute_read_query(
        db_connection, lab_test_query, (patient_id,))

    return lab_tests


def get_medicine_id_for_names(db_connection, medicine_name):
    medicine_id_query = "SELECT MedicineID FROM Medicine WHERE Name = %s"

    try:
        result = execute_read_query(
            db_connection, medicine_id_query, (medicine_name,))

        if result:
            return result[0][0]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def execute_read_query(db_connection, query, params):
    with db_connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_query_medcine(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all rows from the result
        return result
