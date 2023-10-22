# %%
import subprocess
import sys

# %%
try:
    import datetime
    print('Библиотека datetime уже установлена')
except ImportError:
    print('Библиотека datetime не установлена. Установка...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime'])
    import datetime

# %%
try:
    import suntime
    print('Библиотека suntime уже установлена')
except ImportError:
    print('Библиотека suntime не установлена. Установка...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'suntime'])
    import suntime

# %%
import pandas as pd
import numpy as np

from os.path import join
from pathlib import Path
import os


from datetime import datetime, timedelta
from suntime import Sun, SunTimeException




# %%
path = Path("C:/Users/79099/Desktop/Hakaton_GlowByte/first-competition-2/data/")
filename = 'da_true_weather.csv'


# %%
def preprocessing(x):
    ## Функция заменяет значения в столбце с осадками и делит их на 4 категории :
    ## 1) Нет осадков
    ## 2) Слабый дождь
    ## 3) Сильный дождь
    ## 4) Снег
    
    x.WW = x.WW.str.lower()
    x.WW = x.WW.fillna('нет осадков')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), дождь', 'сильный дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), дождь, снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег, дождь', 'снег')
    x.WW = x.WW.replace('ливень (ливни), снег, дождь', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь, дымка', 'слабый дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) ливень (ливни), снег, дождь', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь, дымка', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег, дымка', 'снег')
    x.WW = x.WW.replace('ливень (ливни), дождь, снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь, снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег', 'снег')
    x.WW = x.WW.replace('снег, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег, дождь, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег, дождь', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег', 'снег')
    x.WW = x.WW.replace('ливень (ливни), снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('сильный(ая)(ые) снег', 'снег')
    x.WW = x.WW.replace('снег, дождь, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) морось', 'слабый дождь')
    x.WW = x.WW.replace('дымка', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) морось, дымка', 'слабый дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) ливень (ливни)', 'сильный дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) ливень (ливни), снег', 'снег')
    x.WW = x.WW.replace('частичный (охватывающий часть аэродрома) туман', 'слабый дождь')
    x.WW = x.WW.replace('замерзающий(ая) (переохлажденный(ая)) туман', 'снег')
    x.WW = x.WW.replace('клочьями туман', 'слабый дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) ливень (ливни), дождь, снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег, дождь, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), дождь, небольшой град и/или снежная крупа', 'снег')
    x.WW = x.WW.replace('частичный (охватывающий часть аэродрома) туман, дымка', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), дождь, дымка', 'сильный дождь')
    x.WW = x.WW.replace('морось, дымка', 'слабый дождь')
    x.WW = x.WW.replace('морось, дымка', 'слабый дождь')
    x.WW = x.WW.replace('дымка, дым', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) замерзающий(ая) (переохлажденный(ая)) морось, дымка', 'снег')
    x.WW = x.WW.replace('ливень (ливни), снег, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) гроза, дождь', 'сильный дождь')
    x.WW = x.WW.replace('ливень (ливни), дождь', 'сильный дождь')
    x.WW = x.WW.replace('снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('клочьями туман, дымка', 'слабый дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) дождь,частичный (охватывающий часть аэродрома) туман', 'сильный дождь')
    x.WW = x.WW.replace('гроза', 'сильный дождь')
    x.WW = x.WW.replace('ливень (ливни), небольшой град и/или снежная крупа', 'снег')
    x.WW = x.WW.replace('поземный туман', 'слабый дождь')
    x.WW = x.WW.replace('дымка,поземный туман', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь, снег, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) замерзающий(ая) (переохлажденный(ая)) морось', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег, слабый(ая)(ые) замерзающий(ая) (переохлажденный(ая)) дождь', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), небольшой град и/или снежная крупа', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег,частичный (охватывающий часть аэродрома) туман, дымка', 'снег')
    x.WW = x.WW.replace('дымка,клочьями туман', 'слабый дождь')
    x.WW = x.WW.replace('дождь, дымка', 'слабый дождь')
    x.WW = x.WW.replace('сильный(ая)(ые) ливень (ливни), снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('сильный(ая)(ые) снег,низовая (метель, буря) снег', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), дождь, туман', 'сильный дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) замерзающий(ая) (переохлажденный(ая)) дождь, дымка', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) ливень (ливни), снег, небольшой град и/или снежная крупа', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) дождь, туман', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) морось,частичный (охватывающий часть аэродрома) туман, дымка', 'слабый дождь')
    x.WW = x.WW.replace('слабый(ая)(ые) замерзающий(ая) (переохлажденный(ая)) дождь', 'снег')
    x.WW = x.WW.replace('слабый(ая)(ые) снег, поземок, снег', 'снег')
    x.WW = x.WW.replace('снег, поземок, снег', 'снег')
    x.WW = x.WW.replace('дым', 'слабый дождь')
    x.WW = x.WW.replace('снег, дождь', 'снег')
    x.WW = x.WW.replace('дождь, снег', 'снег')
    x.WW = x.WW.replace('туман', 'слабый дождь')
    x.WW = x.WW.replace('поземок, снег', 'снег')
    x.WW = x.WW.replace('гроза, дождь', 'сильный дождь')
    return x

