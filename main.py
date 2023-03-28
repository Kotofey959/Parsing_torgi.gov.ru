import requests
import datetime as dt

from etp import get_last_date
from pdf import get_rooms_floors
from sheets import info_to_worksheet
from metro import get_metro, get_key_words
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
    # 'Cookie': 'SESSION=MDlhZDlhOTctMmE3Mi00YTM1LWI3ZTYtYTAwMzViMGM0ZTJj; _ym_uid=1679826671768036242; _ym_d=1679826671; _ym_isad=2; _ym_visorc=w',
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


def get_api_url(page, size):
    url = f"https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=78&biddType=178FZ&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION&catCode=9&byFirstVersion=true&withFacets=false&page={page}&size={size}&sort=updateDate,desc"
    return url


def get_total_elements(url):
    response = requests.get(url, cookies=cookies, headers=headers).json()
    return response.get('totalElements')


def get_element_link(element_id):
    link = f'https://torgi.gov.ru/new/public/lots/lot/{element_id}/(lotInfo:info)?fromRec=false'
    return link


def get_json(url):
    response = requests.get(url, cookies=cookies, headers=headers).json()
    return response


def get_element_ids():
    total_elements = int(get_total_elements(get_api_url(1, 10)))
    total_pages = (total_elements // 10) + 1
    ids_list = []
    for i in range(1, total_pages + 1):
        url = get_api_url(i, 10) if i != total_pages else get_api_url(i, total_elements % 10)
        response = get_json(url)
        for k in response.get('content'):
            ids_list.append(k.get('id'))
    return ids_list


def parse_title_to_kwargs(title):
    kwargs = {
        'address': title[title.find('по адресу:'):title.find(' общей площадью')].split('по адресу:')[1].strip(','),
    }
    if title.find('кадастровый номер'):
        kwargs['kdstr'] = title[title.find('кадастровый номер'):].split('кадастровый номер')[-1].strip(":").strip(' ').strip(')').strip(').').split(';')[0]
    return kwargs


def get_document_id(document):
    for i in document.get('noticeAttachments'):
        if 'Лотовая документация' in i.get('fileName') or 'лотовая документация' in i.get('fileName'):
            return i.get('fileId')


def get_info(obj_id, date1, date2):
    resp = requests.get(f"https://torgi.gov.ru/new/api/public/lotcards/{obj_id}").json()
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
            print(obj.get('coords'))
            if obj.get('coords'):
                obj['metro'] = get_metro(obj.get('coords'))
        key_words = get_key_words(resp)
        obj['keywords'] = key_words
        if obj.get('doc_id'):
            rooms_floors = get_rooms_floors(obj.get('doc_id'))
            if rooms_floors:
                obj['rooms'] = rooms_floors.get('rooms')
                obj['floors'] = rooms_floors.get('floors')
        obj['last_time'] = get_last_date(resp.get('etpUrl'))
        return obj


def main(date1, date2):
    ids_list = get_element_ids()
    obj_list = [get_info(id, date1, date2) for id in ids_list]
    print(obj_list)
    info_to_worksheet(obj_list, date1, date2)


if __name__ == '__main__':
    '''
    Здесь указать даты по которым отбираем лоты
    '''
    main('20.02.2023', '26.02.2023')
