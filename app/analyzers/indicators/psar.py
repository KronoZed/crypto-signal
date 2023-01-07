""" Parabolic SAR (Stop And Reverse)
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
            signal (list, optional): Defaults to psar. The indicator line to check hot against.

        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """


        dataframe = self.convert_to_dataframe(historical_data)

        psar_values = talib.SAR(dataframe.high.values, dataframe.low.values, acceleration=0.02, maximum=0.20)
        psar_values = pd.DataFrame({'psar': psar_values}, index=dataframe.index)
        psar_values.dropna(how='all', inplace=True)


        try:
            psar_values['close']=dataframe.close
            if psar_values[signal[0]].shape[0]:
                psar_values['is_hot'] = psar_values[signal[0]] < psar_values['close']
                psar_values['is_cold'] = psar_values[signal[0]] > psar_values['close']
        except:
            pass

        return psar_values
