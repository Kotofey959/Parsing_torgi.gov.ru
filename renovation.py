import re

import requests
from links import renovation_link
import matplotlib.path as mpltPath

headers = {
    'authority': 'www.mos.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'referer': 'https://www.mos.ru/city/projects/renovation/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.594 Yowser/2.5 Safari/537.36',
    'x-caller-id': 'renovation-app',
}


def get_renovation_coords():
    """
    Получение списка полигонов координат объектов, попадающих под программу реновации

    """
    response = requests.get(renovation_link, headers=headers).json()
    coords = []
    for i in response:
        if i.get("type") == "address":
            coords.append(i.get("data").get("polygon").get("coordinates")[0])
    return coords


list_coords = get_renovation_coords()


def check_coords(obj_coords):
    """
    Проверяем попадает ли объект под программу реновации

    """
    template = r'([\d]+\.[\d]{4,}:[\d]+\.[\d]{4,})'
    if not re.match(template, obj_coords):
        return
    obj_lat, obj_lon = obj_coords.split(":")
    for coords in list_coords:
        path = mpltPath.Path(coords)
        if path.contains_point((float(obj_lat), float(obj_lon))):
            return "Да"
    return "Нет"
