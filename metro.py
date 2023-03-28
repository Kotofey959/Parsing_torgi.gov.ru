import json

from geopy.distance import geodesic


def get_metro(coords):
    if 'None' not in coords:
        coords = tuple(map(float, coords.split(':')))
        with open('metro.json', 'r', encoding='Windows-1251') as file:
            dist = {}
            metro = json.load(file)
            for m in metro.keys():
                metro_coords = tuple(map(float, m.split(':')))
                dist[geodesic(metro_coords, coords).meters] = m

            return metro.get(dist.get(min(dist.keys())))


def get_key_words(obj_json):
    words = ['обременение', 'залог', 'кредит', 'ипотека', 'домовая книга', 'выписка из домовой книги',
             'архивная выписка']
    obj_str = str(obj_json).lower()
    res = []
    for w in words:
        if w in obj_str:
            res.append(w)
    return res
