import requests

cookies = {
    'etpsid': 'fce412fbe84e093ac5f99b2fcdbd743f',
    '20b6b357ea192383cb1244412247c5ea': 'dba5b9803f2dd18011e91516ba66fb6a',
}

headers = {
    'authority': '178fz.roseltorg.ru',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'etpsid=fce412fbe84e093ac5f99b2fcdbd743f; 20b6b357ea192383cb1244412247c5ea=dba5b9803f2dd18011e91516ba66fb6a',
    'origin': 'https://178fz.roseltorg.ru',
    'referer': 'https://178fz.roseltorg.ru/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'rpctype': 'direct',
    'module': 'default',
    'action': 'Procedure.load',
}


def get_last_date(etp_link):
    etp_id = etp_link.split('/')[-1]
    json_data = {
        'action': 'Procedure',
        'method': 'load',
        'data': [
            {
                'procedure_id': etp_id,
                'is_view': 1,
            },
        ],
        'type': 'rpc',
        'tid': 3,
        'token': '1aakEnWBd7QaUPmIvz9XAg',
    }
    response = requests.post('https://178fz.roseltorg.ru/index.php', params=params, cookies=cookies, headers=headers,
                             json=json_data).json()
    return response.get('result').get('procedure').get('date_end_first_parts_review').split('T')[0]

