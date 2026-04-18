import json

from pydantic import BaseModel

class Car(BaseModel):
    id: int
    size: str
    fuel:str | None ='electrics'
    doors:int
    transmission:str | None = 'auto'


# class CarOutput(CarInput):
#     id: int
#     trips: list[TripOutput] = [] # noqa (turns off an incorrect pycharm warning)

def load_db() -> list[Car]:
    """Load a list of Car objects from a JSON file"""
    with open("cars.json") as f:
        return [Car.model_validate (obj) for obj in json.load(f)]