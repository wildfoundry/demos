from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn
from datetime import datetime
import os

app = FastAPI()

# Define a Pydantic model for the JSON input
class ReadingData(BaseModel):
    time: str
    reading: float

# Set up SQLAlchemy engine and Session
script_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_directory, "measurements.db")
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Measurement model
class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, index=True)
    reading = Column(Float)

# Create the table in the database
Base.metadata.create_all(engine)

# Define a route to accept POST requests
@app.post("/record/")
def record_reading(data: ReadingData):
    time = datetime.strptime(data.time, "%S:%M:%H %d-%m-%Y")
    reading = data.reading
    
    # Insert the data into the database using SQLAlchemy
    session = Session()
    try:
        measurement = Measurement(time=time, reading=reading)
        session.add(measurement)
        session.commit()
    finally:
        session.close()

    return {"message": "Data recorded successfully"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()