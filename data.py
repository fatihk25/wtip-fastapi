import pandas as pd
import random
from faker import Faker
from random import randrange
from datetime import datetime

nr_of_data = 1000

fake = Faker('id_ID')

data = []

for data_id in range(nr_of_data):

    # Create transaction date 
    d1 = datetime.strptime(f'1/1/2015', '%m/%d/%Y')
    d2 = datetime.strptime(f'8/10/2022', '%m/%d/%Y')
    transaction_date = fake.date_between(d1, d2)
    commodity = ['Apel', 'Mangga', 'Bawang Merah', 'Kopi', 'Bawang Putih', 'Lada', 'Teh', 'Cabai Rawit', 'Cengkeh', 'Alpukat']

    #Create city
    city = fake.city()
    
    #create amount spent
    current_price = fake.pyfloat(right_digits=2, positive=True, min_value=1000, max_value=80000)

    last_price = fake.pyfloat(right_digits=2, positive=True, min_value=1000, max_value=80000)

    data.append([data_id, transaction_date, random.choice(commodity), city, current_price, last_price])

data_df = pd.DataFrame(data, columns=['ID', 'TransactionDate', 'Commodity' ,'City','Current Price', 'Last Price']) 
                
pd.pandas.set_option('display.max_columns', None)
print(data_df)
data_df.to_csv('dataset.csv') 