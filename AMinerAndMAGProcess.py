import logging
import json
import DBConnector
import DataModel
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def assemble_main_model_reflex(json_line: dict):
    json_model = DataModel.MAG()
    if 'keywords' in json_line:
        json_model.keywords = ';'.join(json_line['keywords'])
        del json_line['keywords']
    if 'url' in json_line:
        json_model.url = ';'.join(json_line['url'])
        del json_line['url']
    if 'fos' in json_line:
        json_model.fos = ';'.join(json_line['fos'])
        del json_line['fos']

    for key, value in json_line.items():
        setattr(json_model, key, value)
    return json_model


def assemble_author_model_list(json_line):
    json_model_list = []
    for name_dict in json_line['authors']:
        json_model = DataModel.MAGAuthor()
        json_model.id = json_line['id']
        json_model.year = json_line['year']
        if name_dict['name'] is None or name_dict['name'] == '':
            continue
        json_model.name = name_dict['name']
        if 'org' not in name_dict:
            continue
        json_model.org = name_dict['org']
        json_model_list.append(json_model)
    return json_model_list


def assemble_reference_model_list(json_line):
    json_model_list = []
    for ref in json_line['references']:
        json_model = DataModel.MAGReference()
        json_model.id = json_line['id']
        json_model.year = json_line['year']
        json_model.reference = ref
        json_model_list.append(json_model)
    return json_model_list


def load_data_to_db(file_dir_index):
    file_dir = 'D:\\DataSets\\MAGPapers\\mag_papers_{0}.txt'.format(str(file_dir_index))
    file = open(file_dir, 'r')
    model_list, author_model_lists, reference_model_lists = [], [], []
    row_count = 0
    while True:
        line = file.readline()
        if not line:
            break
        parsed_line = json.loads(line)
        start_time = time.time()
        if 'authors' in parsed_line:
            author_model_list = assemble_author_model_list(parsed_line)
            del parsed_line['authors']
            for item in author_model_list:
                author_model_lists.append(item)
            if len(author_model_lists) > 10000:
                DBConnector.db_list_writer(author_model_lists)
                author_model_lists.clear()

        if 'references' in parsed_line:
            reference_model_list = assemble_reference_model_list(parsed_line)
            del parsed_line['references']
            for item in reference_model_list:
                reference_model_lists.append(item)
            if len(reference_model_lists) > 10000:
                DBConnector.db_list_writer(reference_model_lists)
                reference_model_lists.clear()

        model = assemble_main_model_reflex(parsed_line)
        model_list.append(model)
        if len(model_list) == 10000:
            DBConnector.db_list_writer(model_list)
            model_list.clear()
            end_time = time.time()
            row_count = row_count + 10000
            print('完成{0}条记录，耗时{1}秒'.format(str(row_count), str(end_time - start_time)))


for i in range(1, 50):
    load_data_to_db(i)
    print("完成文件{0}读取入库！".format(str(i)))
