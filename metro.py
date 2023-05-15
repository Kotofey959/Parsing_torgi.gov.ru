import json
import re

from geopy.distance import geodesic

file = open('metro.json', 'r', encoding='Windows-1251')
metro = json.load(file)


def get_metro(coordinates: str) -> str or None:
    """
    :param coordinates: координаты объекта или 'None:None'
    :return str: название ближайшего метро
    """
    template = r'([\d]+\.[\d]{4,}:[\d]+\.[\d]{4,})'
    if re.match(template, coordinates):
        coordinates = tuple(map(float, coordinates.split(':')))
        dist = {}
        for m in metro.keys():
            metro_coordinates = tuple(map(float, m.split(':')))
            dist[geodesic(metro_coordinates, coordinates).meters] = m

        return metro.get(dist.get(min(dist.keys())))

