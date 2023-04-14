import json

from geopy.distance import geodesic


def get_metro(coords: str) -> str or None:
    """
    :param coords: координаты объекта или 'None:None'
    :return str: название ближайшего метро
    """
    if 'None' not in coords:
        coords = tuple(map(float, coords.split(':')))
        with open('metro.json', 'r', encoding='Windows-1251') as file:
            dist = {}
            metro = json.load(file)
            for m in metro.keys():
                metro_coords = tuple(map(float, m.split(':')))
                dist[geodesic(metro_coords, coords).meters] = m

            return metro.get(dist.get(min(dist.keys())))

