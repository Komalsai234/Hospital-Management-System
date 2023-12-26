import pandas as pd
from mysql.connector import Error
import mysql.connector
from faker import Faker
import random
from datetime import datetime, time, timedelta, date

fake = Faker('en_IN')


def generate_unique_data(n, data_type):
    unique_data = set()
    while len(unique_data) < n:
        if data_type == 'email':
            unique_data.add(fake.email())
        elif data_type == 'phone':
            phone_number = '+91' + fake.msisdn()[-10:]
            unique_data.add(phone_number)
    return list(unique_data)


def generate_patient_data(num_patients):
    emails = generate_unique_data(num_patients, 'email')
    phone_numbers = generate_unique_data(num_patients, 'phone')

    patients = []
    for i in range(num_patients):
        gender = random.choice(['Male', 'Female'])

        if gender == 'Male':
            first_name = fake.first_name_male()
        elif gender == 'Female':
            first_name = fake.first_name_female()

        patient = (
            i + 1,
            first_name,
            fake.last_name(),
            gender,
            phone_numbers[i],
            emails[i],
            fake.date_of_birth(minimum_age=0, maximum_age=115),
            random.choice(['Single', 'Married', 'Divorced'])
        )
        patients.append(patient)
    return patients


def generate_emergency_contact_data(patients):
    emergency_contact_emails = generate_unique_data(len(patients), 'email')
    emergency_contact_phones = generate_unique_data(len(patients), 'phone')

    emergency_contacts = []
    for i, patient in enumerate(patients):
        contact = (
            patient[0],
            emergency_contact_emails[i],
            emergency_contact_phones[i],
            fake.random_element(
                elements=('Parent', 'Sibling', 'Spouse', 'Friend', 'Other'))
        )
        emergency_contacts.append(contact)
    return emergency_contacts


def generate_patient_address_data(patients):
    patient_addresses = []
    for patient in patients:
        address = (
            patient[0],
            fake.street_address(),
            fake.city(),
            fake.state(),
            'India'
        )
        patient_addresses.append(address)
    return patient_addresses


def generate_patient_medical_background_data(patients):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    patient_medical_backgrounds = []
    for patient in patients:
        medical_background = (
            patient[0],
            round(random.uniform(40.0, 120.0), 1),
            random.choice(blood_groups),
            fake.boolean(),
            fake.boolean(),
            fake.boolean(),
            fake.boolean()
        )
        patient_medical_backgrounds.append(medical_background)
    return patient_medical_backgrounds


departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology', 'Radiology',
               'ENT', 'Dermatology', 'Dental', 'Endocrinology', 'Gastroenterology', 'Nephrology']


def generate_doctor_department_data():
    return [(i + 1, dept) for i, dept in enumerate(departments)]


def generate_doctor_data(num_doctors):
    names = [fake.name() for _ in range(num_doctors)]
    qualifications = [random.choice(['MBBS', 'MD', 'MS', 'PhD'])
                      for _ in range(num_doctors)]
    experiences = [random.randint(1, 45) for _ in range(num_doctors)]

    doctors = []
    for i in range(num_doctors):
        min_education_age = 25
        min_age = min_education_age + experiences[i]
        max_age = 70

        dob = fake.date_of_birth(minimum_age=max(
            0, date.today().year - max_age), maximum_age=max(0, date.today().year - min_age))

        doctor = (i + 1, names[i], dob, random.choice(['Male', 'Female']),
                  qualifications[i], random.randint(1, len(departments)), experiences[i], True)
        doctors.append(doctor)
    return doctors


def generate_disease_data():

    diseases_list = [
        'Mental Health Disorder',
        'Colon Cancer',
        'Prostate Cancer',
        'Uterine Cancer',
        'Breast Cancer',
        'Lung Cancer',
        'Diabetes',
        'High Blood Pressure',
        'High Cholesterol',
        'Heart Disease',
        'Kidney Disease',
        'Alcohol Issues',
        'Thyroid Disorders',
        'Asthma',
        'Osteoporosis',
        'Arthritis',
        'COPD (Chronic Obstructive Pulmonary Disease)',
        'Peptic Ulcer Disease',
        'Pancreatic Cancer',
        'Hepatitis'
    ]

    disease_data = [(i + 1, disease)
                    for i, disease in enumerate(diseases_list)]
    return disease_data


