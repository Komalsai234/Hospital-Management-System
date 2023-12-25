CREATE DATABASE HMS;

USE HMS;

CREATE TABLE Patient (
    PatientID INT UNIQUE PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Mobile VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    DOB DATE,
    MaritalStatus ENUM('Single', 'Married', 'Divorced', 'Widowed')
);


CREATE TABLE EmergencyContact (
    PatientID INT PRIMARY KEY,
    Email VARCHAR(50) UNIQUE,
    MobileNumber VARCHAR(15),
    RelationshipToPatient VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);



CREATE TABLE PatientAddress (
    PatientID INT PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    ZipCode VARCHAR(10) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

CREATE TABLE PatientMedicalBackground (
    PatientID INT PRIMARY KEY,
    Weight FLOAT,
    BloodGroup ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    TobaccoUsage BOOLEAN,
    AlcoholIntake BOOLEAN,
    IsDiabetic BOOLEAN,
    IsHavingBP BOOLEAN,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

CREATE TABLE Disease (
    DiseaseID INT AUTO_INCREMENT PRIMARY KEY,
    DiseaseName VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE PatientFamilyMedicalBackground (
    PatientID INT,
    DiseaseID INT,
    PRIMARY KEY (PatientID, DiseaseID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DiseaseID) REFERENCES Disease(DiseaseID)
);

CREATE TABLE DoctorDepartment (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Doctor (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    DoctorName VARCHAR(255) NOT NULL,
    DateOfBirth DATE,
    DoctorGender ENUM('Male', 'Female', 'Other'),
    DoctorQualification VARCHAR(255),
    DoctorDepartmentID INT,
    YearOfExperience SMALLINT,
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (DoctorDepartmentID) REFERENCES DoctorDepartment(DepartmentID)
);

CREATE TABLE HealthInsurance (
    PatientID INT,
    HealthInsuranceID INT UNIQUE PRIMARY KEY,
    ProviderName VARCHAR(255) NOT NULL,
    CoveragePlan VARCHAR(255),
    CoverageIsUnder VARCHAR(100),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

CREATE TABLE Appointment (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE NOT NULL,
    AppointmentStartTime TIME NOT NULL,
    AppointmentStatus VARCHAR(50),
    ReasonForVisit VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);



CREATE TABLE RoomType (
    RoomTypeID INT AUTO_INCREMENT PRIMARY KEY,
    TypeName VARCHAR(100) NOT NULL UNIQUE,
    RoomRent INT CHECK (RoomRent >= 0)
);


CREATE TABLE Room (
    RoomNumber INT UNIQUE PRIMARY KEY,
    RoomTypeID INT NOT NULL,
    Status ENUM('Available', 'Occupied', 'Maintenance') NOT NULL,
    FOREIGN KEY (RoomTypeID) REFERENCES RoomType(RoomTypeID)
);


CREATE TABLE InPatient (
    InPatientID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    RoomNumber INT NOT NULL,
    DateOfAdmission DATE NOT NULL,
    DateOfDischarge DATE,
    Advance FLOAT CHECK (Advance >= 0), 
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)  
);


CREATE TABLE Bill (
    BillNo INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    InPatientID INT,
    RoomRent FLOAT CHECK (RoomRent >= 0),
    NumberOfDaysRoomOccupancy INT CHECK (NumberOfDaysRoomOccupancy >= 0),
    LabCharge FLOAT CHECK (LabCharge >= 0),
    PaymentMethod ENUM('Cash', 'Credit Card', 'Insurance'),
    TotalBill FLOAT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ,
    FOREIGN KEY (InPatientID) REFERENCES InPatient(InPatientID) 
);


CREATE TABLE Medicine (
    MedicineID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) UNIQUE NOT NULL,
    manufacturer_name VARCHAR(100),
    Price FLOAT CHECK (Price >= 0)
);

CREATE TABLE Prescription (
    PrescriptionID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    MedicineID INT,
    MedicineDosage VARCHAR(255),
    MedicineDuration VARCHAR(255),
    PrescribedDate TIMESTAMP,
    PrescriptionStatus ENUM('Active','Discontinued'),
    AppointmentID INT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    FOREIGN KEY (MedicineID) REFERENCES Medicine(MedicineID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);


CREATE TABLE LabTest (
    TestID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Price FLOAT CHECK (Price >= 0)
);

CREATE TABLE Lab (
    LabRecordID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    ReferredDoctorID INT,
    TestID INT,
    TestDateTime DATETIME NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (ReferredDoctorID) REFERENCES Doctor(DoctorID),
    FOREIGN KEY (TestID) REFERENCES LabTest(TestID)
);

CREATE TABLE Pharmacy (
    MedicineID INT,
    QuantityAvailable INT CHECK (QuantityAvailable >= 0),
    LastRestocked DATE,
    PRIMARY KEY (MedicineID),
    FOREIGN KEY (MedicineID) REFERENCES Medicine(MedicineID)
);

CREATE TABLE Admin_Login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL
);

CREATE TABLE Doctor_Login (
    doctor_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL
);

INSERT INTO Admin_Login (username, password) VALUES ('admin', SHA2('admin@123', 256));

INSERT INTO Doctor_Login (doctor_id, username, password) 
VALUES 
(1,'doctor1', SHA2('doctor@1', 256)),
(2, 'docuser2', SHA2('pass#2', 256)),
(3, 'docuser3', SHA2('pass#3', 256)),
(4, 'docuser4', SHA2('pass#4', 256)),
(5, 'docuser5', SHA2('pass#5', 256)),
(6, 'docuser6', SHA2('pass#6', 256)),
(7, 'docuser7', SHA2('pass#7', 256)),
(8, 'docuser8', SHA2('pass#8', 256)),
(9, 'docuser9', SHA2('pass#9', 256)),
(10, 'docuser10', SHA2('pass#10', 256)),
(11, 'docuser11', SHA2('pass#11', 256)),
(12, 'docuser12', SHA2('pass#12', 256)),
(13, 'docuser13', SHA2('pass#13', 256)),
(14, 'docuser14', SHA2('pass#14', 256)),
(15, 'docuser15', SHA2('pass#15', 256)),
(16, 'docuser16', SHA2('pass#16', 256)),
(17, 'docuser17', SHA2('pass#17', 256)),
(18, 'docuser18', SHA2('pass#18', 256)),
(19, 'docuser19', SHA2('pass#19', 256)),
(20, 'docuser20', SHA2('pass#20', 256)),
(21, 'docuser21', SHA2('pass#21', 256)),
(22, 'docuser22', SHA2('pass#22', 256)),
(23, 'docuser23', SHA2('pass#23', 256)),
(24, 'docuser24', SHA2('pass#24', 256)),
(25, 'docuser25', SHA2('pass#25', 256)),
(26, 'docuser26', SHA2('pass#26', 256)),
(27, 'docuser27', SHA2('pass#27', 256)),
(28, 'docuser28', SHA2('pass#28', 256)),
(29, 'docuser29', SHA2('pass#29', 256)),
(30, 'docuser30', SHA2('pass#30', 256)),
(31, 'docuser31', SHA2('pass#31', 256)),
(32, 'docuser32', SHA2('pass#32', 256)),
(33, 'docuser33', SHA2('pass#33', 256)),
(34, 'docuser34', SHA2('pass#34', 256)),
(35, 'docuser35', SHA2('pass#35', 256)),
(36, 'docuser36', SHA2('pass#36', 256)),
(37, 'docuser37', SHA2('pass#37', 256)),
(38, 'docuser38', SHA2('pass#38', 256)),
(39, 'docuser39', SHA2('pass#39', 256)),
(40, 'docuser40', SHA2('pass#40', 256));
