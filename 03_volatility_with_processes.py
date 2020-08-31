# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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

from multiprocessing import Process, Queue
import queue
import os
from csv import DictReader
from Class_2_volatility import TradeCalc

cur_dir = os.path.dirname(__file__)
path_in = os.path.join(cur_dir, 'trades')


class TradeReader(Process):

    def __init__(self, file_in, vol_tiker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_in = file_in
        self.secid = None
        self.price_list = []
        self.volaty_tiker = vol_tiker

    def run(self):
        with open(self.file_in, mode='r', encoding='utf8') as ff:
            reader = DictReader(ff)
            for row in reader:
                self.secid = row['SECID']
                self.price_list.append(float(row['PRICE']))
        price_max = max(self.price_list)
        price_min = min(self.price_list)
        volaty = round((((price_max - price_min) / ((price_max + price_min) / 2)) * 100), 2)
        self.volaty_tiker.put((self.secid, volaty))


volaty_tiker = Queue(maxsize=2)
tr_list = []
if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk(path_in):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            tr = TradeReader(file_in=file_path, vol_tiker=volaty_tiker)
            tr_list.append(tr)

    for tr_numbers_start in tr_list:
        tr_numbers_start.start()

    volaty_tiker_dict = {}
    while True:
        try:
            res = volaty_tiker.get(timeout=1)
            volaty_tiker_dict[res[0]] = res[1]
        except queue.Empty:
            if not any(tr_numbers_start.is_alive() for tr_numbers_start in tr_list):
                break

    for tr_numbers_end in tr_list:
        tr_numbers_end.join()

    tr_cacl = TradeCalc(volaty_dict=volaty_tiker_dict)
    tr_cacl.run()
