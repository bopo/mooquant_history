# -*- coding: utf-8 -*-
import json
import math
import os
from datetime import datetime
import pandas as pd
from ..helpers import get_stock_codes


def get_quarter(month):
    return math.ceil(int(month) / 3)


def use(export='csv', **kwargs):
    if export.lower() in ['csv']:
        return CSVStore(**kwargs)

class Store:
    def load(self, symbol_data):
        pass

    def write(self, symbol_code, updated_data, **kwargs):
        pass


class CSVStore(Store):
    def __init__(self, path, dtype, **kwargs):
        self.bundle_path = path

        if dtype.lower() in ['day']:
            self.path = os.path.join(path, 'day')

        # self.result_path = os.path.join(self.path, 'data')
        self.raw_path = os.path.join(self.path, 'raw_data')

    def write(self, symbol_code, updated_data, **kwargs):
        # if not os.path.exists(self.result_path):
        #     os.makedirs(self.result_path)

        if not os.path.exists(self.raw_path):
            os.makedirs(self.raw_path)

        csv_file_path = os.path.join(self.raw_path, '{}.csv'.format(symbol_code))

        if os.path.exists(csv_file_path):
            try:
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return

            updated_data_start_date = updated_data[0][0]
            old_his = his[his.date < updated_data_start_date]
            updated_his = pd.DataFrame(updated_data, columns=his.columns)
            his = old_his.append(updated_his)
        else:
            his = pd.DataFrame(updated_data, columns=['date', 'open', 'high', 'close', 'low', 'volume', 'amount', 'factor'])

        his.to_csv(csv_file_path, index=False)
        date = his.iloc[-1].date

        self.__write_summary(symbol_code, date)
        # self.__write_factor_his(symbol_code, his)

    def get_his_symbol_date(self, symbol_code, **kwargs):
        summary_path = os.path.join(self.raw_path, '{}_summary.json'.format(symbol_code))

        if not os.path.exists(summary_path):
            return None
        
        try:
            with open(summary_path) as f:
                summary = json.load(f)

            latest_date = datetime.strptime(summary['date'], '%Y-%m-%d')

            return latest_date
        except json.decoder.JSONDecodeError:
            return None


    def __write_summary(self, symbol_code, date, **kwargs):
        file_path = os.path.join(self.raw_path, '{}_summary.json'.format(symbol_code))

        with open(file_path, 'w') as f:
            latest_day = datetime.strptime(date, '%Y-%m-%d')
            summary = dict(
                year=latest_day.year,
                month=latest_day.month,
                day=latest_day.day,
                date=date
            )

            json.dump(summary, f)


    @property
    def update_symbols(self):
        code_slice = slice(6)
        return [f[code_slice] for f in os.listdir(self.raw_path) if f.endswith('.json')]

    @property
    def append_symbols(self):
        symbol_codes = self.get_all_symbols()
        exists_codes = set()

        if os.path.exists(self.raw_path):
            exists_codes = {code[slice(-4)] for code in os.listdir(self.raw_path) if code.endswith('.csv')}

        return set(symbol_codes).difference(exists_codes)

    @property
    def initial_symbols(self):
        symbol_codes = self.get_all_symbols(realtime=True)

        return set(symbol_codes)

    def get_all_symbols(self, realtime=False, **kwargs):
        symbol_path = os.path.join(self.bundle_path, 'symbols.json')
        symbol_code = get_stock_codes(symbol_path=symbol_path, realtime=realtime)

        return symbol_code
