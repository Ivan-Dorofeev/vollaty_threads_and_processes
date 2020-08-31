# -*- coding: utf-8 -*-

class TradeCalc:

    def __init__(self, volaty_dict):
        self.volaty_dict = volaty_dict
        self.max_volaty = None
        self.min_volaty = None
        self.zero_volaty = []

    def run(self):
        self.max_volaty = sorted(self.volaty_dict.items(), key=lambda y: y[1], reverse=True)
        self.min_volaty = sorted(self.volaty_dict.items(), key=lambda x: x[1], )
        self.max_volaty = dict(self.max_volaty)
        self.min_volaty = dict(self.min_volaty)
        for key, value in self.volaty_dict.items():
            if value == 0:
                self.min_volaty.pop(key)
                self.zero_volaty.append(key)
        count = 0
        print("Максимальная волатильность:")
        for key, value in self.max_volaty.items():
            count += 1
            if count > 3:
                break
            print(f'ТИКЕР {key} : {value}')
        count = 0
        print("Минимальная волатильность:")
        for key, value in self.min_volaty.items():
            count += 1
            if count > 3:
                break
            print(f'ТИКЕР {key} : {value}')
        print("Нулевая волатильность:")
        print(f'ТИКЕР: {",".join(self.zero_volaty)}')
