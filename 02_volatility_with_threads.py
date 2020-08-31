# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.


import os
import threading
from csv import DictReader
from threading import Thread

from Class_2_volatility import TradeCalc

cur_dir = os.path.dirname(__file__)
path_in = os.path.join(cur_dir, 'trades')


class TradeReader(Thread):

    def __init__(self, file_in, vol_tiker, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_in = file_in
        self.secid = None
        self.price_list = []
        self.volaty_tiker = vol_tiker
        self.lock = lock

    def run(self):
        with open(self.file_in, mode='r', encoding='utf8') as ff:
            reader = DictReader(ff)
            for row in reader:
                self.secid = row['SECID']
                self.price_list.append(float(row['PRICE']))
        price_max = max(self.price_list)
        price_min = min(self.price_list)
        volaty = round((((price_max - price_min) / ((price_max + price_min) / 2)) * 100), 2)
        with self.lock:
            self.volaty_tiker[self.secid] = volaty


lock = threading.Lock()
volaty_tiker = {}
tr_list = []
for dirpath, dirnames, filenames in os.walk(path_in):
    for file in filenames:
        file_path = os.path.join(dirpath, file)
        tr = TradeReader(file_in=file_path, vol_tiker=volaty_tiker, lock=lock)
        tr_list.append(tr)

for tr_numbers_start in tr_list:
    tr_numbers_start.start()
for tr_numbers_end in tr_list:
    tr_numbers_end.join()

tr_cacl = TradeCalc(volaty_dict=volaty_tiker)
tr_cacl.run()


