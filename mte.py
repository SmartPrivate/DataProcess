import logging
import bibtexparser
import os
import DataModel, DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_nedd_main():
    files = os.listdir('NEDD')
    for file in files:
        bib_file = open('NEDD/{0}'.format(file), encoding='utf-8')
        bib_db = bibtexparser.load(bib_file)
        model_list = []
        for item in bib_db.entries:
            attr_dict = {}
            for key in item.keys():
                value = item[key].replace('{', '').replace('}', '').replace('\n', ' ')
                if '-' in key:
                    key = key.replace('-', '_')
                    attr_dict[key] = value
                if key == 'funding-acknowledgement':
                    attr_dict[key.replace('-', '_')] = item[key]
                if key == 'cited-references':
                    attr_dict[key.replace('-', '_')] = '!'.join(item[key].replace('{', '').replace('}', '').split('\n'))
                if key == 'author':
                    attr_dict[key] = '!'.join(item[key].split(' and '))
                if key == 'type':
                    attr_dict['type_'] = item[key].replace('{', '').replace('}', '').replace('\n', ' ')
                if key == 'ID':
                    attr_dict['id_'] = item[key].replace('{', '').replace('}', '').replace('\n', ' ')
                if key == 'ENTRYTYPE':
                    attr_dict['entrytype'] = item[key].replace('{', '').replace('}', '').replace('\n', ' ')
                else:
                    attr_dict[key] = value
            model = DataModel.NEDDContent()
            for key, value in attr_dict.items():
                setattr(model, key, value)
            model_list.append(model)
        DBConnector.db_list_writer(model_list)
        print('Finish {0}'.format(file))


def get_nedd_author():
    models = DBConnector.query_all(DataModel.NEDDContent)
    for model in models:
        model: DataModel.NEDDContent
        author_models = []
        for author in model.author.split(' and'):
            author_model = DataModel.NEDDAuthorContent()
            try:
                if author[0] == ' ':
                    author = author[1:]
                if author[-1] == ' ':
                    author = author[:-1]
            except IndexError:
                continue
            author_model.author = author
            author_model.unique_id = model.unique_id
            author_model.nedd_sid = model.sid
            author_models.append(author_model)
        DBConnector.db_list_writer(author_models)
        print('Finish sid = {0}'.format(model.sid))


get_nedd_main()
# get_nedd_author()
