from datetime import date
from pydantic import BaseModel, validator
from src.backend.factory.EssayPlannerFactory import EssayPlannerFactory
from src.backend.factory.KBCompressorFactory import KBCompressorFactory
from fastapi import Depends, FastAPI
import uvicorn

app = FastAPI()

class DateRange(BaseModel):
    task_description: str
    start_date: str
    end_date: str

    @validator('end_date')
    def check_dates(cls, v, values, **kwargs):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

@app.get("/run/essay")
def run_essay(date_range: DateRange = Depends()):
    essayplanner = EssayPlannerFactory().produce()
    return essayplanner.run_chain(date_range.task_description, date_range.start_date, date_range.end_date)

@app.post("/run/kb_compressor")
def run_chain():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)