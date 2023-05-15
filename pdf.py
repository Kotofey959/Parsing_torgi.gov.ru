import requests
from PyPDF2 import PdfReader

from links import get_doc_link


def get_rooms_floors(doc_id: int):
    """
    :param doc_id: id документа
    :return: словарь с этажом и количеством комнат объекта
    """
    url = get_doc_link(doc_id)
    response = requests.get(url)

    with open('document.pdf', 'wb') as f:
        f.write(response.content)
    with open('document.pdf', 'rb') as f:
        rooms_floors = {}
        pdf = PdfReader(f)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            rooms_index = text.find('Количество комнат')
            floors_index = text.find('этажном')
            if rooms_index:
                rooms_floors['rooms'] = text[rooms_index:rooms_index + 22]
            if floors_index:
                buf = ''
                for symbol in text[floors_index - 20:floors_index]:
                    if symbol.isnumeric():
                        buf += symbol
                rooms_floors['floors'] = buf
            if rooms_floors.get('rooms') and rooms_floors.get('floors'):
                return rooms_floors

