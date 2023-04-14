from typing import List, Dict

import pygsheets

client = pygsheets.authorize(
    service_account_file='E:\PyCharm Community Edition 2022.3\Parsing_torgi.gov.ru\parsing-torg-8e4dbd63d412.json')


def list_to_str(lst: List[str]) -> str:
    """
    Преобразуем список элементов в строку
    """
    text = ''
    for i in lst:
        text += f'{str(i)}\n'
    return text


def info_to_worksheet(objects: List[Dict], date1: str, date2: str) -> None:
    """
    :param objects: список словарей с информацией об объекте
    :param date1: дата начала периода
    :param date2: дата конца периода
    :return:
    """
    sh = client.open('Parsing')
    work_sh = sh.worksheet_by_title(f'{date1} - {date2}')
    count = 1
    for obj in objects:
        if obj:
            count += 1
            work_sh.update_values(f'A{count}', [[
                '-',
                count - 1,
                obj.get("id"),
                obj.get("metro"),
                obj.get("title"),
                obj.get("address"),
                str(obj.get("area")).replace(".", ","),
                obj.get("floor"),
                obj.get("rooms"),
                obj.get("floors"),
                f'=M{count}/G{count}',
                obj.get("kdstr"),
                str(obj.get("start_price")).replace(".", ","),
                '-',
                '-',
                f'=M{count}*1,2',
                str(obj.get("deposit")).replace(".", ","),
                str(obj.get("price_step")).replace(".", ","),
                '0',
                f'=S{count}*0,13',
                '0',
                f'=S{count}-T{count}-U{count}-M{count}',
                '-',
                list_to_str(obj.get("documents")),
                list_to_str(obj.get("keywords")),
                obj.get("biddStartTime"),
                obj.get("biddEndTime"),
                obj.get("auctionStartDate"),
                obj.get("last_date"),
                obj.get("izv_link"),
                'АКЦИОНЕРНОЕ ОБЩЕСТВО «ЕДИНАЯ ЭЛЕКТРОННАЯ ТОРГОВАЯ ПЛОЩАДКА»'
            ]])



