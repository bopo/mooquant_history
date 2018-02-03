# -*- coding: utf-8 -*-
from .bundle import Day


def init(dtype='day', export='csv', path=None):
    return Day(path=path, export=export).init()


def single(dtype='day', stock=None, path='history', export='csv'):
    if stock is None:
        raise Exception('stock code is None')

    return Day(path=path, export=export).single(stock)


def update(dtype='day', export='csv', path=None):
    return Day(path=path, export=export).update()


def initial(dtype='day', export='csv', path=None):
    return Day(path=path, export=export).initial()


def bundle(dtype='day', export='csv', path=None, **kwargs):
    return Day(dtype='day',path=path, export=export).bundle(**kwargs)
