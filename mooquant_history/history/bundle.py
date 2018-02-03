# -*- coding: utf-8 -*-
import math
import os
import re
import time
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool

import requests
from pyquery import PyQuery
from user_agent import generate_user_agent

import pandas as pd
from . import store

try:
    from urllib.error import HTTPError
except Exception as e:
    from urllib2 import HTTPError


class Day:
    DOWN_DELAY = 0.5
    SINA_API = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/{symbol}.phtml'

    def __init__(self, path=None, export='csv', **kwargs):
        path = path if path else os.path.abspath(os.path.expanduser("~/.mooquant/bundle"))
        print('[-] Bundle Path: %s' % path)
        self.store = store.use(export=export, path=path, dtype='day')

    def initial(self, thread=2):
        symbols = self.store.initial_symbols

        pool = ThreadPool(thread)
        pool.map(self.initail_symbol, symbols)


    def bundle(self, symbol=None, initial=False, delay=0.5, **kwargs):
        self.DOWN_DELAY = delay

        if initial:
            self.initial(**kwargs)
        elif symbol:
            self.single(symbol, **kwargs)
        else:
            self.update(**kwargs)


    def update(self, thread=2, append=False):
        """ 更新已经下载的历史数据 """
        self.DOWN_DELAY = delay

        if append == True:
            symbols = self.store.append_symbols
        else:
            symbols = self.store.update_symbols

        pool = ThreadPool(thread)
        pool.map(self.single, symbols)


    def single(self, symbol, **kwargs):
        """ 更新对应的股票文件历史行情
        :param symbol: 股票代码
        :return:
        """
        latest_date = self.store.get_his_symbol_date(symbol)

        if not latest_date:
            return self.initail_symbol(symbol)

        updated_data = self.get_update_day_history(symbol, latest_date)

        if len(updated_data) == 0 or len(updated_data[0]) == 0:
            return

        self.store.write(symbol, updated_data)

    def get_update_day_history(self, symbol, latest_date):
        data_quarter = store.get_quarter(latest_date.month)
        data_year = latest_date.year
        now_year = datetime.now().year

        # 使用下一天的日期作为更新起始日，避免季度末时多更新上一季度的内容
        tomorrow = datetime.now() + timedelta(days=1)
        now_quarter = store.get_quarter(tomorrow.month)
        updated_data = list()

        for year in range(data_year, now_year + 1):
            for quarter in range(1, 5):
                if year == data_year:
                    if quarter < data_quarter:
                        continue

                if year == now_year:
                    if quarter > now_quarter:
                        continue
  
                updated_data += self.get_quarter_history(symbol, year, quarter)
        else:
            pass

        updated_data.sort(key=lambda day: day[0])

        return updated_data

    def initail_symbol(self, symbol):
        all_history = self.get_all_history(symbol)

        if len(all_history) <= 0:
            return

        self.store.write(symbol, all_history)

    def get_latest_history(self, symbol):
        years = self.get_symbol_time(symbol)
        all_history = []

        for year in years:
            year_history = self.get_year_history(symbol, year)
            all_history += year_history
        else:
            pass

        all_history.sort(key=lambda day: day[0])
        return all_history

    def get_all_history(self, symbol):
        years = self.get_symbol_time(symbol)
        all_history = []

        for year in years:
            year_history = self.get_year_history(symbol, year)
            all_history += year_history
        else:
            pass

        all_history.sort(key=lambda day: day[0])
        return all_history

    def get_year_history(self, symbol, year):
        year_history = []
        now_year = datetime.now().year
        now_month = datetime.now().month

        end_quarter = 5 if str(year) != str(now_year) else math.ceil(now_month / 3) + 1
        end_quarter = int(end_quarter)

        for quarter in range(1, end_quarter):
            quarter_data = self.get_quarter_history(symbol, year, quarter)

            if quarter_data is None:
                continue

            year_history += quarter_data
        else:
            pass

        return year_history

    def get_symbol_time(self, symbol):
        # 获取年月日
        url = self.SINA_API.format(symbol=symbol)

        try:
            dom = PyQuery(url)
        except requests.ConnectionError:
            print('requests.ConnectionError')
            print(url)
            time.sleep(60)
            return []
        except HTTPError as e:
            print('HTTPError', e.code)
            print(url)
            time.sleep(60)
            return []

        year_options = dom('select[name=year] option')
        years = [o.text for o in year_options][::-1]

        return years

    def get_quarter_history(self, symbol, year, quarter):
        year = int(year)

        if year < 1990:
            return list()

        params = dict(year=year, jidu=quarter)
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
            'User-Agent': generate_user_agent()
        }

        url = self.SINA_API.format(symbol=symbol)
        rep = None

        for _ in range(10):
            try:
                time.sleep(float(self.DOWN_DELAY))
                rep = requests.get(url, params, timeout=3, headers=headers)
                break
            except requests.ConnectionError:
                print('ConnectionError: sleep 60...')
                time.sleep(60)
            except Exception as e:
                raise e

        else:
            print('[*] {} => {}年{}季度. 失败'.format(symbol, year, quarter))
            return []

        print('[*] {} => {}年{}季度.'.format(symbol, year, quarter))

        if not rep:
            with open('errors.log', 'a+') as f:
                f.write('{},{},{}'.format(symbol, year, quarter))

            return []

        res = self.handle_quarter_history(rep.text)
        return res

    def handle_quarter_history(self, rep_html):
        dom = PyQuery(rep_html)
        raw_trows = dom('#FundHoldSharesTable tr')

        if len(raw_trows) <= 2:
            return list()

        trows = raw_trows[2:]
        res = list()

        for row_td_list in trows:
            td_list = row_td_list.getchildren()
            day_history = []

            for i, td in enumerate(td_list):
                td_content = td.text_content()
                date_index = 0

                if i == date_index:
                    td_content = re.sub(r'\r|\n|\t', '', td_content)

                day_history.append(td_content)
            else:
                pass

            self.convert_symbol_data_type(day_history)
            res.append(day_history)
        else:
            pass

        return res

    def convert_symbol_data_type(self, data):
        """将获取的对应日期股票数据除了日期之外，转换为正确的 float / int 类型
        :param data: ['2016-02-19', '945.019', '949.701', '940.336', '935.653', '31889824.000', '320939648.000', '93.659']
        :return: ['2016-02-19', 945.019, 949.701, 940.336, 935.653, 31889824.000, 320939648.000, 93.659]
        """
        for i, val in enumerate(data):
            if i == 0:
                continue
            data[i] = float(val)
        else:
            pass
