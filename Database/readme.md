# Hosptial Management System Database Schema

# SQL Database 

## 1. Patient Table
- **Primary Key:** Patient ID
- **Unique Key:** Mobile, Email

| Attribute      | Data Type    | Description                         |
|----------------|--------------|-------------------------------------|
| Patient ID     | INT          | Unique identifier for each patient  |
| First Name     | VARCHAR(100) | Patient's first name                |
| Last Name      | VARCHAR(100) | Patient's last name                 |
| Gender         | ENUM         | Patient's gender: Male, Female, Other |
| Mobile         | VARCHAR(100) | Patient's mobile number             |
| Email          | VARCHAR(100) | Patient's email address             |
| DOB            | DATE         | Patient's date of birth             |
| MaritalStatus  | ENUM         | Marital status: Single, Married, Divorced |


## 2. Patient Address Table
- **Primary Key, Foreign Key:** Patient ID

| Attribute   | Data Type             | Description                    |
|-------------|-----------------------|--------------------------------|
| Patient ID  | INT                   | Unique identifier for each patient |
| Address     | VARCHAR(255) NOT NULL | Patient's address             |
| City        | VARCHAR(100) NOT NULL | City of residence             |
| ZipCode     | VARCHAR(10) NOT NULL  | Zip code                      |
| State       | VARCHAR(100) NOT NULL | State or province             |
| Country     | VARCHAR(100) NOT NULL | Country                       |

## 3. Patient Medical Background Table
- **Primary Key, Foreign Key:** Patient ID

| Attribute         | Data Type | Description                                   |
|-------------------|-----------|-----------------------------------------------|
| Patient ID        | INT       | Unique identifier for each patient            |
| Weight            | FLOAT     | Patient's weight                              |
| Blood Group       | ENUM      | Blood type: O-, O+, etc.                      |
| Tobacco Usage     | BOOLEAN   | Indicates tobacco use                         |
| Alcohol Intake    | BOOLEAN   | Indicates alcohol consumption                 |
| Is Diabetic       | BOOLEAN   | Indicates if patient has diabetes             |
| Is Having BP      | BOOLEAN   | Indicates if patient has blood pressure issues|

## 4. Emergency Contact Table
- **Primary Key, Foreign Key:** Patient ID
- **Unique Key:** Email, Mobile Number

| Attribute                  | Data Type    | Description                              |
|----------------------------|--------------|------------------------------------------|
| Patient ID                 | INT          | Unique identifier for each patient       |
| Email                      | VARCHAR(100) | Email of emergency contact               |
| Mobile Number              | VARCHAR(15)  | Mobile number of emergency contact       |
| Relationship to the patient| VARCHAR(50)  | Contact's relationship to the patient    |

### 5. PatientLogin Table
- **Primary Key:** `id`
- **Unique Key:** `email`

| Attribute      | Data Type    | Description                            |
|----------------|--------------|----------------------------------------|
| id             | INT          | Unique identifier for each login       |
| email          | VARCHAR(50)  | Email of the patient                   |
| userpassword   | VARCHAR(256) | Password for the patient               |



## 6. Doctor Department Table
- **Primary Key:** Department ID
- **Unique Key:** Department Name

| Attribute        | Data Type            | Description                           |
|------------------|----------------------|---------------------------------------|
| Department ID    | INT                  | Unique identifier for each department |
| Department Name  | VARCHAR(100) NOT NULL| Name of the department                |

## 7. Doctor Table
- **Primary Key:** Doctor ID
- **Foreign Key:** Department ID

| Attribute            | Data Type             | Description                          |
|----------------------|-----------------------|--------------------------------------|
| Doctor ID            | INT                   | Unique identifier for each doctor    |
| Doctor Name          | VARCHAR(255) NOT NULL | Full name of the doctor              |
| Date of Birth        | DATE                  | Doctor's birth date                  |
| Doctor Gender        | ENUM                  | Doctor's gender: Male, Female, Other |
| Doctor Qualification | VARCHAR(255)          | Doctor's qualifications              |
| Department ID        | INT                   | Identifier for doctor's department   |
| Years of Experience  | SMALL INT             | Years doctor has practiced           |
| Is Active            | BOOLEAN               | If the doctor is currently active    |

## 8. Doctor Consultant Fee Table
- **Primary Key:** Doctor ID
- **Foreign Key:** Doctor ID

