
import numpy as np
import pandas as pd
import datetime
import lightgbm as lgb
import sys
import re

import xgboost as xgb
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')
 
from data_preprocess import DataTransformer
NUM_ITERATIONS = 5000
random_state = 12345


if len(sys.argv) > 1:
    path = str(sys.argv[1])
    print("Путь к файлу", path)
    
else:
    print("Путь к файлу не найден, пожалуйста попробуйте еще раз")
    exit()


transformer = DataTransformer()



all_ds, test_begin, test_end = transformer.open_file(path)

all_ds = transformer.transform(all_ds)

# Отбираем признаки. Все лишние колонки здесь отбрасываем, кроме 'date', которую уберем позже 
feature_cols = list(all_ds.columns)

# выбрасываем взгляд в прошлое и расшифрованную погоду
drop_list = ['target', 'day_of_year', 'weather_pred', 'weather_fact', 'temp']

# выбрасываем признаки, найденные процедурно в процессе оптимизации
drop_list = drop_list + ['target_lag_48', 'target_lag_168'] 

for name in drop_list:
    feature_cols.remove(name)

# Формируем набор датасетов для обучения и проверки
features = all_ds[feature_cols]
target = all_ds['target']

# готовим учебный и тестовый датасеты

features_test, target_test = transformer.features_interval(features, target, test_begin, test_end)


feat_lgbm_test = features_test

lgbm_model_all_train = lgb.Booster(model_file='models/lgb_model_FULL_ds_no_aug.txt')

l_predict_test = lgbm_model_all_train.predict(feat_lgbm_test)




feat_xgb_test = features_test[transformer.xgb_feat]



xgb_model_all_train = XGBRegressor()
# загружаем модель из файла
xgb_model_all_train.load_model('models/xgb_modelbase feature_3.json')

xgb_predict_test = xgb_model_all_train.predict(feat_xgb_test)

predict = (xgb_predict_test + l_predict_test)/2

predict_result = pd.DataFrame( )

datetimes = all_ds.loc[features_test.index, 'date'] + pd.to_timedelta(all_ds.loc[features_test.index, 'time'], 'H')
predict_result['datetime'] = datetimes.values
predict_result['predict'] = predict
predict_result.reset_index(drop=True)

predict_result.to_csv('predict_result.csv', index=False)



