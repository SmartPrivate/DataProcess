import logging
import xml.etree.ElementTree as ET
import DataModel
import DBConnector
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

model_list = []
count = 1
start_time = time.time()
for event, element in ET.iterparse('dblp_new.xml'):
    if count == 10000:
        DBConnector.db_list_writer(model_list)
        model_list.clear()
        count = 1
        end_time = time.time()
        print('完成10000条记录，累计耗时{0}秒'.format(str(end_time - start_time)))
    if event == 'end':
        if element.tag == 'article':
            model = DataModel.DBLP()
            try:
                model.title = element.find('title').text
            except AttributeError:
                model.title = None
            try:
                model.year = int(element.find('year').text)
            except AttributeError:
                model.year = None
            try:
                model.volume = element.find('volume').text
            except AttributeError:
                model.volume = None
            try:
                model.number = element.find('number').text
            except AttributeError:
                model.number = None
            try:
                model.journal = element.find('journal').text
            except AttributeError:
                model.journal = None
            try:
                model.pages = element.find('pages').text
            except AttributeError:
                model.pages = None
            ees, urls, authors = [], [], []
            try:
                for ee in element.findall('ee'):
                    ees.append(ee.text)
                    model.ee = ';'.join(ees)
            except AttributeError:
                model.ee = None
            try:
                for url in element.findall('url'):
                    urls.append(url.text)
                    model.url = ';'.join(urls)
            except AttributeError:
                model.url = None
            try:
                for author in element.findall('author'):
                    authors.append(author.text)
                    model.author = ';'.join(authors)
            except AttributeError:
                model.author = None
            model_list.append(model)
            count = count + 1
if len(model_list) > 0:
    DBConnector.db_list_writer(model_list)
print('操作已完成！')
