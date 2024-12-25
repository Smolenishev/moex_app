# 2024-12-25 12:50 срд Нвг
# тут сам страраюсь писать

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import datetime

st.set_page_config(layout="wide", initial_sidebar_state='expanded', page_title='MOEX  котировки')

#---------------------
# получение всх тикеров
url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"

j = requests.get(url).json()

data = [{k : r[i] for i, k in enumerate(j['securities']['columns'])} for r in j['securities']['data']]
df_t = pd.DataFrame(data)

df_t = df_t[['SECID', 'SHORTNAME']]

secid = df_t['SECID'].unique()


#---------------------
# левая панель

with st.sidebar:    
    # Выберете начальную дату
    d0 = st.date_input("Выберете начальную дату выборки: ", value=datetime.date(2024, 1, 1))
    st.write(d0)
    # Выберете завешающую дату
    d1 = st.date_input("Выберете завершающую дату выборки: ", value="today")
    st.write(d1)
    # Выбор тикера
    # ticker = st.selectbox("Выберите тикер:", ["SBER", "GAZP", "LKOH", "AFLT", "ABRD", "AFKS", "ALRS", "APTK", "DSKY", "FLOT", "GMKN", "MTSS", "SNGS", "MVID", "NLMK", "SIBN"])
    ticker = st.selectbox("Выберите ID:", secid, index=191)
    st.write('Справка по ID: ')
    st.table(df_t)



#---------------------
# получение данныы
# j = requests.get('http://iss.moex.com/iss/engines/stock/markets/shares/securities/SBER/candles.json?from=2024-01-01&till=2024-12-24&interval=24').json()

# url = f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from=2024-01-01&till=2024-12-24&interval=24'

# Форматирование дат для запроса
start_date_str = d0.strftime('%Y-%m-%d')
end_date_str = d1.strftime('%Y-%m-%d')

# url = f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from={d0}&till={d1}&interval=24'
url = f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from={start_date_str}&till={end_date_str}&interval=24'

j = requests.get(url).json()

data = [{k : r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
df = pd.DataFrame(data)
df['data'] = (pd.to_datetime(df['end'])).dt.date

# начальные и конечные значения
d_0 = df['data'].min()
p_0 = df[df['data']==d_0]['close'].values[0]


d_1 = df['data'].max()
p_1 = df[df['data']==d_1]['close'].values[0]

p_d = (p_1 - p_0).round(2)

p_d_p = ((p_d / p_0)*100).round(2)


#-----------------------
# 




#-----------------------
# представление в Streamlit
st.title("Данные Московской биржи: дневные котировки")
st.write("Data from the Moscow Stock Exchange. [https://www.moex.com/](https://www.moex.com/)")
st.write('Источник данных: http://iss.moex.com/iss/engines/stock/markets/shares/securities/')

st.divider()

st.subheader(f"Дневные данные по ID {ticker}:")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label=f'Начало: {start_date_str}', value=p_0)
with col2:
    st.metric(label=f'Окончание: {end_date_str}', value=p_1, delta=p_d)
with col3:
    st.metric(label="Изм. %: ", value=p_d_p)


col1, col2 = st.columns([1, 4])
with col1:    
    st.dataframe(df[['data', 'close']])

with col2:
    st.area_chart(df, x='data', y='close', y_label='руб.')




#------------------------------------------
st.divider()
st.write('Автор: Смоленышев Олег. smolenishev@oter-finance.ru')
st.write('Сайт автора: [https://otter-finance.ru](https://otter-finance.ru)')
st.write('Скрипт расположен: []()')
st.divider()
st.markdown(""" #### :blue[Окончание]""")
