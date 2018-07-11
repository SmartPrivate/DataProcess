import logging
import DataModel
import datetime
import DBConnector
import re

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

reader = open(r'C:\\Users\\macha\\Desktop\\weibo.txt', 'r', errors='replace')

while True:
    line = reader.readline()
    if not line:
        break
    items = line.split('\t')
    model = DataModel.Weibo()
    model.url = items[0]
    model.author = items[1]
    content_ori = items[2]
    result = re.subn('//@.*', '', content_ori)
    result = re.subn('@.*? ', '', result[0])
    result = re.subn('@.*?：', '', result[0])
    result = re.subn('\(分享自.*', '', result[0])
    result = re.subn('\?+', '', result[0])
    result = re.subn('（.*秒拍.*?）', '', result[0])
    result = re.subn('\(.*秒拍.*?\)', '', result[0])
    result = re.subn('L.*秒拍视频', '', result[0])
    replace_list = ['O网页链接','O秒拍视频', '?查看图片', '(来自', '（分享自', 'L微博视频','分享自秒拍用户','...展开全文c','  的作品,一起来看~ ','我的秒拍作品，一起来看~']
    content = result[0]
    for word in replace_list:
        content = content.replace(word, '')
    if content.find('秒拍') != -1:
        print(content)
    if content == '':
        continue
    model.content = content
    emoji = re.findall('\[.*?\]', content)
    if len(emoji) > 0:
        model.emoji = ','.join(emoji)
    else:
        model.emoji = ''
