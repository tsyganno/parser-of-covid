import requests
from bs4 import BeautifulSoup
import xlwt


def parsing(count, path='registry.xls'):
    element = []
    dataset = []
    for i in range(count):
        link = f'https://xn--80aesfpebagmfblc0a.xn--p1ai/news/?page={i}'
        inquiry = requests.get(link)
        soup = BeautifulSoup(inquiry.text, 'html.parser')
        soup_link_list = soup.find_all("a")
        for el in soup_link_list:
            if el.find_all("p"):
                tag_h2 = str(el)[str(el).find('<h2>') + 4: str(el).find('</h2>')]
                element.append(tag_h2)
                tag_p = str(el)[str(el).find('<p>') + 3: str(el).find('</p>')]
                element.append(tag_p)
                link = f'https://xn--80aesfpebagmfblc0a.xn--p1ai/news/{str(el)[str(el).find("href=") + 6: str(el).find("<p>") - 2]}'
                element.append(link)
                dataset.append(tuple(element))
                element = []
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Данные')
    count = 0
    for i in range(len(dataset)):
        if i == 0:
            sheet.write(count, 0, 'Заголовок')
            sheet.write(count, 1, 'Дата размещения')
            sheet.write(count, 2, 'Ссылка на ресурс')
            count += 1
        sheet.write(count, 0, dataset[i][0])
        sheet.write(count, 1, dataset[i][1])
        sheet.write(count, 2, dataset[i][2])
        count += 1
    wb.save(path)


count_webpages = 23
parsing(count_webpages)
