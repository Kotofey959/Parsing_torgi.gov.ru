import requests
from PyPDF2 import PdfReader

from links import doc_link


def get_rooms_floors(doc_id: int):
    """
    :param doc_id: id документа
    :return: словарь с этажом и количеством комнат объекта
    """
    response = requests.get(doc_link(doc_id))

    with open('123.pdf', 'wb') as f:
        f.write(response.content)
    with open('123.pdf', 'rb') as f:
        rooms_floors = {}
        pdf = PdfReader(f)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            rooms = text.find('Количество комнат')
            floors = text.find('этажном')
            if rooms:
                rooms_floors['rooms'] = text[rooms:rooms + 22]
            if floors:
                buf = ''
                for k in text[floors - 20:floors]:
                    if k in '123456789':
                        buf += k
                rooms_floors['floors'] = buf
            if rooms_floors.get('rooms') and rooms_floors.get('floors'):
                return rooms_floors

