import json
from typing import Dict, Any

import requests
import datetime as dt
import re

from etp import get_last_date
from links import sample_link, lot_link
from pdf import get_rooms_floors
from sheets import info_to_worksheet
from metro import get_metro
from kdstr import get_floor_area

cookies = {
    'SESSION': 'MDlhZDlhOTctMmE3Mi00YTM1LWI3ZTYtYTAwMzViMGM0ZTJj',
    '_ym_uid': '1679826671768036242',
    '_ym_d': '1679826671',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36',
    'branchId': 'null',
    'organizationId': 'null',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'traceparent': '00-62e95e8741fd54dd64859c48cbb23b74-4f77a890b6c3dae1-01',
}


def get_total_elements(url: str) -> int:
    """
    :param url: url API общей выборки лотов
    :return: количество элементов в выборке
    """
    response = requests.get(url, cookies=cookies, headers=headers).json()
    return response.get('totalElements')


def get_json(url: str) -> Dict[str, Any]:
    """
    :param url: API url выборки лотов
    :return: json с выборкой лотов
    """
    response = requests.get(url, cookies=cookies, headers=headers).json()
    return response


def get_element_ids():
    """
    :return: список id всех лотов из выборки
    """
    total_elements = int(get_total_elements(sample_link(1, 10)))
    total_pages = (total_elements // 10) + 1
    ids_list = []
    for i in range(1, total_pages + 1):
        url = sample_link(i, 10) if i != total_pages else sample_link(i, total_elements % 10)
        response = get_json(url)
        for k in response.get('content'):
            ids_list.append(k.get('id'))
    return ids_list


def parse_title_to_kwargs(title: str) -> Dict[str, Any]:
    """
    :param title: Название лота
    :return: Словарь с адресом и кадастровым номером
    """
    kwargs = {
        'address': title[title.find('по адресу:'):title.find(' общей площадью')].split('по адресу:')[1].strip(','),
        'kdstr': re.search(r'\d{2}:\d{2}:\d{7,9}:\d{2,6}', title).group()
    }
    return kwargs


def get_document_id(document: Dict[str, Any]) -> None or int:
    """
    :param document: словарь с информацией о документах к лоту
    :return: id нужного документа если он есть
    """
    for i in document.get('noticeAttachments'):
        if 'Лотовая документация' in i.get('fileName') or 'лотовая документация' in i.get('fileName'):
            return i.get('fileId')


def get_key_words(obj_json: json) -> list[str]:
    """
    :param obj_json: json cо всей информацией о лоте
    :return: список ключевых слов, если встречаются
    """
    words = ['обременение', 'залог', 'кредит', 'ипотека', 'домовая книга', 'выписка из домовой книги',
             'архивная выписка']
    obj_str = str(obj_json).lower()
    res = []
    for w in words:
        if w in obj_str:
            res.append(w)
    return res


def get_info(obj_id, date1, date2):
    """
    :param obj_id: id лота
    :param date1: дата начала периода
    :param date2: дата конца периода
    :return: словарь со всей инофрмацией об объекте
    """
    resp = requests.get(lot_link(obj_id)).json()
    obj = {
        'id': obj_id,
        'title': resp.get('lotName'),
        'start_price': resp.get('priceMin'),
        'price_step': resp.get('priceStep'),
        'deposit': resp.get('deposit'),
        'auctionStartDate': resp.get('auctionStartDate').split('T')[0],
        'biddStartTime': resp.get('biddStartTime').split('T')[0],
        'biddEndTime': resp.get('biddEndTime').split('T')[0],
        'documents': [i.get('fileName') for i in resp.get('noticeAttachments')],
        'izv_link': f'https://torgi.gov.ru/new/public/notices/view/{obj_id.split("_")[0]}',
        'doc_id': get_document_id(resp)
    }
    d_obj = dt.datetime.strptime(obj.get("biddStartTime"), '%Y-%m-%d')
    d1 = dt.datetime.strptime(date1, '%d.%m.%Y')
    d2 = dt.datetime.strptime(date2, '%d.%m.%Y')

    if d1 <= d_obj <= d2:
        addr_kdstr = parse_title_to_kwargs(obj.get('title'))

        obj['address'] = addr_kdstr.get('address')
        obj['kdstr'] = addr_kdstr.get('kdstr')
        if obj.get('kdstr'):
            floor_area = get_floor_area(obj.get('kdstr'))
            obj['floor'] = floor_area.get('floor')
            obj['area'] = floor_area.get('area')
            obj['coords'] = floor_area.get('coords')
            if obj.get('coords'):
                obj['metro'] = get_metro(obj.get('coords'))
        key_words = get_key_words(resp)
        obj['keywords'] = key_words
        if obj.get('doc_id'):
            rooms_floors = get_rooms_floors(obj.get('doc_id'))
            if rooms_floors:
                obj['rooms'] = rooms_floors.get('rooms')
                obj['floors'] = rooms_floors.get('floors')
        obj['last_date'] = get_last_date(obj_id.split("_")[0])
        return obj


def main(date1, date2):
    """
    1) Собираем все id выборки
    2) Формируем словари с инфо об нужных объектах
    3) Добавляем информацию в гугл таблицу

    :param date1: дата начала периода
    :param date2: дата конца периода

    """
    ids_list = get_element_ids()
    obj_list = [get_info(id, date1, date2) for id in ids_list]
    info_to_worksheet(obj_list, date1, date2)


if __name__ == '__main__':
    '''
    Здесь указать даты по которым отбираем лоты
                  \     /
                   \   / 
                    \ /       
    '''
    main('18.04.2023', '30.04.2023')
