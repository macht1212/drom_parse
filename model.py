import datetime as dt

from pydantic import BaseModel



class Car(BaseModel):
    """
    Модель Car наследующаяся от класса BaseModel библиотеки pydantic представляет собой модель для записи информации в
    файл csv.
    
    Параметры, которые передаются в модель:
        name: Название марки автомобиля
        year: Год выпуска автомобиля
        engine_capacity: Объем двигателя автомобиля
        horse_power: Мощность двигателя автомобиля
        transmission: Коробка передач
        drive_unit: Привод
        fuel: Тип топлива
        mileage: Пробег автомобиля
        price: Цена автомобиля
    """
    name: str
    year: int
    engine_capacity: float
    horse_power: int
    transmission: str
    drive_unit: str
    fuel: str
    mileage: int
    price: int
    
