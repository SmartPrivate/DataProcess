import logging

import DataModel, DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

model_list = DBConnector.get_weibo_all()
count_model = []
writer=open('with_at.txt','w',encoding='utf-8')
for model in model_list:
    model: DataModel.Weibo
    if '@' in model.weibo_content:
        print(str(model.sid)+':'+model.weibo_content)
        count_model.append(str(model.sid)+':'+model.weibo_content+'\n')
print(len(count_model))
writer.writelines(count_model)