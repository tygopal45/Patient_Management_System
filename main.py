from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="The name of the patient", examples=["NRI Chai Wala", "Pradhanmantri MBA Wala"])]
    city: Annotated[str, Field(..., description="The city where the patient resides", examples=["Delhi", "Mumbai"])]
    age: Annotated[int, Field(..., gt=0, description="The age of the patient", examples=[25, 40])]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters", examples=[1.75, 1.80])]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms", examples=[70.5, 80.0])]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    # verdict on the basis of BMI value.
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(None, description="The name of the patient")]
    city : Annotated[Optional[str], Field(None, description="The city where the patient resides")]
    age : Annotated[Optional[int], Field(None, gt=0, description="The age of the patient")]
    gender : Annotated[Optional[Literal["male", "female", "others"]], Field(None, description="The gender of the patient")]
    height : Annotated[Optional[float], Field(None, gt=0, description="The height of the patient in meters")]
    weight : Annotated[Optional[float], Field(None, gt=0, description="The weight of the patient in kilograms")]

BASE_DIR = os.path.dirname(__file__)

app = FastAPI()

def load_data():
    with open(os.path.join(BASE_DIR, "patients.json"), "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open(os.path.join(BASE_DIR, "patients.json"), "w") as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {"message": "This is a simple Patient Management System API."}


@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to be retrieved", examples=["P001"])):
    # Load the patient data from the JSON file
    data = load_data()
    
    # Find the patient with the specified ID
    if patient_id in data:
        return data[patient_id]
    # return {"error": "Patient not found"}
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="The field to sort the patients by ['height', 'weight', 'bmi']"), order: str = Query("asc", description="Sort in ascending or descending order")):
    
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Select from valid fields {valid_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Select 'asc' or 'desc'")
    
    data = load_data()
    sort_order = (order == "desc")

    # x[column_name] =  The sorted function will use this value to sort the patient records based on the specified column.
    sorted_data = sorted(data.values(), key = lambda x: x[sort_by], reverse = sort_order)

    return sorted_data


@app.post('/create')
# the patient object is of Patient data type and it will be automatically validated by FastAPI using the Pydantic model.
# bmi and verdict will be automatically calculated and included in the response when a new patient is created.
def crate_patient(patient: Patient):
    # Load the existing patient data from the JSON file 
    data = load_data()

    # check if the patient ID already exists.
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    # Add the new patient to the data dictionary
    value_for_new_patient = patient.model_dump(exclude={'id'})
    data[patient.id] = value_for_new_patient

    # Save the updated patient data back to the JSON file
    save_data(data) 

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update the patient data with the new values
    existing_patient_data = data[patient_id]

    # the patient_update_data will contain only the fields that were provided in the request body, excluding any fields that were not set (i.e., those that are None).
    patient_update_data = patient_update.model_dump(exclude_unset=True)

    # Update the existing patient data with the new values
    for key, value in patient_update_data.items():
        existing_patient_data[key] = value
    
    # Save the updated patient data back to the JSON file

    # but the bmi and verdict also change when the height or weight is updated, so we need to recalculate the bmi and verdict if either height or weight is updated.

    # existing patient -> pydantic model -> update the height and weight -> recalculates the bmi and verdict -> convert back to dict -> save to json 
    # to avoid error while creating the pydantic object (keep it short) we insert patient id
    existing_patient_data["id"] = patient_id
    Patient_Pydantic_object = Patient(**existing_patient_data)

    # model to dictinary
    existing_patient_data = Patient_Pydantic_object.model_dump(exclude={'id'})

    # adding this dict to data
    data[patient_id] = existing_patient_data

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Remove the patient from the data dictionary
    del data[patient_id]

    # Save the updated patient data back to the JSON file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})