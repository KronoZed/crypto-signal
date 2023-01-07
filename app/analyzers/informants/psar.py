""" Parabolic SAR
"""

import numpy as np
from scipy import stats
import talib
import pandas as pd
import pickle

from analyzers.utils import IndicatorUtils

"""
name: ahmet aksoy
date: 2023-01-02
psar: Parabolic Stop And Reverse
"""
class PSAR(IndicatorUtils):

    def analyze(self, historical_data, signal=['psar'], hot_thresh=0, cold_thresh=0):
        """Performs an analysis about the increase in volumen on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to ipsar. The indicator line to check hot against.

        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)

        psar_values = talib.SAR(dataframe.high.values, dataframe.low.values, acceleration=0.02, maximum=0.20)
        psar_values = pd.DataFrame({'psar': psar_values}, index=dataframe.index)
        psar_values.dropna(how='all', inplace=True)

        psar_values['psar']=psar_values['psar']/ dataframe.close

        return psar_values
