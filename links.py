class GetLink:
    @property
    def etp_link(self):
        return 'https://178fz.roseltorg.ru/index.php'

    @property
    def cadastre_link(self):
        return 'https://ru.reestrgos.com/api/objects/get'

    @staticmethod
    def doc_link(doc_id):
        return f'https://torgi.gov.ru/new/file-store/v1/{doc_id}'

    @staticmethod
    def sample_link(page, size):
        return f"https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=78&biddType=178FZ&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION&catCode=9&byFirstVersion=true&withFacets=false&page={page}&size={size}&sort=updateDate,desc"

    @staticmethod
    def lot_link(lot_id):
        return f"https://torgi.gov.ru/new/api/public/lotcards/{lot_id}"
