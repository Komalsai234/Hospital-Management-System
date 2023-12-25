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

## 2. Emergency Contact Table
- **Primary Key, Foreign Key:** Patient ID
- **Unique Key:** Email, Mobile Number

| Attribute                  | Data Type    | Description                              |
|----------------------------|--------------|------------------------------------------|
| Patient ID                 | INT          | Unique identifier for each patient       |
| Email                      | VARCHAR(100) | Email of emergency contact               |
| Mobile Number              | VARCHAR(15)  | Mobile number of emergency contact       |
| Relationship to the patient| VARCHAR(50)  | Contact's relationship to the patient    |

## 3. Patient Address Table
- **Primary Key, Foreign Key:** Patient ID

| Attribute   | Data Type             | Description                    |
|-------------|-----------------------|--------------------------------|
| Patient ID  | INT                   | Unique identifier for each patient |
| Address     | VARCHAR(255) NOT NULL | Patient's address             |
| City        | VARCHAR(100) NOT NULL | City of residence             |
| ZipCode     | VARCHAR(10) NOT NULL  | Zip code                      |
| State       | VARCHAR(100) NOT NULL | State or province             |
| Country     | VARCHAR(100) NOT NULL | Country                       |

## 4. Patient Medical Background Table
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

## 5. Disease Table
- **Primary Key:** Disease ID
- **Unique Key:** Disease Name

| Attribute     | Data Type   | Description                          |
|---------------|-------------|--------------------------------------|
| Disease ID    | INT         | Unique identifier for each disease   |
| Disease Name  | VARCHAR(255)| Name of the disease                  |

## 6. Patient Family Medical Background Table
- **Primary Key:** Patient ID, Disease ID
- **Foreign Key:** Patient ID, Disease ID

| Attribute  | Data Type | Description                           |
|------------|-----------|---------------------------------------|
| Patient ID | INT       | Unique identifier for each patient    |
| Disease ID | INT       | Unique identifier for each disease entry |

## 7. Doctor Department Table
- **Primary Key:** Department ID
- **Unique Key:** Department Name

| Attribute        | Data Type            | Description                           |
|------------------|----------------------|---------------------------------------|
| Department ID    | INT                  | Unique identifier for each department |
| Department Name  | VARCHAR(100) NOT NULL| Name of the department                |

## 8. Doctor Table
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

## 9. Health Insurance Table
- **Primary Key:** Health Insurance ID
- **Foreign Key:** Patient ID

| Attribute       | Data Type            | Description                      |
|-----------------|----------------------|----------------------------------|
| Patient ID      | INT                  | Unique identifier for each patient |
| Health Insurance ID | INT              | Unique identifier for insurance record |
| Provider Name   | VARCHAR(255) NOT NULL| Name of health insurance provider|
| Coverage Plan   | VARCHAR(255)         | Details of insurance coverage    |
| Coverage Is Under | VARCHAR(100)      | Identifier for insurance department |

## 10. Appointment Table
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
| Reason For Visit      | VARCHAR(50)       | Reason for patient's visit        |

## 11. Room Type Table
- **Primary Key:** Room Type ID
- **Unique Key:** Room Type Name

| Attribute       | Data Type        | Description                      |
|-----------------|------------------|----------------------------------|
| Room Type ID    | INT              | Unique identifier for room type  |
| Room Type Name  | VARCHAR(100) NOT NULL | Name of room type             |
| Room Rent       | INT              | Cost of the room per day         |

## 12. Room Table
- **Primary Key:** Room Number
- **Foreign Key:** Room Type ID

| Attribute    | Data Type             | Description                    |
|--------------|-----------------------|--------------------------------|
| Room Number  | INT                   | Unique identifier for each room|
| Room Type ID | VARCHAR(100) NOT NULL | Name of room type              |
| Status       | ENUM                  | Status of the room             |

## 13. In-Patient Table
- **Primary Key:** In-Patient ID
- **Foreign Key:** Patient ID, Room Number

