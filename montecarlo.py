import asyncio
import json
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from pandas_datareader import data as wb
from scipy.stats import norm

from model.MonteCarloReturn import MonteCarloReturn

api_key = '2451a9a6a8afb255ffeb81038b5d5628'

def import_stock_data(tickers, start = '2010-01-01', end = datetime.today().strftime('%Y-%m-%d')):
    data = pd.DataFrame()
    if len(tickers) ==1:
        if(tickers == '^GSPC'):
            prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{tickers}?serietype=line&apikey={api_key}').json()
        else:
            prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{tickers[0]}?serietype=line&apikey={api_key}&from=2015-01-01').json()
        a = []
        for x in prices['historical']:
            a.append(x['close'])
        if (tickers == '^GSPC'):
            data[tickers] = a
        else:
            data[tickers[0]] = a
        data = pd.DataFrame(data)
    else:
        if(tickers == "^GSPC"):
            prices = requests.get(
                f'https://financialmodelingprep.com/api/v3/historical-price-full/^GSPC?serietype=line&apikey={api_key}').json()
            a = []

            for x in prices['historical']:
                a.append(x['close'])
            if (tickers == '^GSPC'):
                data[tickers] = a
            else:
                data[tickers] = a
            data = pd.DataFrame(data)
        else:
            for t in tickers:
                if (t == '^GSPC'):
                    prices = requests.get(
                            f'https://financialmodelingprep.com/api/v3/historical-price-full/^GSPC?serietype=line&apikey={api_key}').json()
                else:
                    prices = requests.get(
                            f'https://financialmodelingprep.com/api/v3/historical-price-full/{t}?serietype=line&apikey={api_key}&from=2015-01-01').json()
                a = []


                for x in prices['historical']:
                    a.append(x['close'])
                if (t == '^GSPC'):
                    data[t] = a
                else:
                    data[t] = a
                data = pd.DataFrame(data)
    return(data)

def log_returns(data):
    return (np.log(1+data.pct_change()))
def simple_returns(data):
    return ((data/data.shift(1))-1)

def market_data_combination(data, mark_ticker = "^GSPC", start='2010-1-1'):
    market_data = import_stock_data(mark_ticker, start)

    market_rets = log_returns(market_data).dropna()
    ann_return = np.exp(market_rets.mean()*252).values-1
    data = data.merge(market_data, left_index=True, right_index=True)
    return data, ann_return

def beta_sharpe(data, mark_ticker = "^GSPC", start='2010-1-1', riskfree = 0.025):

    """
    Input:
    1. data: dataframe of stock price data
    2. mark_ticker: ticker of the market data you want to compute CAPM metrics with (default is ^GSPC)
    3. start: data from which to download data (default Jan 1st 2010)
    4. riskfree: the assumed risk free yield (US 10 Year Bond is assumed: 2.5%)

    Output:
    1. Dataframe with CAPM metrics computed against specified market procy
    """
    # Beta
    dd, mark_ret = market_data_combination(data, mark_ticker, start)
    log_ret = log_returns(dd)
    covar = log_ret.cov()*252
    covar = pd.DataFrame(covar.iloc[:-1,-1])
    mrk_var = log_ret.iloc[:,-1].var()*252
    beta = covar/mrk_var

    stdev_ret = pd.DataFrame(((log_ret.std()*250**0.5)[:-1]), columns=['STD'])
    beta = beta.merge(stdev_ret, left_index=True, right_index=True)

    # CAPM
    for i, row in beta.iterrows():
        beta.at[i,'CAPM'] = riskfree + (row[mark_ticker] * (mark_ret-riskfree))
    # Sharpe
    for i, row in beta.iterrows():
        beta.at[i,'Sharpe'] = ((row['CAPM']-riskfree)/(row['STD']))
    beta.rename(columns={"^GSPC":"Beta"}, inplace=True)

    return beta

def drift_calc(data, return_type='log'):
    if return_type=='log':
        lr = log_returns(data)
    elif return_type=='simple':
        lr = simple_returns(data)
    u = lr.mean()
    var = lr.var()
    drift = u-(0.5*var)
    try:
        return drift.values
    except:
        return drift

def daily_returns(data, days, iterations, return_type='log'):
    ft = drift_calc(data, return_type)
    if return_type == 'log':
        try:
            stv = log_returns(data).std().values
        except:
            stv = log_returns(data).std()
    elif return_type=='simple':
        try:
            stv = simple_returns(data).std().values
        except:
            stv = simple_returns(data).std()
            #Oftentimes, we find that the distribution of returns is a variation of the normal distribution where it has a fat tail
    # This distribution is called cauchy distribution
    dr = np.exp(ft + stv * norm.ppf(np.random.rand(days, iterations)))
    return dr

