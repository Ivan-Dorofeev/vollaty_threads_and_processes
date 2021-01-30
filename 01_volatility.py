# -*- coding: utf-8 -*-

import os
from csv import DictReader
from Class_2_volatility import TradeCalc

cur_dir = os.path.dirname(__file__)
path_in = os.path.join(cur_dir, 'trades')


class TradeReader:

    def __init__(self, vol_tiker):
        self.secid = None
        self.price_list = []
        self.volaty_tiker = vol_tiker

    def run(self, file_in):
        with open(file_in, mode='r', encoding='utf8') as ff:
            reader = DictReader(ff)
            for row in reader:
                self.secid = row['SECID']
                self.price_list.append(float(row['PRICE']))
        price_max = max(self.price_list)
        price_min = min(self.price_list)
        volaty = round((((price_max - price_min) / ((price_max + price_min) / 2)) * 100), 2)
        self.volaty_tiker[self.secid] = volaty


volaty_tiker = {}
for dirpath, dirnames, filenames in os.walk(path_in):
    for file in filenames:
        tr = TradeReader(vol_tiker=volaty_tiker)
        file_path = os.path.join(dirpath, file)
        tr.run(file_in=file_path)
#
tr_cacl = TradeCalc(volaty_dict=volaty_tiker)
tr_cacl.run()
