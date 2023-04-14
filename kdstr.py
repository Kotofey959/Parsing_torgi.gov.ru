from typing import Dict

import requests

from links import GetLink

cookies = {
    'utm_data': '%7B%7D',
    '_ym_uid': '1679847441976221864',
    '_ym_d': '1679847441',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ga': 'GA1.2.1736190133.1679847442',
    '_gid': 'GA1.2.460986836.1679847442',
    '_gat': '1',
}

headers = {
    'authority': 'ru.reestrgos.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'api-token': 'd41d8cd98f00b204e',
    'content-type': 'application/json',
    'origin': 'https://ru.reestrgos.com',
    'referer': 'https://ru.reestrgos.com/object/77-09-0003002-3548',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36',
}


def get_floor_area(kdstr) -> Dict or None:
    """
    :param kdstr: кадастровый номер
    :return: словарь с этажом, площадью и координатами объекта
    """
    json_data = {
        'number': str(kdstr),
    }
    response = requests.post(GetLink().cadastre_link, cookies=cookies, headers=headers,
                             json=json_data).json()
    if response:
        return {'floor': response.get('response').get('data').get('common').get('floor'),
                'area': response.get('response').get('data').get('common').get('area'),
                'coords': f"{response.get('response').get('data').get('fias').get('geo_lat')}:{response.get('response').get('data').get('fias').get('geo_lon')}"
                }
