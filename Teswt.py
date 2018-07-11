import logging
import sys
import xml.etree.cElementTree as ET

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

file_dir = r'D:\DataSets\DBLP\dblp.xml'

reader=open(file_dir,'r')

