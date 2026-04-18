import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

from schemas import load_db

app = FastAPI()

db = load_db()
@app.get("/")
async def welcome(name):
    return {'message': f"Hello {name}! "}

@app.get("/api/cars")
def get_cars(size:str|None=None, doors:int|None=None)->list:
    result = db
    if size:
        result = [car for car in result if car['size'] == size]
    if doors:
        result = [car for car in result if car['doors'] >= doors]
    return result

@app.post("/api/cars/{id}")
def get_car(id:int)->dict:
    result = [car for car in db if car['id'] == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)