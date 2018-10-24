import logging
import json
import requests
import DataModel, DBConnector
import os
import redis
import WordCutter
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

models = DBConnector.query_all(DataModel.YelpUser)
with_friend_models = list(filter(lambda o: o.friends != 'None', models))
db_session = DBConnector.create_db_session(DBConnector.DBName.MySQL)
new_session = db_session()
for model in with_friend_models:
    user_models = []
    model: DataModel.YelpUser
    friends = model.friends.split(', ')
    for friend in friends:
        user_model = DataModel.YelpFriend()
        user_model.user_id = model.user_id
        user_model.friend_user_id = friend
        friend_in_user = new_session.query(DataModel.YelpUser).filter(DataModel.YelpUser.user_id == friend).all()
        user_model.is_in_t_user = len(friend_in_user)
        user_models.append(user_model)
    new_session.bulk_save_objects(user_models)
    new_session.commit()
    print('Finish user_sid {0}'.format(model.sid))