| Attribute   | Data Type       | Description                              |
|-------------|-----------------|------------------------------------------|
| Doctor ID   | INT             | Unique identifier for each doctor        |
| Fee Amount  | DECIMAL(10, 2)  | Consultant fee amount charged by the doctor |

## 9. Appointment Table
- **Primary Key:** Appointment ID
- **Foreign Key:** Patient ID, Doctor ID

| Attribute             | Data Type         | Description                       |
|-----------------------|-------------------|-----------------------------------|
| Appointment ID        | INT               | Unique identifier for appointment |
| Patient ID            | INT               | Unique identifier for each patient |
| Doctor ID             | INT               | Unique identifier for each doctor |
| Appointment Date      | DATE NOT NULL     | Date of appointment               |
| Appointment Start Time| TIME NOT NULL     | Start time of appointment         |
| Appointment Status    | VARCHAR(50)       | Status of appointment             |

### 10. DoctorLogin Table
- **Primary Key:** `doctor_id`

| Attribute     | Data Type    | Description                             |
|---------------|--------------|-----------------------------------------|
| doctor_id     | INT          | Unique identifier for each doctor login |
| docpassword    | VARCHAR(256) | Password for the doctor                 |

### 11. Medicine Table
- **Primary Key:** `MedicineID`
- **Unique Key:** `manufacturer_name`

| Attribute           | Data Type      | Description                               |
|---------------------|----------------|-------------------------------------------|
| MedicineID          | INT            | Unique identifier for each medicine       |
| Name                | VARCHAR(255)   | Name of the medicine                      |
| manufacturer_name    | VARCHAR(100)   | Name of the manufacturer                  |
| Price               | DECIMAL(10, 2) | Price of the medicine                     |

### 12. Prescription Table
- **Primary Key:** `PrescriptionID`
- **Foreign Keys:** `PatientID`, `DoctorID`, `MedicineID`, `AppointmentID`

| Attribute          | Data Type    | Description                                 |
|--------------------|--------------|---------------------------------------------|
| PrescriptionID     | INT          | Unique identifier for each prescription     |
| PatientID          | INT          | Unique identifier for the patient           |
| DoctorID           | INT          | Unique identifier for the doctor            |
| MedicineID         | INT          | Unique identifier for the medicine          |
| MedicineDosage     | VARCHAR(255) | Dosage of the medicine                      |
| MedicineDuration    | VARCHAR(255) | Duration for which the medicine is prescribed |
| noOfTablets        | INT          | Number of tablets prescribed                 |
| PrescribedDate     | TIMESTAMP    | Date and time the medicine was prescribed   |
| PrescriptionStatus  | ENUM         | Status of the prescription: Active, Discontinued |
| AppointmentID      | INT          | Unique identifier for the appointment       |

### 13. AdminLogin Table
- **Primary Key:** `username`

| Attribute      | Data Type    | Description                            |
|----------------|--------------|----------------------------------------|
| username       | VARCHAR(255) | Unique username for the admin          |
| adminpassword   | VARCHAR(256) | Password for the admin                 |

### 14. RoomType Table
- **Primary Key:** `RoomTypeID`
- **Unique Key:** `TypeName`

| Attribute       | Data Type    | Description                             |
|-----------------|--------------|-----------------------------------------|
| RoomTypeID      | INT          | Unique identifier for each room type    |
| TypeName        | VARCHAR(100) | Name of the room type                   |
| RoomRent        | INT          | Rent for the room type                  |

### 15. Room Table
- **Primary Key:** `RoomNumber`
- **Unique Key:** `RoomNumber`

| Attribute      | Data Type    | Description                             |
|----------------|--------------|-----------------------------------------|
| RoomNumber     | INT          | Unique identifier for each room         |
| RoomTypeID     | INT          | Identifier for the room type            |
| Status         | ENUM         | Status of the room: Available, Occupied, Maintenance |

### 16. InPatient Table
- **Primary Key:** `InPatientID`
- **Foreign Keys:** `PatientID`, `RoomNumber`

| Attribute      | Data Type    | Description                             |
|----------------|--------------|-----------------------------------------|
| InPatientID    | INT          | Unique identifier for each inpatient     |
| PatientID      | INT          | Unique identifier for the patient        |
| RoomNumber     | INT          | Room number assigned to the inpatient    |
| DateOfAdmission| DATE         | Date of admission to the hospital       |
| DateOfDischarge| DATE         | Date of discharge from the hospital     |