def probs_find(predicted, higherthan, ticker = None, on = 'value'):
    """
    This function calculated the probability of a stock being above a certain threshhold, which can be defined as a value (final stock price) or return rate (percentage change)
    Input:
    1. predicted: dataframe with all the predicted prices (days and simulations)
    2. higherthan: specified threshhold to which compute the probability (ex. 0 on return will compute the probability of at least breakeven)
    3. on: 'return' or 'value', the return of the stock or the final value of stock for every simulation over the time specified
    4. ticker: specific ticker to compute probability for
    """
    if ticker == None:
        if on == 'return':
            predicted0 = predicted.iloc[0,0]
            predicted = predicted.iloc[-1]
            predList = list(predicted)
            over = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 >= higherthan]
            less = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 < higherthan]
        elif on == 'value':
            predicted = predicted.iloc[-1]
            predList = list(predicted)
            over = [i for i in predList if i >= higherthan]
            less = [i for i in predList if i < higherthan]
        else:
            print("'on' must be either value or return")
    else:
        if on == 'return':
            predicted = predicted[predicted['ticker'] == ticker]
            predicted0 = predicted.iloc[0,0]
            predicted = predicted.iloc[-1]
            predList = list(predicted)
            over = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 >= higherthan]
            less = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 < higherthan]
        elif on == 'value':
            predicted = predicted.iloc[-1]
            predList = list(predicted)
            over = [i for i in predList if i >= higherthan]
            less = [i for i in predList if i < higherthan]
        else:
            print("'on' must be either value or return")
    return (len(over)/(len(over)+len(less)))


def simulate_mc(data, days, iterations,monteCarloReturn, return_type='log', plot=True):
    # Generate daily returns
    returns = daily_returns(data, days, iterations, return_type)
    # Create empty matrix
    price_list = np.zeros_like(returns)
    # Put the last actual price in the first row of matrix.
    price_list[0] = data.iloc[-1]
    # Calculate the price of each day
    for t in range(1,days):
        price_list[t] = price_list[t-1]*returns[t]

    #CAPM and Sharpe Ratio
    monteCarloReturn.days = days-1
    monteCarloReturn.expected_value = round(pd.DataFrame(price_list).iloc[-1].mean(),2)
    monteCarloReturn.returns = round(100*(pd.DataFrame(price_list).iloc[-1].mean()-price_list[0,1])/pd.DataFrame(price_list).iloc[-1].mean(),2)
    monteCarloReturn.prob_breakeven = probs_find(pd.DataFrame(price_list),0, on='return')
    # print(f"Days: {days-1}")
    # print(f"Expected Value: ${round(pd.DataFrame(price_list).iloc[-1].mean(),2)}")
    # print(f"Return: {round(100*(pd.DataFrame(price_list).iloc[-1].mean()-price_list[0,1])/pd.DataFrame(price_list).iloc[-1].mean(),2)}%")
    # print(f"Probability of Breakeven: {probs_find(pd.DataFrame(price_list),0, on='return')}")
    return pd.DataFrame(price_list)

async def monte_carlo(tickers, days_forecast, iterations,monteCarloReturn,  start_date = '2010-1-1', return_type = 'log', plotten=False):
    mc_list = []
    data = import_stock_data(tickers, start=start_date)
    inform = beta_sharpe(data, mark_ticker="^GSPC", start=start_date)
    for t in range(len(tickers)):
        y = simulate_mc(data.iloc[:,t], (days_forecast+1), iterations, monteCarloReturn, return_type)
        if plotten == True:
            forplot = y.iloc[:,0:10]
            forplot.plot(figsize=(15,4))
        monteCarloReturn.beta = round(inform.iloc[t,inform.columns.get_loc('Beta')],2)
        monteCarloReturn.sharpe = round(inform.iloc[t,inform.columns.get_loc('Sharpe')],2)
        monteCarloReturn.capm_return = round(100*inform.iloc[t,inform.columns.get_loc('CAPM')],2)
        mc_list.append(monteCarloReturn)
        monteCarloReturn = MonteCarloReturn()
        # print(f"Beta: {round(inform.iloc[t,inform.columns.get_loc('Beta')],2)}")
        # print(f"Sharpe: {round(inform.iloc[t,inform.columns.get_loc('Sharpe')],2)}")
        # print(f"CAPM Return: {round(100*inform.iloc[t,inform.columns.get_loc('CAPM')],2)}%")

    await asyncio.sleep(2)
    return mc_list
