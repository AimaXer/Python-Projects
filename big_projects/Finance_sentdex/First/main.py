import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import psycopg2 as pgsql

class DataManagement():
    def getDataFromDataBase(self, cursor):
        cursor.execute("""SELECT * FROM test_python;""")
        return pd.fromlist(cursor.fetchall())

    def updateDataBase(self, start_date, end_date, df, db_session):
        while start_date.strftime("%Y-%m-%d") != end_date:
            time = start_date.strftime("%Y-%m-%d")
            if start_date in df['Low']:
                data = (str(time), df['Low'][str(time)], df['High'][str(time)], df['Open'][str(time)], df['Close'][str(time)], df['Adj Close'][str(time)], int(df['Volume'][str(time)]))
                cursor.execute("""INSERT INTO test_python(date, low, high, open, close, adj_close, volume) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (date) DO NOTHING;""", data)
                db_session.commit()
            start_date += timedelta(days=1)

style.use('ggplot')
start_date = dt.datetime(2009,1,1)
end_date = dt.datetime.now()

df = web.DataReader('TSLA', 'yahoo', start_date)

db_session = pgsql.connect(host="10.0.0.22", port=5432, database="test", user="mchmielewski", password="1111")
cursor = db_session.cursor()

# DataManagement().updateDataBase(start_date, end_date, df, db_session)
print(DataManagement().getDataFromDataBase(cursor))

# df['Adj Close'].plot()
# plt.show()

cursor.close()
db_session.close()