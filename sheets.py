import pygsheets

client = pygsheets.authorize(
    service_account_file='E:\PyCharm Community Edition 2022.3\Parsing_torgi.gov.ru\parsing-torg-8e4dbd63d412.json')


def list_to_str(lst):
    text = ''
    for i in lst:
        text += f'{str(i)}\n'
    return text


def info_to_worksheet(objects, date1, date2):
    sh = client.open('Parsing')
    work_sh = sh.worksheet_by_title(f'{date1} - {date2}')
    count = 1
    for obj in objects:
        if obj:
            count += 1
            work_sh.update_values(f'A{count}', [[
                '-',
                f'{count - 1}',
                f'{obj.get("id")}',
                f'{obj.get("metro")}',
                f'{obj.get("title")}',
                f'{obj.get("address")}',
                f'{str(obj.get("area")).replace(".", ",")}',
                f'{obj.get("floor")}',
                f'{obj.get("rooms")}',
                f'{obj.get("floors")}',
                f'=M{count}/G{count}',
                f'{obj.get("kdstr")}',
                f'{str(obj.get("start_price")).replace(".", ",")}',
                '-',
                '-',
                f'=M{count}*1,2',
                f'{str(obj.get("deposit")).replace(".", ",")}',
                f'{str(obj.get("price_step")).replace(".", ",")}',
                '0',
                f'=S{count}*0,13',
                '0',
                f'=S{count}-T{count}-U{count}-M{count}',
                '-',
                f'{list_to_str(obj.get("documents"))}',
                f'{list_to_str(obj.get("keywords"))}',
                f'{obj.get("biddStartTime")}',
                f'{obj.get("biddEndTime")}',
                f'{obj.get("auctionStartDate")}',
                f'{obj.get("last_time")}',
                f'{obj.get("izv_link")}',
                'АКЦИОНЕРНОЕ ОБЩЕСТВО «ЕДИНАЯ ЭЛЕКТРОННАЯ ТОРГОВАЯ ПЛОЩАДКА»'


            ]])



