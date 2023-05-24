etp__link = 'https://178fz.roseltorg.ru/index.php'
cadastral_link = 'https://ru.reestrgos.com/api/objects/get'
renovation_link = 'https://www.mos.ru/altmosmvc/api/renovation/v2/bounded_addresses'


def get_doc_link(doc_id: int) -> str:
    return f'https://torgi.gov.ru/new/file-store/v1/{doc_id}'


def get_sample_link(page: int, size: int) -> str:
    return f"https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=78&biddType=178FZ&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION&catCode=9&byFirstVersion=true&withFacets=false&page={page}&size={size}&sort=firstVersionPublicationDate,desc"


def get_lot_link(lot_id: str) -> str:
    return f"https://torgi.gov.ru/new/api/public/lotcards/{lot_id}"


def get_etp_link(obj_id: str) -> str:
    return f'https://torgi.gov.ru/new/api/public/notices/noticeNumber/{obj_id}'


def get_izv_link(obj_id: str) -> str:
    return f'https://torgi.gov.ru/new/public/notices/view/{obj_id.split("_")[0]}'



