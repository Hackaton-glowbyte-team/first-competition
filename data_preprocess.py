
import pandas as pd
import re

class DataTransformer:
    def __init__(self):
        pass

    # Ваши другие функции здесь...

    def open_file(self, path=None):
        # читаем исходные датасеты и складываем в один
        train_ds = pd.read_csv('data/train_dataset.csv')
        test_ds = pd.read_csv('data/test_dataset.csv')
        try:
            close_test_ds = pd.read_csv(path)
            train_ds = pd.concat([train_ds, test_ds, close_test_ds])

            close_test_begin = pd.to_datetime(close_test_ds['date']).min()
            close_test_end = pd.to_datetime(close_test_ds['date']).max() + pd.to_timedelta(1,'d')

            print('начало закрытого теста:', close_test_begin, '    конец закрытого теста:', close_test_end)

            return train_ds, close_test_begin, close_test_end
        except:
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

        # Добавление данных о праздниках из файла 'data/holidays.csv'

        df_holidays = pd.read_csv('data/holidays.csv')
        df_holidays['date'] = pd.to_datetime(df_holidays['date'])

        # Assuming df_holidays and train_ds are your dataframes
        train_ds = pd.merge(train_ds, df_holidays, on='date', how='left')

        # Fill NaN values with 0
        train_ds['holidays'].fillna(0, inplace=True)
        train_ds['preholidays'].fillna(0, inplace=True)

        # Convert to int
        train_ds['holidays'] = train_ds['holidays'].astype(int)
        train_ds['preholidays'] = train_ds['preholidays'].astype(int)
        
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
            list_fact_columns=list([df.columns])
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
        train_ds = train_ds.merge(df_true_weather, left_on='date_hours', right_on='date_tw')
        train_ds = train_ds.drop(['date_hours', 'date_tw'], axis=1)

        return train_ds

    def transform(self, data):
        data = self.date_transform(data)
        data = self.fill_weather_columns(data)
        data = self.holydays(data)
        data = self.create_lags(data)
        # data = self.add_vvp2(data)
        data = self.add_true_weather(data)

        return data




