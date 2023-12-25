
# Hospital Management System
![Logo](https://www.startlazaa.com/wp-content/uploads/hospital-management-software-hospital-management-information-software-startlazaa.png)

# Contents

* [Introduction](#introduction)
* [Dataset Description](#DatasetDescription)
* [Tech Stack](#tectstack)
* [Prerequisites](#prerequisites)
* [How to Run this App Locally](#HowtoRunthisAppLocally)
* [Streamlit](#streamlit)
* [Contributors](#contributors)

<a name='introduction'></a>
## Introduction 

The Hospital Management System (HMS) is designed to streamline the operations of healthcare facilities. Leveraging MySQL Engine from AWS RDS and MongoDB, this dual-database system efficiently handles structured patient data and unstructured medical records. It features a user-friendly interface developed with Streamlit for the needs of patients, doctors, and administrators.


<a name='DatasetDescription'></a>
## Dataset Description
Given the sensitive nature of real-world hospital data
and the strict confidentiality protocols it necessitates,
our project employs synthetic data to simulate the
functionalities of the Hospital Management System. This
approach allows for a comprehensive demonstration of the
system's capabilities.

[Click Here for the Dataset](https://github.com/Komalsai234/Hospital-Management-System/tree/436e1662abdbe00717a51cc540da0d4692bf1e55/Dataset)



<a name='tectstack'></a>
## Tech Stack
- **Databases:** MySQL, MongoDB
- **User Interface:** Streamlit 
- AWS Relational Database Service (RDS)
- AWS EC2
- Apache Spark


<a name='prerequisites'></a>
## Prerequisites
- Anaconda 
- Python
- Apache Spark
- Scala
- AWS Account
- Streamlit Account

<a name='HowtoRunthisAppLocally'></a>
## How to Run this App Locally

### Clone this Repository

```bash
git clone https://github.com/Komalsai234/Hospital-Management-System.git
```

### Setting up Conda Environment
- **Create a new Conda environment**
```bash
conda create --name hms python=3.9
```

- **Activate the environment**
```bash
conda activate hms
```

- **Navigate to the project directory**
```bash
cd path/to/hospital-management-system
```


### Install required Packages
- **Install the required packages**
```bash
pip install -r requirements.txt
```

### Streamlit App Usage
- **Navigate to the Streamlit directory within the src folder**
```bash
cd src/Streamlit/
```

- **Run the Streamlit app**
```bash
streamlit run app.py
```

## ❗ Note
**The application requires a connection to the AWS RDS database to function
correctly. Without the database running and properly configured with the correct
credentials in your environment, data insertion and retrieval operations will not be
possible.**

### Credentials to use Admin and Doctor Module

**ADMIN** 

- **Username:** admin, **Password:** admin@123

**Doctor** 

- **DoctorID:** 1, **Username:** doctor1, **Password:** doctor@1

<a name='streamlit'></a>
## Streamlit
**This app can be accessed from below link bu only when the AWS RDS Database is running.**

https://hospital-management-system.streamlit.app/


[Click Here for the Dataset](https://github.com/Komalsai234/Hospital-Management-System/tree/436e1662abdbe00717a51cc540da0d4692bf1e55/Dataset)
## Instructor

### Dr. Sanajanasri J P, Assistant Professor, Amrita School of AI

<a name='contributors'></a>
## Contributors

- [P.S.S.Sai Keerthana](https://github.com/saikeerthana234)
- [P. Komal Sai Anurag](https://www.github.com/komalsai234)
- [Udayagiri Varun](https://github.com/VarunUdayagiri)
- [Sejal Singh](https://github.com/sejal923)

