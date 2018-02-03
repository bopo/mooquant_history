# -*- coding: utf-8 -*-
import json
import os

import pandas as pd

from tqdm import tqdm
import talib
from .. import formula

class Indicator(object):
    def __init__(self, symbol, history, **kwargs):
        self.history = history
        self.symbol = symbol
        self.hisarg = {}

    def __getattr__(self, item):
        def formula_func(*args, **kwargs):
            str_args = ''.join(map(str, args))
            index = item + str_args

            if index in self.hisarg and self.hisarg[index] is not None:
                return self.hisarg[index]

            try:
                fun = getattr(talib, item)
                res = fun(self.history['close'].values, *args, **kwargs)
            except Exception as e:
                fun = getattr(formula, item)
                res = fun(self.history, *args, **kwargs)
            else:
                pass
            finally:
                pass

            self.hisarg[index] = res
            return self.hisarg[index]
        
        return formula_func



class History(object):
    def __init__(self, dtype='day', path=None, symbol=None, export='csv', **kwargs):
        path = path if path else os.path.abspath(os.path.expanduser("~/.mooquant/bundle"))

        print('[*] Bundle Path: %s' % path)
        print('[+] Bundle loading...')

        data_path = os.path.join(path, dtype, 'raw_data')

        self.market = dict()
        self.__load_csv_files(data_path, symbol, **kwargs)

        print('[x] Done')

    def __load_csv_files(self, path=None, symbol=None, export='csv', **kwargs):
        export = '.' + export.strip('.')
        
        if symbol and os.path.exists(os.path.join(path, symbol + export)):
            file_list = [symbol + export]
        else:
            file_list = [f for f in os.listdir(path) if f.endswith(export)]
            file_list = tqdm(file_list)

        for symbol_csv in file_list:
            symbol = symbol_csv[:-4]
            csv_path = os.path.join(path, symbol_csv)
            self.market[symbol] = Indicator(symbol, pd.read_csv(csv_path, index_col='Date Time', **kwargs))


    def __getitem__(self, item):
        return self.market[item]
