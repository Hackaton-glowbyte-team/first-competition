import pandas as pd

def add_light_work(data):
    """
    Функция добавляет данные о времени включения света из файла 'time_city_light.csv'
    подаем на вход c сырой датой
    """
    # обработаем файл с временем вкл освящения
    light = pd.read_csv('data/time_city_light.csv')
    light['turn_on'] = pd.to_datetime(light['on'], format='%H-%M').dt.time
    light['turn_off'] = pd.to_datetime(light['off'], format='%H-%M').dt.time
    light.drop(['on','off'], inplace=True, axis=1) 
        
    # обработаем основной фрейм - создадим столбец времени, который потом удалим
    data['date_temp'] = pd.to_datetime(data['date'], format = '%Y-%m-%d' )
    data['date_temp'] = data['date_temp'] + pd.to_timedelta(data['time'] , 'H')

    def is_light(input_dt):
        """
        Функция сравнивает значения с временем вкл. света.
        если освещение включено, возвращает 1. 
        """
        # извлекаем месяц и день из входящей даты
        month = input_dt.month
        day = input_dt.day
        # находим график работы освещения в справочном файле
        row = light.loc[(month==light['month'])  & (light['day']<=day),:].tail(1)

        # извлекаем время из timestamp и сравниваем 
        tm = input_dt.time()
        if tm<row.turn_off.values or tm>row.turn_on.values:
            return 1
        else:
            return 0
    
        
    data['is_light'] = data['date_temp'].map(is_light)
    data.drop('date_temp',axis=1,inplace=True)
       
    return data

def add_euro(df):
    """
    Функция добавляет данные о курсе ЕВРО, которые устанавливает ЦБ РФ 
    на завтрашний день из файла 'euro_info.csv'
    подаем на вход c сырой датой
    """
    # обработаем файл с курсом
    euro = pd.read_csv('data/euro_info.csv',)
    euro['curs'] = euro['curs'].astype('int')
    euro['data'] = pd.to_datetime(euro['data'], format = '%d.%m.%Y')

    df['date_temp'] = pd.to_datetime(df['date'], format = '%Y-%m-%d' )
    # берем последнее значение из 2018 года 
    last_value_2018 = euro[euro['data'].dt.year==2018].head(1).curs.values
    # соединяем фреймы
    result = pd.merge(df,euro,how='left',left_on='date_temp',right_on='data')
    # в начале года берем инфу из 2018
    result['curs'].iloc[0] = last_value_2018
    # заполняем пропуски на выходных и т.д.
    result['curs'].fillna(method='ffill',inplace=True)
    result.drop(['date_temp','data'],inplace=True,axis=1)
    return result

def add_stock(df):
    """
    Функция добавляет данные торгов на бирже на момент закрытия 
    из файла 'stock.csv'
    подаем на вход c сырой датой
    """
    # обработаем файл сырой для создания времени сопряжения
    df['date_temp'] = pd.to_datetime(df['date'], format = '%Y-%m-%d' )
    # обработаем файл с исходными данными
    stock = pd.read_csv('data/stock.csv')
    stock['TRADEDATE'] = pd.to_datetime(stock['TRADEDATE'], format = '%d.%m.%Y' )
    

    last_MOEX_2018 = stock[stock['TRADEDATE'].dt.year==2018].head(1).MOEX.values
    last_RTSI_2018 = stock[stock['TRADEDATE'].dt.year==2018].head(1).RTSI.values
    # соединяем фреймы
    result = pd.merge(df,stock,how='left',left_on='date_temp',right_on='TRADEDATE')
    # в начале года берем инфу из 2018
    result['MOEX'].iloc[0] = last_MOEX_2018
    result['RTSI'].iloc[0] = last_RTSI_2018
    # заполняем пропуски на выходных и т.д.
    result['MOEX'].fillna(method='ffill',inplace=True)
    result['RTSI'].fillna(method='ffill',inplace=True)
    # удаляем временные и лишние столбцы
    result.drop(['date_temp','TRADEDATE'],inplace=True, axis=1)
    return result

def add_ipp_mm(df):
    """
    Функция добавляет данные по индексу промышленного производства из Росстата. 
    Данные появляются примерно с месячной задержкой относительно рассматриваемого 
    месяца. В столбце 'date' лежит дата выхода информации. Индекс - "К предыдущему
     периоду". подаем на вход функции датафрейм c сырой датой
    """
    # обработаем входной файл для создания времени сопряжения
    df['date_temp'] = pd.to_datetime(df['date'], format = '%Y-%m-%d' )

    # обработаем файл с исходными данными
    df_mm = pd.read_csv('data/IPP_mm.csv')
    df_mm['date_inf'] = pd.to_datetime(df_mm['date_inf'], format = '%d.%m.%Y' )
    df_mm = df_mm.add_suffix('_mm')
    # сливаем в один датафрейм 
    mm_result = pd.merge(df,df_mm,how='left',left_on='date_temp',right_on='date_inf_mm')
    # данные по дням, которые мы не знаем берем по последнему значению
    ls_data = ['sum_mm','mining_mm','produce_mm','supply_mm','water_mm']
    mm_result[ls_data] = mm_result[ls_data].ffill()
    # удаляем столбцы сопряжения
    mm_result.drop(['date_temp','date_inf_mm'],inplace=True, axis=1)
    return mm_result
    
def add_ipp_yy(df):
    """
    Функция добавляет данные по индексу промышленного производства из Росстата. 
    Данные появляются примерно с месячной задержкой относительно рассматриваемого 
    месяца. В столбце 'date' лежит дата выхода информации. Индекс - "Отчетный месяц к 
    соответствующему месяцу предыдущего года". подаем на вход функции датафрейм c сырой датой
    """
    # обработаем входной файл для создания времени сопряжения
    df['date_temp'] = pd.to_datetime(df['date'], format = '%Y-%m-%d' )

    # обработаем файл с исходными данными
    df_yy = pd.read_csv('data/IPP_yy.csv')
    df_yy['date_inf'] = pd.to_datetime(df_yy['date_inf'], format = '%d.%m.%Y' )
    df_yy = df_yy.add_suffix('_yy')
    # сливаем в один датафрейм 
    yy_result = pd.merge(df,df_yy,how='left',left_on='date_temp',right_on='date_inf_yy')
    # данные по дням, которые мы не знаем берем по последнему значению
    ls_data = ['sum_yy','mining_yy','produce_yy','supply_yy','water_yy']
    yy_result[ls_data] = yy_result[ls_data].ffill()
    # удаляем столбцы сопряжения
    yy_result.drop(['date_temp','date_inf_yy'],inplace=True, axis=1)
    return yy_result