# %%
def wind_direction(column):
    'Новые столбцы: N, S, W, E'
    if column == 'Ветер, дующий с юго-юго-запада':
        return 0, 1, 0.5, 0
    if column == 'Ветер, дующий с юго-запада':
        return 0, 1, 1, 0
    if column == 'Ветер, дующий с западо-юго-запада':
        return 0, 0.5, 1, 0
    if column == 'Ветер, дующий с запада':
        return 0, 0, 1, 0
    if column == 'Ветер, дующий с западо-северо-запада':
        return 0.5, 0, 1, 0
    if column == 'Ветер, дующий с северо-запада':
        return 1, 0, 1, 0
    if column == 'Ветер, дующий с северо-северо-запада':
        return 1, 0, 0.5, 1
    if column == 'Ветер, дующий с северо-северо-востока':
        return 1, 0, 0, 0.5
    if column == 'Ветер, дующий с севера':
        return 1, 0, 0, 0
    if column == 'Переменное направление':
        return 1, 1, 1, 1
    if column == 'Ветер, дующий с юга':
        return 0, 1, 0, 0
    if column == 'Ветер, дующий с северо-востока':
        return 1, 0, 0, 1
    if column == 'Ветер, дующий с востоко-северо-востока':
        return 0.5, 0, 0, 1
    if column == 'Ветер, дующий с востока':
        return 0, 0, 0, 1
    if column == 'Ветер, дующий с юго-востока':
        return 0, 1, 0, 1
    if column == 'Ветер, дующий с юго-юго-востока':
        return 0, 1, 0, 0.5
    if column == 'Ветер, дующий с востоко-юго-востока':
        return 0, 0.5, 0, 1
    if column == 'Штиль, безветрие':
        return 0, 0, 0, 0


# %%
def directions(data):
    '''
    Функция создает 4 новых признака по направлению ветра.
    N - north
    S - south
    W - west
    E - east
    '''
    data['wind'] = data['DD'].apply(wind_direction)
    data[['N', 'S', 'W', 'E']] = data['wind'].apply(lambda x: pd.Series(x))
    data.drop('wind', axis=1, inplace=True)
    return data

# %%
def processing_table(df):
    df.rename(columns = {'Местное время в Храброво / им. императрицы Елизаветы Петровны (аэропорт)':'date'}, inplace = True )
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    df = df.sort_values(by='date')
    df = df.set_index('date')
    df = preprocessing(df)
    df = directions(df)

    return df

# %%
def preprocessing_loaded_table(path, filename):
    df_true_weather = pd.read_csv(join(path, filename), sep=';')
    df_true_weather = processing_table(df_true_weather)
    display(df_true_weather.head(5))
    return df_true_weather
     



# %%
df_true_weather =  preprocessing_loaded_table(path, filename) 