def generate_patient_family_medical_background_data(patients, diseases):
    patient_family_medical_backgrounds = []
    for patient in patients:
        num_diseases = random.randint(0, len(diseases))
        patient_diseases = random.sample(diseases, num_diseases)

        for disease in patient_diseases:
            record = (
                patient[0],
                disease[0]
            )
            patient_family_medical_backgrounds.append(record)

    return patient_family_medical_backgrounds


def generate_health_insurance_data(patients):
    provider_names = [
        'Apollo Munich Health Insurance', 'Max Bupa Health Insurance',
        'ICICI Lombard General Insurance', 'Religare Health Insurance',
        'Star Health and Allied Insurance', 'HDFC ERGO General Insurance',
        'New India Assurance', 'Oriental Insurance Company',
        'United India Insurance', 'National Insurance Company',
        'Bajaj Allianz General Insurance', 'SBI Health Insurance',
        'Tata AIG General Insurance', 'Bharti AXA General Insurance',
        'Future Generali India Insurance', 'IFFCO Tokio General Insurance',
        'Reliance General Insurance', 'Universal Sompo General Insurance',
        'Aetna Health Insurance', 'Cigna TTK'
    ]
    coverage_plans = ['Basic', 'Standard', 'Premium', 'Family', 'Individual']
    coverage_is_under = ['Self', 'Spouse', 'Parent', 'Employer']

    health_insurance_data = []
    for patient in patients:
        health_insurance_record = (
            patient[0],
            fake.unique.random_int(min=1, max=1000000),
            random.choice(provider_names),
            random.choice(coverage_plans),
            random.choice(coverage_is_under)
        )
        health_insurance_data.append(health_insurance_record)

    return health_insurance_data


num_room_types = 5

room_types = [('Standard', 1000), ('Deluxe', 2000),
              ('Suite', 3000), ('Executive', 2500), ('General-Ward', 800)]


def generate_room_data(num_rooms, num_room_types):
    room_statuses = ['Available', 'Occupied', 'Maintenance']
    room_data = []

    for i in range(1, num_rooms + 1):
        room = (i, random.randint(1, num_room_types),
                random.choice(room_statuses))
        room_data.append(room)

    return room_data


def generate_appointment_data(patients, doctors, start_date, end_date, max_appointments_per_patient):
    appointment_data = []
    reasons_for_visit = ['Consultation',
                         'Routine Check', 'Emergency', 'General Checkup']

    appointment_slots = ['10:00', '10:30', '11:00', '11:30',
                         '12:00', '14:00', '14:30', '15:00', '15:30', '16:00']

    for patient in patients:
        patient_id = patient[0]
        num_appointments = random.randint(1, max_appointments_per_patient)

        for _ in range(num_appointments):
            doctor_id = random.choice(doctors)[0]
            random_date = start_date + \
                timedelta(days=random.randint(0, (end_date - start_date).days))
            random_slot = random.choice(appointment_slots)

            appointment_status = 'Cancelled' if random.random() < 0.05 else random.choice([
                'Scheduled'])

            appointment = (
                patient_id,
                doctor_id,
                random_date.strftime('%Y-%m-%d'),
                random_slot,
                appointment_status,
                random.choice(reasons_for_visit)
            )
            appointment_data.append(appointment)

    return appointment_data