### 17. Pharmacy Table
- **Primary Key, Foreign Key:** `MedicineID`

| Attribute           | Data Type      | Description                              |
|---------------------|----------------|------------------------------------------|
| MedicineID          | INT            | Unique identifier for the medicine       |
| QuantityAvailable    | INT            | Quantity of the medicine available       |
| LastRestocked       | DATE           | Date when the medicine was last restocked |

### 18. RoomRent Table
- **Primary Key, Foreign Keys:** `BillID`, 
- **Foreign Keys:** `InPatientID`, `PatientID`

| Attribute           | Data Type    | Description                             |
|---------------------|--------------|-----------------------------------------|
| BillID              | INT          | Unique identifier for each bill         |
| InPatientID         | INT          | Unique identifier for the inpatient      |
| PatientID           | INT          | Unique identifier for the patient        |
| Stay_Duration       | INT          | Duration of stay in days                |
| TotalRoomRent       | FLOAT        | Total rent for the room                  |
| BillStatus          | ENUM         | Payment status: Paid, Not Paid          |

### 19. LabTest Table
- **Primary Key:** `TestID`

| Attribute      | Data Type      | Description                             |
|----------------|----------------|-----------------------------------------|
| TestID         | INT            | Unique identifier for each lab test     |
| Name           | VARCHAR(255)   | Name of the lab test                    |
| Price          | FLOAT          | Price of the lab test                   |

### 20. Lab Table
- **Primary Key, Foreign Keys:** `LabRecordID`
- **Foreign Keys:** `PatientID`, `ReferredDoctorID`, `TestID`

| Attribute           | Data Type    | Description                             |
|---------------------|--------------|-----------------------------------------|
| LabRecordID         | INT          | Unique identifier for each lab record   |
| PatientID           | INT          | Unique identifier for the patient       |
| ReferredDoctorID    | INT          | Unique identifier for the referred doctor |
| TestID              | INT          | Unique identifier for the test          |
| TestDateTime        | DATETIME     | Date and time the test was performed    |
| TestStatus          | ENUM         | Status of the test: Completed, In Progress |
| BillStatus          | ENUM         | Billing status: Generated, Not Generated |

### 21. LabBill Table
- **Primary Key, Foreign Key:** `BillID`
- **Primary Key, Foreign Key:** `PatientID`

| Attribute        | Data Type    | Description                             |
|------------------|--------------|-----------------------------------------|
| BillID           | INT          | Unique identifier for each lab bill     |
| PatientID        | INT          | Unique identifier for the patient       |
| TotalLabBill     | FLOAT        | Total amount for the lab services       |
| BillStatus       | ENUM         | Payment status: Paid, Not Paid          |


# MongoDB Database 

## Overview

This section outlines the database structure used in the Hospital Management System, focusing on the implementation of MongoDB and its GridFS feature. GridFS is crucial for managing large medical datasets, such as high-resolution images and comprehensive diagnostic reports.

## GridFS Implementation

GridFS in MongoDB addresses the challenges of storing files larger than the BSON document size limit (16MB). It enhances efficiency and scalability by splitting large files into smaller, manageable chunks.

### Key Components of GridFS

1. **fs.files Collection**
   - Contains metadata for each file, including:
     - `_id`: Unique identifier.
     - `filename`: Name of the file.
     - `uploadDate`: Date of file upload.

2. **fs.chunks Collection**
   - Stores the binary chunks of each file.
   - Each chunk is linked to its parent file via a `files_id` field.

This structure enables efficient data transfer and supports concurrent read/write operations, essential in hospital environments.

## Schema Design for 'Lab Reports' Collection

The 'lab reports' collection is a critical component of the database, structured as follows:

- **Patient ID**: Foreign key linking to the patient ID in the SQL database.
- **Tests**: Array of embedded documents, each representing an individual lab test, containing:
  - `Test name`: Name of the lab test.
  - `Test datetime`: Timestamp of the lab test administration.
  - `File id`: Unique identifier for the file in GridFS.

## Advantages in HMS

The integration of GridFS streamlines the workflow in HMS by:
- Facilitating the upload of large files without overburdening the network.
- Allowing clinicians to access and download only necessary parts of a file, enhancing efficiency during patient consultations and treatment planning.
