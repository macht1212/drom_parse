import os
import datetime as dt
import time
import csv
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from model import Car


class Parser:

    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename

    def parse(self):

        Logger(f'logs_{self.filename}.log').create_log()

        CreateCSV(name=self.filename).create_csv()

        for j in tqdm(range(1, 101)):
            time.sleep(2)

            url = self.url + f'all/page{j}'
            result = requests.get(url=url).text

            soup = BeautifulSoup(result, features='lxml')
            raw_data = soup.find_all('a', {'data-ftid': "bulls-list_bull"})

            for i in range(20):
                try:
                    name_year = raw_data[i].find('span', {'data-ftid': "bull_title"}).getText()
                    name, year = name_year.strip().split(',')
                    info = raw_data[i].find('div', {'data-ftid': "component_inline-bull-description"}).getText()
                    engine_capacity_horse_power, fuel, transmission, drive_unit, mileage = info.strip().split(',')
                    mileage = ''.join(mileage.strip().split(' ')[:-1])
                    price = raw_data[i].find('span', {'data-ftid': "bull_price"}).getText()
                    price = ''.join(re.findall(pattern=r'\d+', string=price))

                    engine_capacity, horse_power = re.findall(pattern=r'\d.\d', string=engine_capacity_horse_power)

                    data = Car(
                        name=name,
                        year=int(year),
                        engine_capacity=float(engine_capacity),
                        horse_power=int(horse_power),
                        fuel=fuel,
                        transmission=transmission,
                        drive_unit=drive_unit,
                        mileage=int(mileage),
                        price=int(price)
                    )

                    WriteCSV(self.filename).write_csv(data)
                except Exception as e:
                    Logger(f'logs_{self.filename}.log').add_error(j, i, str(e))


class CreateCSV:
    """
    Класс CreateCSV предназначен для создания файла CSV и записи первой строки с загаловками параметров.
    В классе реализован один метод create_csv, в котором реализована вся логика создания файла.
    Класс при создании экземпляра принимает один аргумент:
        name: строковый тип данных, название файла для записи
    """

    def __init__(self, name: str):
        self.name = name

    def create_csv(self):
        """
        Метод create_csv является частью класса CreateCSV и отвечает за создание файла CSV и запись строки заголовка с
        именами параметров.
        
        Процесс:
        1. Метод открывает файл с заданным именем и добавленной к нему текущей датой.
        2. Создается объект csv.writer для записи в файл, используя запятую в качестве разделителя.
        3. Записывается в файл строку заголовка, содержащую имена параметров.
        :return: None
        """
        with open(os.path.join(self.name + f'_{dt.datetime.now().strftime("%Y_%m_%d")}' + '.csv'), 'w') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow([
                'name',
                'year',
                'engine_capacity',
                'horse_power',
                'transmission',
                'drive_unit',
                'fuel',
                'mileage',
                'price'
            ])


class WriteCSV:
    """
    Класс WriteCSV предназначен для записи данных в файл CSV.
    В классе реализован один метод write_csv, в котором реализована вся логика записи в файл.
    Класс при создании экземпляра принимает один аргумент:
        name: строковый тип данных, название файла для записи
    """

    def __init__(self, name: str):
        self.name = name

    def write_csv(self, data: Car):
        """
        Метод write_csv отвечает за запись данных в файл CSV. Он принимает на вход экземпляр класса Car и записывает
        атрибуты автомобиля в файл.
        
        Процесс:
        1. Открывается файл CSV с указанным именем файла и добавленной к нему текущей датой.
        2. Создается объект записи CSV с файлом и запятой в качестве разделителя.
        3. Записывается в CSV-файл строку с атрибутами автомобиля, используя метод writerow объекта записи CSV.
        :return: None
        """
        with open(os.path.join(self.name + f'_{dt.datetime.now().strftime("%Y_%m_%d")}' + '.csv'), 'a') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow([
                data.name,
                data.year,
                data.engine_capacity,
                data.horse_power,
                data.transmission,
                data.drive_unit,
                data.fuel,
                data.mileage,
                data.price
            ])


class Logger:
    """
    Класс Logger предназначен для создания и наполнения файла логов ошибок.
    В классе реализованы два метода:
        create_file, в котором реализована вся логика создания файла
        add_error, в котором реализована вся логика внесения информации об ошибки в файл
    Класс при создании экземпляра принимает один аргумент:
        filename: строковый тип данных, название файла для записи
    """

    def __init__(self, filename: str):
        self.filename = filename

    def create_log(self):
        """
        Метод create_file отвечает за создание файла логов ошибок
        
        Процес:
        1. Создается файл для записи
        2. Записывается строка состоящая из временной метки когда был создан файл
        3. Закрывается файл
        :return: None
        """
        with open(os.path.join(self.filename + '.log'), 'w') as file:
            file.write(f'{dt.datetime.now()} \n')
            file.write('page_line\ttimestamp\terror\n')

    def add_error(self, page: int, line: int, error: str):
        """
        Метод add_error отвечает за внесение данных об ошибках в лог файл
        
        Процесс:
        1. Открывается файл для дополнения
        2. Записывается форматированная строка, содердащая номер страницы, номер линии, текущее время в формате
            временной метки и сообщение об ошибке
        3. Закрывается файл
        
        :param page: Номер страницы с которой производится парсинг, целое число
        :param line: Номер линии (объекта) который парсится, целое число
        :param error: Сообщение об ошибке, строка
        :return: None      
        """
        with open(os.path.join(self.filename), 'a') as file:
            file.write(f'{page}.{line}\t{dt.datetime.timestamp(dt.datetime.now())}\t{error} \n')