| Attribute        | Data Type       | Description                        |
|------------------|-----------------|------------------------------------|
| In-patient ID    | INT             | Unique identifier for each inpatient admission |
| Patient ID       | INT             | Unique identifier for each patient |
| Room Number      | INT             | Unique identifier for each room    |
| Date of Admission| DATE NOT NULL   | Date of patient admission          |
| Date of Discharge| DATE            | Date of patient discharge          |
| Advance          | FLOAT           | Advance payment at admission       |
| Reason For Visit | VARCHAR(50)     | Reason for patient's visit         |

## 14. Bill Table
- **Primary Key:** Bill No
- **Foreign Key:** Patient ID, In-Patient ID

| Attribute                  | Data Type  | Description                    |
|----------------------------|------------|--------------------------------|
| Bill No                    | INT        | Unique identifier for bill     |
| Patient ID                 | INT        | Unique identifier for each patient |
| In-patient ID              | INT        | Unique identifier for each inpatient admission |
| Room Rent                  | FLOAT      | Total cost of room rent        |
| Number of days room occupancy | INT     | Number of days room was occupied |
| Lab Charge                 | FLOAT      | Charges for lab tests          |
| Payment Method             | ENUM       | Payment method used            |
| Total Bill                 | FLOAT      | Total amount of the bill       |

## 15. Medicine Table
- **Primary Key:** Medicine ID
- **Unique Key:** Medicine Name

| Attribute        | Data Type            | Description                     |
|------------------|----------------------|---------------------------------|
| Medicine ID      | INT                  | Unique identifier for each medicine |
| Medicine Name    | VARCHAR(255) NOT NULL| Name of the medicine             |
| Manufacturer Name| VARCHAR(100)         | Name of medicine manufacturer    |
| Price            | FLOAT                | Price per unit of medicine       |

## 16. Prescription Table
- **Primary Key:** Prescription ID
- **Foreign Key:** Patient ID, Doctor ID, Medicine ID, Appointment ID

| Attribute           | Data Type          | Description                                  |
|---------------------|--------------------|----------------------------------------------|
| Prescription ID     | INT                | Unique identifier for each prescription      |
| Patient ID          | INT                | Unique identifier for each patient           |
| Doctor ID           | INT                | Unique identifier for each doctor            |
| Medicine ID         | INT                | Unique identifier for each medicine          |
| Medicine Dosage     | VARCHAR(255)       | Dosage of the prescribed medicine            |
| Medicine Duration   | VARCHAR(255)       | Duration for taking the medicine             |
| Prescribed Date     | TIME STAMP         | Date and time when the prescription was made |
| Prescription Status | ENUM               | Status of the prescription: Active, etc.     |
| Appointment ID      | INT                | Identifier for the related appointment       |

## 17. Lab Test Table
- **Primary Key:** Test ID

| Attribute   | Data Type | Description                       |
|-------------|-----------|-----------------------------------|
| Test ID     | INT       | Unique identifier for each lab test|
| Test Name   | INT       | Name of the lab test              |
| Price       | FLOAT     | Cost of the lab test              |

## 18. Lab Table
- **Primary Key:** Lab Record ID
- **Foreign Key:** Patient ID, Referred Doctor ID, Test ID

| Attribute         | Data Type     | Description                                    |
|-------------------|---------------|------------------------------------------------|
| Lab Record ID     | INT           | Unique identifier for each lab record          |
| Patient ID        | INT           | Unique identifier for each patient             |
| Referred Doctor ID| INT           | Identifier for the doctor referring the test   |
| Test ID           | INT           | Unique identifier for each test                |
| Test Date Time    | DATE NOT NULL | Date and time when the lab test was conducted  |

## 19. Pharmacy Table
- **Primary Key, Foreign Key:** Medicine ID

| Attribute           | Data Type | Description                            |
|---------------------|-----------|----------------------------------------|
| Medicine ID         | INT       | Unique identifier for each medicine    |
| Quantity Available  | INT       | Stock quantity of the medicine         |
| Last Restocked      | DATE      | Most recent restock date of the medicine|





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
