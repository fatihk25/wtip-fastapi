import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


url = 'https://raw.githubusercontent.com/fatihk25/wtip-fastapi/main/dataset.csv'
dataset = pd.read_csv(url)


def predict_by_commodity(commodity):
    plt.switch_backend('Agg')

    data = dataset[dataset['Commodity'] == commodity]
    payload = {
        'Price': data['Current Price'],
        'Commodity': data['Commodity'],
        'Year': pd.DatetimeIndex(data['TransactionDate']).year
    }
    data = pd.DataFrame(payload)

    price = data.groupby('Year')['Price'].sum()

    x = price.index
    y = price

    linreg = LinearRegression()
    x = np.array(x).reshape(-1, 1)
    linreg.fit(x, y)

    next_x = x[-1] + 1
    next_x = np.array(next_x).reshape(-1, 1)
    pred_x = linreg.predict(next_x, )

    # print('\nPrediksi x \n', pred_x.item())

    plt.scatter(x, y)
    plt.plot(x, y)
    plt.xlabel('Month')
    plt.ylabel('Total Price')

    plt.scatter(next_x, pred_x, c='red')
    pred_y = linreg.predict(x)
    plt.plot(x, pred_y)
    plt.savefig('./images/' + str(commodity) + '.png')
    # plt.show()

    # MSE = mean_squared_error(y,pred_y)
    # print('\nMSE = ', MSE)


def predict():
    commodities = dataset.groupby(['Commodity'])['Commodity']
    commodities = commodities.nunique().index

    for commodity in commodities:
        predict_by_commodity(commodity)
