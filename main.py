
import numpy as np
import pandas as pd
import datetime
import lightgbm as lgb
import sys
import re
 
from data_preprocess import DataTransformer
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

print(features.columns)
print(all_ds.columns)

# готовим учебный и тестовый датасеты
features_all_train, target_all_train = transformer.features_interval(features, target, '2019-01-01', test_begin)
features_test, target_test = transformer.features_interval(features, target, test_begin, test_end)


# Здесь обучаем на всех данных, которые были нам предоставлены 
lgbm_model_all_train = lgb.LGBMRegressor(num_leaves=15, learning_rate=0.02, num_iterations=10000, 
                               feature_fraction=0.987, random_state=random_state, objective='regression_l1', n_jobs=-1)
lgbm_model_all_train.fit(features_all_train, target_all_train)


predict = lgbm_model_all_train.predict(features_test)
predict_result = pd.DataFrame( features.loc[features_test.index, 'date'] )
predict_result['predict'] = predict
predict_result = predict_result.groupby(by='date').sum().reset_index()

predict_result.to_csv('predict_result.csv', index=False)



