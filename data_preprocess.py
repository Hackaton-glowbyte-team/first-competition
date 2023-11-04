
import pandas as pd
import numpy as np
import re

class DataTransformer:
    def __init__(self):

        self.xgb_feat = ["time","temp_pred","year","month","day_of_week","day","holidays_true","temp_last_day","target_lag_24","target_lag_72","target_lag_336","VVP","cloudy","rainy","windy","clear","rain_probability","has_rain_probability","P","U","WW","Td","N","S","W","E","last_evening_avg_target_0","last_evening_avg_temp_0","last_evening_avg_target_19","last_evening_avg_temp_19","last_evening_avg_target_22","last_evening_avg_temp_22","time_1","temp_pred_1","year_1","month_1","day_of_week_1","day_1","holidays_true_1","temp_last_day_1","target_lag_24_1","target_lag_72_1","target_lag_336_1","VVP_1","cloudy_1","rainy_1","windy_1","clear_1","rain_probability_1","has_rain_probability_1","P_1","U_1","WW_1","Td_1","N_1","S_1","W_1","E_1","last_evening_avg_target_0_1","last_evening_avg_temp_0_1","last_evening_avg_target_19_1","last_evening_avg_temp_19_1","last_evening_avg_target_22_1","last_evening_avg_temp_22_1","time_2","temp_pred_2","year_2","month_2","day_of_week_2","day_2","holidays_true_2","temp_last_day_2","target_lag_24_2","target_lag_72_2","target_lag_336_2","VVP_2","cloudy_2","rainy_2","windy_2","clear_2","rain_probability_2","has_rain_probability_2","P_2","U_2","WW_2","Td_2","N_2","S_2","W_2","E_2","last_evening_avg_target_0_2","last_evening_avg_temp_0_2","last_evening_avg_target_19_2","last_evening_avg_temp_19_2","last_evening_avg_target_22_2","last_evening_avg_temp_22_2","time_3","temp_pred_3","year_3","month_3","day_of_week_3","day_3","holidays_true_3","temp_last_day_3","target_lag_24_3","target_lag_72_3","target_lag_336_3","VVP_3","cloudy_3","rainy_3","windy_3","clear_3","rain_probability_3","has_rain_probability_3","P_3","U_3","WW_3","Td_3","N_3","S_3","W_3","E_3","last_evening_avg_target_0_3","last_evening_avg_temp_0_3","last_evening_avg_target_19_3","last_evening_avg_temp_19_3","last_evening_avg_target_22_3","last_evening_avg_temp_22_3","time_4","temp_pred_4","year_4","month_4","day_of_week_4","day_4","holidays_true_4","temp_last_day_4","target_lag_24_4","target_lag_72_4","target_lag_336_4","VVP_4","cloudy_4","rainy_4","windy_4","clear_4","rain_probability_4","has_rain_probability_4","P_4","U_4","WW_4","Td_4","N_4","S_4","W_4","E_4","last_evening_avg_target_0_4","last_evening_avg_temp_0_4","last_evening_avg_target_19_4","last_evening_avg_temp_19_4","last_evening_avg_target_22_4","last_evening_avg_temp_22_4","time_5","temp_pred_5","year_5","month_5","day_of_week_5","day_5","holidays_true_5","temp_last_day_5","target_lag_24_5","target_lag_72_5","target_lag_336_5","VVP_5","cloudy_5","rainy_5","windy_5","clear_5","rain_probability_5","has_rain_probability_5","P_5","U_5","WW_5","Td_5","N_5","S_5","W_5","E_5","last_evening_avg_target_0_5","last_evening_avg_temp_0_5","last_evening_avg_target_19_5","last_evening_avg_temp_19_5","last_evening_avg_target_22_5","last_evening_avg_temp_22_5","time_6","temp_pred_6","year_6","month_6","day_of_week_6","day_6","holidays_true_6","temp_last_day_6","target_lag_24_6","target_lag_72_6","target_lag_336_6","VVP_6","cloudy_6","rainy_6","windy_6","clear_6","rain_probability_6","has_rain_probability_6","P_6","U_6","WW_6","Td_6","N_6","S_6","W_6","E_6","last_evening_avg_target_0_6","last_evening_avg_temp_0_6","last_evening_avg_target_19_6","last_evening_avg_temp_19_6","last_evening_avg_target_22_6","last_evening_avg_temp_22_6","time_7","temp_pred_7","year_7","month_7","day_of_week_7","day_7","holidays_true_7","temp_last_day_7","target_lag_24_7","target_lag_72_7","target_lag_336_7","VVP_7","cloudy_7","rainy_7","windy_7","clear_7","rain_probability_7","has_rain_probability_7","P_7","U_7","WW_7","Td_7","N_7","S_7","W_7","E_7","last_evening_avg_target_0_7","last_evening_avg_temp_0_7","last_evening_avg_target_19_7","last_evening_avg_temp_19_7","last_evening_avg_target_22_7","last_evening_avg_temp_22_7","time_8","temp_pred_8","year_8","month_8","day_of_week_8","day_8","holidays_true_8","temp_last_day_8","target_lag_24_8","target_lag_72_8","target_lag_336_8","VVP_8","cloudy_8","rainy_8","windy_8","clear_8","rain_probability_8","has_rain_probability_8","P_8","U_8","WW_8","Td_8","N_8","S_8","W_8","E_8","last_evening_avg_target_0_8","last_evening_avg_temp_0_8","last_evening_avg_target_19_8","last_evening_avg_temp_19_8","last_evening_avg_target_22_8","last_evening_avg_temp_22_8","time_9","temp_pred_9","year_9","month_9","day_of_week_9","day_9","holidays_true_9","temp_last_day_9","target_lag_24_9","target_lag_72_9","target_lag_336_9","VVP_9","cloudy_9","rainy_9","windy_9","clear_9","rain_probability_9","has_rain_probability_9","P_9","U_9","WW_9","Td_9","N_9","S_9","W_9","E_9","last_evening_avg_target_0_9","last_evening_avg_temp_0_9","last_evening_avg_target_19_9","last_evening_avg_temp_19_9","last_evening_avg_target_22_9","last_evening_avg_temp_22_9","time_10","temp_pred_10","year_10","month_10","day_of_week_10","day_10","holidays_true_10","temp_last_day_10","target_lag_24_10","target_lag_72_10","target_lag_336_10","VVP_10","cloudy_10","rainy_10","windy_10","clear_10","rain_probability_10","has_rain_probability_10","P_10","U_10","WW_10","Td_10","N_10","S_10","W_10","E_10","last_evening_avg_target_0_10","last_evening_avg_temp_0_10","last_evening_avg_target_19_10","last_evening_avg_temp_19_10","last_evening_avg_target_22_10","last_evening_avg_temp_22_10","time_11","temp_pred_11","year_11","month_11","day_of_week_11","day_11","holidays_true_11","temp_last_day_11","target_lag_24_11","target_lag_72_11","target_lag_336_11","VVP_11","cloudy_11","rainy_11","windy_11","clear_11","rain_probability_11","has_rain_probability_11","P_11","U_11","WW_11","Td_11","N_11","S_11","W_11","E_11","last_evening_avg_target_0_11","last_evening_avg_temp_0_11","last_evening_avg_target_19_11","last_evening_avg_temp_19_11","last_evening_avg_target_22_11","last_evening_avg_temp_22_11","time_12","temp_pred_12","year_12","month_12","day_of_week_12","day_12","holidays_true_12","temp_last_day_12","target_lag_24_12","target_lag_72_12","target_lag_336_12","VVP_12","cloudy_12","rainy_12","windy_12","clear_12","rain_probability_12","has_rain_probability_12","P_12","U_12","WW_12","Td_12","N_12","S_12","W_12","E_12","last_evening_avg_target_0_12","last_evening_avg_temp_0_12","last_evening_avg_target_19_12","last_evening_avg_temp_19_12","last_evening_avg_target_22_12","last_evening_avg_temp_22_12","time_13","temp_pred_13","year_13","month_13","day_of_week_13","day_13","holidays_true_13","temp_last_day_13","target_lag_24_13","target_lag_72_13","target_lag_336_13","VVP_13","cloudy_13","rainy_13","windy_13","clear_13","rain_probability_13","has_rain_probability_13","P_13","U_13","WW_13","Td_13","N_13","S_13","W_13","E_13","last_evening_avg_target_0_13","last_evening_avg_temp_0_13","last_evening_avg_target_19_13","last_evening_avg_temp_19_13","last_evening_avg_target_22_13","last_evening_avg_temp_22_13","time_14","temp_pred_14","year_14","month_14","day_of_week_14","day_14","holidays_true_14","temp_last_day_14","target_lag_24_14","target_lag_72_14","target_lag_336_14","VVP_14","cloudy_14","rainy_14","windy_14","clear_14","rain_probability_14","has_rain_probability_14","P_14","U_14","WW_14","Td_14","N_14","S_14","W_14","E_14","last_evening_avg_target_0_14","last_evening_avg_temp_0_14","last_evening_avg_target_19_14","last_evening_avg_temp_19_14","last_evening_avg_target_22_14","last_evening_avg_temp_22_14","time_15","temp_pred_15","year_15","month_15","day_of_week_15","day_15","holidays_true_15","temp_last_day_15","target_lag_24_15","target_lag_72_15","target_lag_336_15","VVP_15","cloudy_15","rainy_15","windy_15","clear_15","rain_probability_15","has_rain_probability_15","P_15","U_15","WW_15","Td_15","N_15","S_15","W_15","E_15","last_evening_avg_target_0_15","last_evening_avg_temp_0_15","last_evening_avg_target_19_15","last_evening_avg_temp_19_15","last_evening_avg_target_22_15","last_evening_avg_temp_22_15","time_16","temp_pred_16","year_16","month_16","day_of_week_16","day_16","holidays_true_16","temp_last_day_16","target_lag_24_16","target_lag_72_16","target_lag_336_16","VVP_16","cloudy_16","rainy_16","windy_16","clear_16","rain_probability_16","has_rain_probability_16","P_16","U_16","WW_16","Td_16","N_16","S_16","W_16","E_16","last_evening_avg_target_0_16","last_evening_avg_temp_0_16","last_evening_avg_target_19_16","last_evening_avg_temp_19_16","last_evening_avg_target_22_16","last_evening_avg_temp_22_16","time_17","temp_pred_17","year_17","month_17","day_of_week_17","day_17","holidays_true_17","temp_last_day_17","target_lag_24_17","target_lag_72_17","target_lag_336_17","VVP_17","cloudy_17","rainy_17","windy_17","clear_17","rain_probability_17","has_rain_probability_17","P_17","U_17","WW_17","Td_17","N_17","S_17","W_17","E_17","last_evening_avg_target_0_17","last_evening_avg_temp_0_17","last_evening_avg_target_19_17","last_evening_avg_temp_19_17","last_evening_avg_target_22_17","last_evening_avg_temp_22_17","time_18","temp_pred_18","year_18","month_18","day_of_week_18","day_18","holidays_true_18","temp_last_day_18","target_lag_24_18","target_lag_72_18","target_lag_336_18","VVP_18","cloudy_18","rainy_18","windy_18","clear_18","rain_probability_18","has_rain_probability_18","P_18","U_18","WW_18","Td_18","N_18","S_18","W_18","E_18","last_evening_avg_target_0_18","last_evening_avg_temp_0_18","last_evening_avg_target_19_18","last_evening_avg_temp_19_18","last_evening_avg_target_22_18","last_evening_avg_temp_22_18","time_19","temp_pred_19","year_19","month_19","day_of_week_19","day_19","holidays_true_19","temp_last_day_19","target_lag_24_19","target_lag_72_19","target_lag_336_19","VVP_19","cloudy_19","rainy_19","windy_19","clear_19","rain_probability_19","has_rain_probability_19","P_19","U_19","WW_19","Td_19","N_19","S_19","W_19","E_19","last_evening_avg_target_0_19","last_evening_avg_temp_0_19","last_evening_avg_target_19_19","last_evening_avg_temp_19_19","last_evening_avg_target_22_19","last_evening_avg_temp_22_19","time_20","temp_pred_20","year_20","month_20","day_of_week_20","day_20","holidays_true_20","temp_last_day_20","target_lag_24_20","target_lag_72_20","target_lag_336_20","VVP_20","cloudy_20","rainy_20","windy_20","clear_20","rain_probability_20","has_rain_probability_20","P_20","U_20","WW_20","Td_20","N_20","S_20","W_20","E_20","last_evening_avg_target_0_20","last_evening_avg_temp_0_20","last_evening_avg_target_19_20","last_evening_avg_temp_19_20","last_evening_avg_target_22_20","last_evening_avg_temp_22_20","time_21","temp_pred_21","year_21","month_21","day_of_week_21","day_21","holidays_true_21","temp_last_day_21","target_lag_24_21","target_lag_72_21","target_lag_336_21","VVP_21","cloudy_21","rainy_21","windy_21","clear_21","rain_probability_21","has_rain_probability_21","P_21","U_21","WW_21","Td_21","N_21","S_21","W_21","E_21","last_evening_avg_target_0_21","last_evening_avg_temp_0_21","last_evening_avg_target_19_21","last_evening_avg_temp_19_21","last_evening_avg_target_22_21","last_evening_avg_temp_22_21","time_22","temp_pred_22","year_22","month_22","day_of_week_22","day_22","holidays_true_22","temp_last_day_22","target_lag_24_22","target_lag_72_22","target_lag_336_22","VVP_22","cloudy_22","rainy_22","windy_22","clear_22","rain_probability_22","has_rain_probability_22","P_22","U_22","WW_22","Td_22","N_22","S_22","W_22","E_22","last_evening_avg_target_0_22","last_evening_avg_temp_0_22","last_evening_avg_target_19_22","last_evening_avg_temp_19_22","last_evening_avg_target_22_22","last_evening_avg_temp_22_22","time_23","temp_pred_23","year_23","month_23","day_of_week_23","day_23","holidays_true_23","temp_last_day_23","target_lag_24_23","target_lag_72_23","target_lag_336_23","VVP_23","cloudy_23","rainy_23","windy_23","clear_23","rain_probability_23","has_rain_probability_23","P_23","U_23","WW_23","Td_23","N_23","S_23","W_23","E_23","last_evening_avg_target_0_23","last_evening_avg_temp_0_23","last_evening_avg_target_19_23","last_evening_avg_temp_19_23","last_evening_avg_target_22_23","last_evening_avg_temp_22_23","target_1","temp_1","target_5","temp_5","target_9","temp_9"]
        pass

    def features_interval(self, features, target, date1, date2):
        """
        Функция для выделения временных интервалов из таблиц признаков и целей
        на этом этапе отбрасываем колонку 'date'
        """
        features_interval = features[ (features['date']>=date1) & (features['date']<date2) ]
        target_interval = target[features_interval.index]
        features_interval = features_interval.drop('date', axis=1)
        
        return features_interval, target_interval

    def open_file(self, path=None):
        # читаем исходные датасеты и складываем в один

        try:
            print('i am here')
            close_test_ds = pd.read_csv(path)
        
            train_ds = close_test_ds

            close_test_begin = pd.to_datetime('2023-08-01')
            close_test_end = pd.to_datetime('2023-09-30') + pd.to_timedelta(1,'d')

        
            
            return train_ds, close_test_begin, close_test_end
        
        except:
            print("Файл не найден, попробуйте еще раз")
            exit()

            train_ds = pd.read_csv('data/train_dataset.csv')
            test_ds = pd.read_csv('data/test_dataset.csv')


            train_ds = pd.concat([train_ds, test_ds])

            # запоминаем дату начала тестовых данных, потом также поступим и с закрытым датасетом
            open_test_begin = pd.to_datetime(test_ds['date']).min()
            open_test_end = pd.to_datetime(test_ds['date']).max() + pd.to_timedelta(1,'d')
            print('начало открытого теста:', open_test_begin, '    конец открытого теста:', open_test_end)

            return train_ds, open_test_begin, open_test_end

    def date_transform(self, train_ds):
        # преобразуем дату и делаем из нее колонки
        train_ds['date'] = pd.to_datetime(train_ds['date'])
        train_ds['year'] = train_ds['date'].dt.year
        train_ds['month'] = train_ds['date'].dt.month
        train_ds['day_of_week'] = train_ds['date'].dt.dayofweek
        train_ds['day'] = train_ds['date'].dt.day
        train_ds['day_of_year'] = train_ds['date'].dt.dayofyear

        return train_ds

    def fill_weather_columns(self, df):


        def in_what_list(weather, big_list):
            for list_number, small_list in enumerate(big_list):
                if any(word in weather for word in small_list):
                    return list_number+1
            return 0

        def weather_split2(row):
            weather = row['weather_pred']
            cloudy_list = [['проясн', 'пер.об.', 'п/об'], ['пасм', 'обл']]
            rainy_list = [['дождь', 'снег', 'д+сн'], ['гроз', 'ливень']]
            windy_list = [['вет'],['штор']]
            clear_list = [['проясн'], ['ясно'], ['солнеч']]
            numbers = re.findall(r'\d+', weather)
            cloudy = in_what_list(weather, cloudy_list)
            rainy = in_what_list(weather, rainy_list)
            windy = in_what_list(weather, windy_list)
            clear = in_what_list(weather, clear_list)
            rain_probability = 0 if len(numbers)==0 else int(numbers[0])
            has_rain_probability = int(len(numbers)==0)
            return cloudy, rainy, windy, clear, rain_probability, has_rain_probability

        df['weather_pred'] = df['weather_pred'].fillna('')
        df['cloudy'], df['rainy'], df['windy'], df['clear'], df['rain_probability'], df['has_rain_probability'] = \
                    zip(*df.apply(weather_split2, axis=1))
        return df

    def holydays(self, train_ds):
        """
        Добавление данных о праздниках из файла 'data/holidays_true.csv'
        """
        df_holidays_true = pd.read_csv('data/holidays_true.csv')
        df_holidays_true['date'] = pd.to_datetime(df_holidays_true['date'])
        
        # Assuming df_holidays and train_ds are your dataframes
        train_ds = pd.merge(train_ds, df_holidays_true, on='date', how='left')
        
        # Fill NaN values with 0
        train_ds['holidays_true'].fillna(0, inplace=True)
        train_ds['preholidays_true'].fillna(0, inplace=True)
        
        # Convert to int
        train_ds['holidays_true'] = train_ds['holidays_true'].astype(int)
        train_ds['preholidays_true'] = train_ds['preholidays_true'].astype(int)

        return train_ds

    def create_lags(self, train_ds):
        """
        Добавление колонок с временными лагами
        """
        # создаем столбец 'temp_last_day'
        train_ds['temp_last_day'] = train_ds['temp'].shift(24)

        # заполняем пропущенные значения в 'temp_last_day'
        train_ds['temp_last_day'].fillna(train_ds['temp_pred'], inplace=True)

        # создаем столбцы с временными лагами для 'target'
        lags = [24, 48, 72, 7*24, 14*24]
        
        for lag in lags:
            train_ds[f'target_lag_{lag}'] = train_ds['target'].shift(lag)

        # заполняем пропущенные значения в столбцах с лагами
        for lag in lags:
            train_ds[f'target_lag_{lag}'].fillna(0, inplace=True)
        
        return train_ds

    def add_vvp2(self, data, file_source='data/VVP.csv'):
    
        """
        Функция добавляет данные о ВВП из файла 'data/VVP.csv' в датасет
        сырой датафрем подаем на вход
        """
        # обработаем файл с динамикой ВВП
        vvp = pd.read_csv(file_source)
        # преобразуем дату файла-источника в формат datetime64 и дропнем один столбик
        vvp['date'] = pd.to_datetime(vvp['date'], format ='%Y-%m-%d %H:%M:%S')
        vvp.drop('for_month',axis=1,inplace=True) 
        
        # обработаем основной фрейм - создадим столбец для соединения, который потом удалим
        data['date_temp'] = pd.to_datetime(data['date'], format = '%Y-%m-%d' )
        data['date_temp'] = data['date_temp'] + pd.to_timedelta(data['time'] , 'H')
        
        # соединяем основной фрейм и ВВП по дате объявления показтеля ВВП
        for idx in reversed(vvp.index):
            data.loc[data['date_temp']>=vvp.date[idx],'VVP'] = vvp.VVP_perc[idx]
            
        data.drop('date_temp',axis=1,inplace=True)   

        return data


    def add_true_weather(self, train_ds):
        '''
        Функции для работы с данными о фактической погоде из 'data/preprocessing_loaded_table.csv'
        '''
        # Кодировка информации об осадках из колонки WW
        def true_weather_WW_replace(ww):
            if ww=='нет осадков':
                return 0
            elif ww=='слабый дождь':
                return 1
            elif (ww=='сильный дождь') or (ww=='снег'):
                return 2
            else:
                return 3

        # Вычисление Timestamp из даты и времени
        def row_plus_hours_to_index(row):
            return row['date'] + pd.to_timedelta(row['time'] , 'H')

        # Функция для сдвига на сутки (в скачанном датасете разбивка по 30 мин, поэтому timeshift=48)
        def shift_features_fact(df, timeshift=48):
            list_fact_columns=list(df.columns)
            list_fact_columns.remove('date_tw')
            new_df = df.copy()
            for column in list_fact_columns:
                
                new_df[column] = new_df[column].shift(timeshift)

            return new_df

        # Читаем файл с архивом фактической погоды
        df_true_weather = pd.read_csv('data/preprocessing_loaded_table.csv')

        # Форматируем колонки
        df_true_weather['WW'] = df_true_weather['WW'].apply(true_weather_WW_replace)
        df_true_weather['date'] = pd.to_datetime(df_true_weather['date'])
        df_true_weather = df_true_weather.rename(columns={'date':'date_tw'})
        
        # Применяем сдвиг на сутки, чтобы не заглядывать в будущее
        df_true_weather = shift_features_fact(df_true_weather)
       
        # Добавляем в датасет
        train_ds['date_hours'] = train_ds.apply(row_plus_hours_to_index, axis=1)
        train_ds = train_ds.merge(df_true_weather,how='left', left_on='date_hours', right_on='date_tw')
        train_ds = train_ds.drop(['date_hours', 'date_tw'], axis=1)
      
        return train_ds
    
    def mean_hour(self, train_ds):
        def mean_evening(values, evening=19):
            return values[evening:].mean()

        evening_slices = [0, 19, 22]
            
        for evening_slice in evening_slices:
            train_ds[['last_evening_avg_target_'+str(evening_slice), 'last_evening_avg_temp_'+str(evening_slice)]] = \
                train_ds[['date', 'target', 'temp']].groupby(by='date').transform(mean_evening, evening=evening_slice).shift(24)
        
        return train_ds
    
    def feature_window(self, train_ds):
        
        FEATURE_WINDOW_SIZE = 24
        
        feature_cols_no_date = list(train_ds.columns)
        feature_cols_no_date.remove('date')

        drop_list = ['target', 
                     'day_of_year', 
                     'weather_pred', 
                     'weather_fact', 
                     'temp',
                     'target_lag_48', 
                     'target_lag_168']
        
        for name in drop_list:
            feature_cols_no_date.remove(name)


        for lag in range(1,FEATURE_WINDOW_SIZE):
            for column in feature_cols_no_date:
                train_ds[column+'_'+str(lag)] = train_ds[column].shift(lag)

        return train_ds
    
    def  lag_for_hours(self, train_ds):

        target_lags=[1, 5, 9]

        for lag in target_lags:
            train_ds['target_'+str(lag)] = train_ds['target'].shift(lag).where(train_ds['time']<lag, np.NaN)
            train_ds['temp_'+str(lag)] = train_ds['temp'].shift(lag).where(train_ds['time']<lag, np.NaN)

        return train_ds
    


    def transform(self, data):
       
        data = self.date_transform(data)
        data = self.holydays(data)
        data = self.create_lags(data)
        data = self.add_vvp2(data)
        data = self.fill_weather_columns(data)
        data = self.add_true_weather(data)
        data = self.mean_hour(data)
        data = self.feature_window(data)
        data = self.lag_for_hours(data)
        return data




