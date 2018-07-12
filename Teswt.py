import logging
import xml.etree.cElementTree as ET

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def write_dict():
    file_dir = r'dtd.txt'
    reader = open(file_dir, 'r')
    lines = reader.readlines()
    entity_dict = {}
    entity_writer = open('entity_dict.txt', 'w+')
    for line in lines:
        entity = line[13:28].split('"')
        key = '&' + entity[0].replace(' ', '') + ';'
        value = entity[-1]
        entity_dict[key] = value
        entity_writer.write(key + ':' + value+'\n')
    entity_writer.close()


def write_dblp_to_xml():
    entity_dict = {}
    reader = open('entity_dict.txt', 'r')
    for item in reader.readlines():
        entity_dict[item.split(':')[0]] = item.split(':')[-1].replace('\n','')
    dblp_dir = r'/Volumes/CZ80/dblp.xml'
    dblp_reader = open(dblp_dir, 'r')
    dblp_writer = open('dblp_new.xml', 'w', encoding='utf-8')
    while True:
        line = dblp_reader.readline()
        if not line:
            break
        for single in entity_dict:
            if single in line:
                line = line.replace(single, entity_dict[single])
        dblp_writer.write(line)
        print(line)

write_dblp_to_xml()