def generate_inpatient_data(patients, rooms, percentage_admitted):
    inpatient_data = []
    advance_payment_choices = [500, 750, 1000, 1500, 2000, 5000, 10000]

    cutoff_date = datetime(2023, 12, 7).date()

    occupied_rooms = [room[0] for room in rooms if room[2] == 'Occupied']

    admitted_patients = random.sample(
        patients, int(len(patients) * percentage_admitted))

    for patient in admitted_patients:
        patient_id = patient[0]
        date_of_admission = fake.date_between(
            start_date='-2y', end_date='today')

        if date_of_admission >= cutoff_date:
            date_of_discharge = None
            if not occupied_rooms:
                continue
            room_number = random.choice(occupied_rooms)
            occupied_rooms.remove(room_number)
        else:
            available_rooms = [room[0] for room in rooms if room[2] not in [
                'Maintenance', 'Occupied']]
            if not available_rooms:
                continue
            room_number = random.choice(available_rooms)
            discharge_days = random.randint(1, 10)
            date_of_discharge = date_of_admission + \
                timedelta(days=discharge_days)

        inpatient_record = (
            patient_id,
            room_number,
            date_of_admission.strftime('%Y-%m-%d'),
            date_of_discharge.strftime(
                '%Y-%m-%d') if date_of_discharge else None,
            random.choice(advance_payment_choices)
        )
        inpatient_data.append(inpatient_record)

    return inpatient_data


def initialize_room_availability(rooms):
    return {room[0]: None for room in rooms}


