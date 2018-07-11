import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

filedir=r'C:\Users\macha\iCloudDrive\Documents\DataSource\核心期刊数据\图象图形\1-500.txt'

reader=open(filedir,errors='ignore')
lines=reader.readlines()

for line in lines:
    print(line)