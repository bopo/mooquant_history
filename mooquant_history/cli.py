# -*- coding: utf-8 -*-

"""Console script for mooquant."""

import os
import sys
import shutil
import locale
import zipfile

import click
from tqdm import tqdm

from mooquant_history import history


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose


@cli.command(help='A股的历史数据下载(sina源).')
@click.option('-d', '--directory', default=os.path.expanduser("~/.mooquant/bundle"), type=click.Path(file_okay=False), help='历史数据下载目录, 默认 ~/.mooquant/bundle.')
@click.option('-i', '--initial', is_flag=True, help='初始化历史, 第一次下载使用该参数, 默认 False.')
@click.option('-s', '--symbol', default=None, help='更新单个股票的代码, 默认为空.')
@click.option('-a', '--append', is_flag=True, help='更新股票的代码 增项增量模式.')
@click.option('-t', '--thread', default='2', help='同时请求线程数, 默认2,建议不要超过5个, 会被封IP.')
@click.option('--delay', default='0.5', help='默认每次请求后等待时间')
def bundle(directory, initial, symbol, append, delay, thread):
    history.bundle(dtype='day', export='csv', **locals()) 

@cli.command(help='更新股票代码.')
@click.option('-d', '--directory', default=os.path.expanduser("~/.mooquant/bundle"), type=click.Path(file_okay=False), help='历史数据下载目录.')
def symbol(directory):
    from mooquant_history.helpers.symbol import update_stock_codes
    update_stock_codes()

@cli.command(help='实时行情(支持sina, qq, ).')
@click.option('-s', '--symbol', default=None, help='单个股票的代码行情.')
def quotes(symbol):
    click.echo('运行实时行情')


@cli.command(help='导出 bundle.')
@click.option('-d', '--directory', default=os.path.expanduser("~/.mooquant/bundle"), type=click.Path(file_okay=False), help='历史数据下载目录.')
@click.option('-o', '--output', default=os.path.expanduser("./bundle"), type=click.Path(file_okay=False), help='导出文件目录, 默认当前目录.')
def export(directory, output):
    data_path = os.path.join(directory, 'day', 'raw_data')
    file_name = os.path.join(output,'bundle.zip')
    file_list = [f for f in os.listdir(data_path) if f.endswith('.csv')]

    click.echo('Starting...')
    z = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)

    if file_list: 
        for f in tqdm(file_list):
            z.write(os.path.join(data_path, f), f) 

    z.close()
    click.echo('done.')


@cli.command(help='转换为 MooQaunt 格式.')
@click.option('-s', '--strategy', default='', help='运行回测规则路径.')
def covert(strategy):
    click.echo('运行回测规则')

def main():
    cli(obj={})


if __name__ == '__main__':
    main()
