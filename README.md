# Patient Management System API

A simple and lightweight RESTful API built with **FastAPI** for managing patient records. It allows you to perform basic CRUD (Create, Read, Update, Delete) operations, compute BMI (Body Mass Index), and sort patient records dynamically.

## 🚀 Features

- **Store & Manage Patients:** Add, view, update, and delete patient records.
- **Automatic BMI Calculation:** Automatically calculates the patient's BMI and provides a health verdict (Underweight, Normal weight, Overweight, Obese) based on height and weight.
- **Sorting Capability:** Sort patient records by height, weight, or BMI in ascending or descending order.
- **Data Persistence:** Uses a lightweight JSON file (`patients.json`) to persist data locally.
- **Data Validation:** Uses Pydantic models to strictly enforce data types, constraints, and provide detailed API documentation.

## 🛠️ Tech Stack

- **Python 3**
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: An ASGI web server implementation for Python.

## 📋 Prerequisites

Make sure you have Python installed (preferably version 3.8 or higher).

## 💻 Installation & Setup

1. **Clone the repository** (or navigate to your project directory):
   ```bash
   cd Patient_Management_System
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   Review the `requirements.txt` file and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   *If `uvicorn` is not in your requirements.txt, install it using `pip install uvicorn`.*

## ▶️ Running the Application

To start the FastAPI server, run the following command in your terminal:

```bash
uvicorn main:app --reload
```

- The API will be available at: http://127.0.0.1:8000
- **Interactive API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs
- **Alternative API Documentation (ReDoc)**: http://127.0.0.1:8000/redoc

## 📡 API Endpoints

### General
| HTTP Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a greeting message. |
| `GET` | `/about` | Returns a short description about the API. |

### Patient Operations
| HTTP Method | Endpoint | Description |
|---|---|---|
| `GET` | `/view` | Retrieves all patient records. |
| `GET` | `/patient/{patient_id}` | Retrieves a specific patient by their ID. |
| `GET` | `/sort` | Retrieves patients sorted. Query params: `sort_by` (`height`, `weight`, `bmi`), `order` (`asc`, `desc`). |
| `POST` | `/create` | Creates a new patient. The payload requires a full `Patient` object. |
| `PUT` | `/update/{patient_id}` | Updates existing patient details. Recalculates BMI automatically. |
| `DELETE`| `/delete/{patient_id}`| Deletes a patient by their ID. |

## 📦 Data Models

### Patient Request Output (Computed)
When you fetch a patient, the response contains basic information along with automatically calculated fields:
```json
{
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.5,
  "bmi": 23.02,
  "verdict": "Normal weight"
}
```

*Note:* Pydantic models ensure that fields like age, height, and weight are strictly greater than zero, and `gender` is restricted to `male`, `female`, or `others`.

## 📁 Project Structure

```text
Patient_Management_System/
│
├── main.py               # Entry point of the FastAPI application
├── patients.json         # Local data storage file (auto-updated)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```