def generate_lab_data(patients, doctors, num_records):
    lab_data = []
    test_ids = range(1, 21)
    frequent_test_ids = [1, 2]

    for _ in range(num_records):
        patient_id = random.choice(patients)[0]
        doctor_id = random.choice(doctors)[0]
        test_id = random.choice(test_ids)

        if test_id in frequent_test_ids:
            date = fake.date_between(start_date='-1y', end_date='today')
            times_a_day = random.randint(1, 3)
            for _ in range(times_a_day):
                test_time = datetime.combine(date, fake.time_object())
                lab_record = (patient_id, doctor_id, test_id,
                              test_time.strftime('%Y-%m-%d %H:%M:%S'))
                lab_data.append(lab_record)
        else:
            test_date_time = fake.date_time_between(
                start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            lab_record = (patient_id, doctor_id, test_id, test_date_time)
            lab_data.append(lab_record)

    return lab_data


def generate_lab_data(patients, inpatient_data, doctors, num_records):
    lab_data = []
    test_ids = range(1, 21)
    frequent_test_ids = [1, 2]

    inpatient_patient_ids = {record[0] for record in inpatient_data}

    for patient_id in inpatient_patient_ids:
        create_lab_record(patient_id, doctors, lab_data,
                          test_ids, frequent_test_ids)
    non_inpatient_patients = [
        p for p in patients if p[0] not in inpatient_patient_ids]
    additional_patients = random.sample(
        non_inpatient_patients, num_records - len(inpatient_patient_ids))

    for patient in additional_patients:
        patient_id = patient[0]
        create_lab_record(patient_id, doctors, lab_data,
                          test_ids, frequent_test_ids)

    return lab_data


def create_lab_record(patient_id, doctors, lab_data, test_ids, frequent_test_ids):
    test_id = random.choice(test_ids)

    if test_id in frequent_test_ids:
        date = fake.date_between(start_date='-1y', end_date='today')
        times_a_day = random.randint(1, 3)
        for _ in range(times_a_day):
            test_time = datetime.combine(date, fake.time_object())
            lab_record = (patient_id, random.choice(doctors)[
                          0], test_id, test_time.strftime('%Y-%m-%d %H:%M:%S'))
            lab_data.append(lab_record)
    else:
        test_date_time = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        lab_record = (patient_id, random.choice(
            doctors)[0], test_id, test_date_time)
        lab_data.append(lab_record)


def connect_fetch_data():
    try:
        connection = mysql.connector.connect(
            host='your-mysql-endpoint',
            database='your-database-name',
            user='your-username',
            password='your-passsword'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM Appointment"
            cursor.execute(query)

            result_list = cursor.fetchall()

            return result_list

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


appointments = connect_fetch_data()


def generate_prescription_data(appointments):
    prescription_data = []
    dosage_options = ['1 Time', '2 Time']
    duration_options = ['1 day', '2 days', '3 days',
                        '5 days', '6 days', '15 days', '30 days']
    prescription_statuses = ['Active', 'Discontinued']

    for appointment in appointments:
        appointment_id, patient_id, doctor_id, appointment_date, slot, status, reason = appointment
        medicine_id = random.randint(1, 5000)
        dosage = random.choice(dosage_options)
        duration = random.choice(duration_options)
        prescription_status = random.choice(prescription_statuses)

        prescription_record = (
            patient_id,
            doctor_id,
            medicine_id,
            dosage,
            duration,
            appointment_date,
            prescription_status,
            appointment_id
        )
        prescription_data.append(prescription_record)

    return prescription_data


def generate_pharmacy_data(num_medicines):
    pharmacy_data = []
    today = datetime.today().date()
    one_week_ago = today - timedelta(days=7)

    for medicine_id in range(1, num_medicines + 1):
        quantity_available = random.randint(0, 100)
        last_restocked = fake.date_between(
            start_date=one_week_ago, end_date=today).strftime('%Y-%m-%d')

        pharmacy_record = (
            medicine_id,
            quantity_available,
            last_restocked
        )
        pharmacy_data.append(pharmacy_record)

    return pharmacy_data


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_bulk_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        connection.commit()
        print("Bulk query successful")
    except Error as err:
        print(f"Error: '{err}'")


host = 'your-mysql-endpoint'
database = 'your-database-name'
user = 'your-username'
password = 'your-passsword'

connection = create_db_connection(host, user, password, database)


def chunk_data(data, chunk_size):
    """Yield successive chunk_size chunks from data."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


insert_patient_query = """
INSERT INTO Patient (PatientID, FirstName, LastName, Gender, Mobile, Email, DOB, MaritalStatus)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
insert_emergency_contact_query = """
INSERT INTO EmergencyContact (PatientID, Email, MobileNumber, RelationshipToPatient)
VALUES (%s, %s, %s, %s);
"""

insert_patient_address_query = """
INSERT INTO PatientAddress (PatientID, Address, City, State, Country)
VALUES (%s, %s, %s, %s, %s);
"""

insert_patient_medical_background_query = """
INSERT INTO PatientMedicalBackground (PatientID, Weight, BloodGroup, TobaccoUsage, AlcoholIntake, IsDiabetic, IsHavingBP)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

insert_doctor_department_query = """
INSERT INTO DoctorDepartment (DepartmentID, DepartmentName)
VALUES (%s, %s);
"""

insert_doctor_query = """
INSERT INTO Doctor (DoctorID, DoctorName, DateOfBirth, DoctorGender, DoctorQualification, DoctorDepartmentID, YearOfExperience, IsActive)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
insert_disease_query = """
INSERT INTO Disease (DiseaseID, DiseaseName)
VALUES (%s, %s);
"""

insert_patient_family_medical_background_query = """
INSERT INTO PatientFamilyMedicalBackground (PatientID, DiseaseID)
VALUES (%s, %s);
"""

insert_health_insurance_query = """
INSERT INTO HealthInsurance (PatientID, HealthInsuranceID, ProviderName, CoveragePlan, CoverageIsUnder)
VALUES (%s, %s, %s, %s, %s);
"""

insert_room_type_query = """
INSERT INTO RoomType (TypeName, RoomRent)
VALUES (%s, %s);
"""

insert_room_query = """
INSERT INTO Room (RoomNumber, RoomTypeID, Status)
VALUES (%s, %s, %s);
"""

insert_appointment_query = """
INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentStartTime, AppointmentStatus, ReasonForVisit)
VALUES (%s, %s, %s, %s, %s, %s);
"""

insert_inpatient_query = """
INSERT INTO InPatient (PatientID, RoomNumber, DateOfAdmission, DateOfDischarge, Advance)
VALUES (%s, %s, %s, %s, %s);
"""

insert_lab_query = """
INSERT INTO Lab (PatientID, ReferredDoctorID, TestID, TestDateTime)
VALUES (%s, %s, %s, %s);
"""

insert_medicine_query = """
INSERT INTO Medicine (Name, manufacturer_name, Price)
VALUES (%s, %s, %s);
"""

insert_prescription_query = """
INSERT INTO Prescription (PatientID, DoctorID, MedicineID, MedicineDosage, MedicineDuration, PrescribedDate, PrescriptionStatus, AppointmentID)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

insert_pharmacy_query = """
INSERT INTO Pharmacy (MedicineID, QuantityAvailable, LastRestocked)
VALUES (%s, %s, %s);
"""

# Generate and insert data into table in MYSQL Database using above defined functions

num_patients = 5500
patients = generate_patient_data(num_patients)
emergency_contacts = generate_emergency_contact_data(patients)
patient_addresses = generate_patient_address_data(patients)
patient_medical_backgrounds = generate_patient_medical_background_data(
    patients)

num_doctors = 40
doctor_departments = generate_doctor_department_data()
doctors = generate_doctor_data(num_doctors)


diseases = generate_disease_data()

patient_family_medical_backgrounds = generate_patient_family_medical_background_data(
    patients, diseases)

health_insurance_data = generate_health_insurance_data(patients)

num_rooms = 50
rooms = generate_room_data(num_rooms, num_room_types)


start_date = datetime(2021, 12, 10)
end_date = datetime.today()

max_appointments_per_patient = 4

appointments = generate_appointment_data(
    patients, doctors, start_date, end_date, max_appointments_per_patient)

room_availability = initialize_room_availability(rooms)
percentage_of_patients_admitted = 0.5
inpatients = generate_inpatient_data(
    patients, rooms, percentage_of_patients_admitted)

lab_records = generate_lab_data(patients, inpatients, doctors, 3500)

df = pd.read_excel('path to\\medicines.xlsx')
random_rows = df.sample(n=5000)
medicine_data = list(random_rows.itertuples(index=False, name=None))

prescriptions = generate_prescription_data(appointments)
num_medicines = 5000
pharmacy_inventory = generate_pharmacy_data(num_medicines)


for patient in patients:
    execute_bulk_query(connection, insert_patient_query, patient)
for contact in emergency_contacts:
    execute_bulk_query(connection, insert_emergency_contact_query, contact)
for chunk in chunk_data(patient_addresses, 200):
    execute_bulk_query(connection, insert_patient_address_query, chunk)
for chunk in chunk_data(patient_medical_backgrounds, 100):
    execute_bulk_query(
        connection, insert_patient_medical_background_query, chunk)
for chunk in chunk_data(doctor_departments, 100):
    execute_bulk_query(connection, insert_doctor_department_query, chunk)
for chunk in chunk_data(doctors, 100):
    execute_bulk_query(connection, insert_doctor_query, chunk)
for chunk in chunk_data(diseases, 100):
    execute_bulk_query(connection, insert_disease_query, chunk)

for chunk in chunk_data(patient_family_medical_backgrounds, 100):
    execute_bulk_query(
        connection, insert_patient_family_medical_background_query, chunk)
for chunk in chunk_data(health_insurance_data, 100):
    execute_bulk_query(connection, insert_health_insurance_query, chunk)
for chunk in chunk_data(room_types, 100):
    execute_bulk_query(connection, insert_room_type_query, chunk)
for chunk in chunk_data(rooms, 100):
    execute_bulk_query(connection, insert_room_query, chunk)

for chunk in chunk_data(appointments, 100):
    execute_bulk_query(connection, insert_appointment_query, chunk)
for chunk in chunk_data(inpatients, 100):
    execute_bulk_query(connection, insert_inpatient_query, chunk)

none_discharge_count = 0
for inpatient in inpatients:
    if inpatient[3] is None:
        print(inpatient)
        none_discharge_count += 1
print(
    f"Number of inpatients with 'None' as discharge date: {none_discharge_count}")

for chunk in chunk_data(lab_records, 100):
    execute_bulk_query(connection, insert_lab_query, chunk)

for chunk in chunk_data(medicine_data, 100):
    execute_bulk_query(connection, insert_medicine_query, chunk)

for chunk in chunk_data(prescriptions, 100):
    execute_bulk_query(connection, insert_prescription_query, chunk)

for chunk in chunk_data(pharmacy_inventory, 100):
    execute_bulk_query(connection, insert_pharmacy_query, chunk)


if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")
