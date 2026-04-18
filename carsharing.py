import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

from schemas import load_db, CarInput, save_db, CarOutput, TripInput, TripOutput

app = FastAPI()

db = load_db()
@app.get("/")
async def welcome(name):
    return {'message': f"Hello {name}! "}

@app.get("/api/cars")
def get_cars(size:str|None=None, doors:int|None=None)->list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result

@app.post("/api/cars/{id}")
def get_car(id:int):
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

@app.post("/api/cars")
def add_car(car:CarInput)->CarOutput :
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car

@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.put("/api/cars/{id}")
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")



@app.post("/api/cars/{car_id}/trips")
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1,
                              start=trip.start, end=trip.end,
                              description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)