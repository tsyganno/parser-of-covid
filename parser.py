import requests
from bs4 import BeautifulSoup
import xlwt
from datetime import datetime


def generation_date(date):
    calendar = {
        'январ': '01',
        'февр': '02',
        'март': '03',
        'апрел': '04',
        'ма': '05',
        'июн': '06',
        'июл': '07',
        'авг': '08',
        'сент': '09',
        'окт': '10',
        'нояб': '11',
        'дек': '03',
    }
    for key in calendar.keys():
        if key in date.split()[1]:
            date_format_date = datetime.strptime(f"2022-{calendar[key]}-{date.split()[0]}", "%Y-%m-%d")
            return date_format_date


def parsing(count, path='registry.xls'):
    element = []
    dataset_minzdrav = []
    dataset_minzdrav_ready = []
    dataset_stop = []
    source_minzdrav = 'минздрав.рф'
    source_stop = 'стопкоронавирус.рф'
    link_minzdrav = f'https://covid19.rosminzdrav.ru/news/'
    inquiry_minzdrav = requests.get(link_minzdrav)
    soup_minzdrav = BeautifulSoup(inquiry_minzdrav.text, 'html.parser')
    soup_link_minzdrav = soup_minzdrav.find_all("a", {"class": "news_block"})
    for el in soup_link_minzdrav:
        date = str(el)[str(el).find('<time>') + 6: str(el).find('</time>')]
        date_format_date = generation_date(date)
        date_now = datetime.now()
        delta = str(date_now - date_format_date).split()
        if delta[0].isdigit() and 0 < int(delta[0]) <= 30 and int(delta[0]):
            dataset_minzdrav_ready.append(el)
        elif len(delta) == 1:
            dataset_minzdrav_ready.append(el)
    for el in dataset_minzdrav_ready:
        title = str(el)[str(el).find('title="') + 7: str(el).find('<div class="') - 2]
        element.append(title)
        date = str(el)[str(el).find('<time>') + 6: str(el).find('</time>')]
        element.append(str(generation_date(date)).split()[0])
        a = str(el)[str(el).find('href="') + 6: str(el).find('" title="')]
        element.append(a)
        dataset_minzdrav.append(tuple(element))
        element = []
    for i in range(count):
        link_stop = f'https://xn--80aesfpebagmfblc0a.xn--p1ai/news/?page={i}'
        inquiry_stop = requests.get(link_stop)
        soup_stop = BeautifulSoup(inquiry_stop.text, 'html.parser')
        soup_link_stop = soup_stop.find_all("a")
        for el in soup_link_stop:
            if el.find_all("p"):
                tag_h2 = str(el)[str(el).find('<h2>') + 4: str(el).find('</h2>')]
                element.append(tag_h2)
                tag_p = str(el)[str(el).find('<p>') + 3: str(el).find('</p>')]
                element.append(str(generation_date(tag_p)).split()[0])
                link = f'https://xn--80aesfpebagmfblc0a.xn--p1ai/news/{str(el)[str(el).find("href=") + 6: str(el).find("<p>") - 2]}'
                if link.count('https') == 2:
                    link = link[link.rfind('https'):]
                element.append(link)
                dataset_stop.append(tuple(element))
                element = []
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Данные')
    count = 0
    for i in range(len(dataset_minzdrav)):
        if i == 0:
            sheet.write(count, 0, 'Заголовок')
            sheet.write(count, 1, 'Дата размещения')
            sheet.write(count, 2, 'Ссылка на ресурс')
            sheet.write(count, 3, 'Источник')
            count += 1
        sheet.write(count, 0, dataset_minzdrav[i][0])
        sheet.write(count, 1, dataset_minzdrav[i][1])
        sheet.write(count, 2, dataset_minzdrav[i][2])
        sheet.write(count, 3, source_minzdrav)
        count += 1
    for i in range(len(dataset_stop)):
        sheet.write(count, 0, dataset_stop[i][0])
        sheet.write(count, 1, dataset_stop[i][1])
        sheet.write(count, 2, dataset_stop[i][2])
        sheet.write(count, 3, source_stop)
        count += 1
    wb.save(path)


count_webpages = 23
parsing(count_webpages)

