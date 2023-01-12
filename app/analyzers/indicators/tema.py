""" Triple Exponential Moving Average
"""

import numpy as np
from scipy import stats
import pandas as pd
import numpy as np

from analyzers.utils import IndicatorUtils

"""
name: ahmet aksoy
date: 2023-01-08
tema: Triple EMA
"""
class TEMA(IndicatorUtils):
    def analyze(self, historical_data, signal=['tema'], short_period=8, middle_period=13, long_period=21, hot_thresh=0,cold_thresh=0):
        """Calculates short, middle and long EMA values and the intersections between them

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to tema. 
            short_period: short period to calculate EMA
            middle_period: middle period to calculate EMA
            long_period: long period to calculate EMA

        Returns:
            pandas.DataFrame: A dataframe containing the indicator values.
        """

        df = self.convert_to_dataframe(historical_data)
        shortEMA = df.close.ewm(span=short_period, adjust=False).mean() #Fast moving average
        middleEMA = df.close.ewm(span=middle_period, adjust=False).mean() #Middle moving average
        longEMA = df.close.ewm(span=long_period, adjust=False).mean() #Slow moving average

        df['short'] = shortEMA
        df['middle'] = middleEMA
        df['long'] = longEMA        

        def buy_or_sell(data):
            buy_list = []
            sell_list = []
            flag_long = False
            flag_short = False

            for i in range(0,len(data)):
                try:
                    if data['middle'][i] < data['long'][i] and data['middle'][i] > data['short'][i] and flag_long == False and flag_short == False:
                        buy_list.append(data['close'][i])
                        sell_list.append(np.nan)
                        flag_short = True
                    elif data['middle'][i] > data['long'][i] and data['middle'][i] < data['short'][i] and flag_short == False and flag_long == False:
                        buy_list.append(data['close'][i])
                        sell_list.append(np.nan)
                        flag_long = True
                    elif flag_short == True and data['short'][i] > data['middle'][i]:
                        sell_list.append(data['close'][i])
                        buy_list.append(np.nan)
                        flag_short = False
                    elif flag_long == True and data['short'][i] < data['middle'][i]:
                        sell_list.append(data['close'][i])
                        buy_list.append(np.nan)
                        flag_long = False
                    else:
                        buy_list.append(np.nan)
                        sell_list.append(np.nan)
                except:
                    pass

            return (buy_list, sell_list)

        #Add the buy and sell signals to the data set
        df['buy'] = buy_or_sell(df)[0]
        df['sell'] = buy_or_sell(df)[1]
        df['is_hot'] = False
        df['is_cold'] = False
        df['is_hot'] = df['buy']>0
        df['is_cold'] = df['sell']>0

        return df
