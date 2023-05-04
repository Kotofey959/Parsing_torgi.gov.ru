import requests


def get_last_date(obj_id: str) -> str:
    """
    :param obj_id: id объекта
    :return str: дата рассмотрения заявок
    """
    cookies = {
        '_ym_uid': '1679826671768036242',
        '_ym_d': '1679826671',
        '_ym_isad': '2',
        'SESSION': 'ZjdmYzllZDEtYmE0Ni00NzU4LTkwZDMtOGYzZGI5MDA5MjNj',
        '_ym_visorc': 'w',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36',
        'branchId': 'null',
        'organizationId': 'null',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'traceparent': '00-75d3cbe9cc829af7b502c3e905fedef5-a20f477a0f3e9d1d-01',
    }

    response = requests.get(
        f'https://torgi.gov.ru/new/api/public/notices/noticeNumber/{obj_id}',
        cookies=cookies,
        headers=headers,
    ).json()
    return response.get('biddReviewDate').split('T')[0]