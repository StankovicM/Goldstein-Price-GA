import numpy as np
import json, random, sys

konf = None

min_xy      = -2.0
max_xy      = 2.0
min_x       = 0.0
min_y       = -1.0
min_f       = 3.0
evolucija   = 500
populacija  = 20
iteracija   = 1
mutacija    = 0.1


def goldstajn_prajs(x, y):
    a = x + y + 1
    b = 19 - 14*x + 3*x*x - 14*y + 6*x*y +3*y*y
    c = 2*x - 3*y
    d = 18 - 32*x + 12*x*x + 48*y - 36*x*y + 27*y*y

    res = (1 + a*a*b)*(30 + c*c*d)
    return res


def float_to_bin(x):
    x_string = ''

    if x < 0:
        x_string = '1'
    else:
        x_string = '0'

    x_int = int(abs(int(x)))
    x_dec = int(round(abs(x) - x_int, 3) * 1000)

    if x_int == 0:
        x_string += '00'
    elif x_int == 1:
        x_string += '01'
    elif x_int == 2:
        x_string += '10'
    else:
        print('GRESKA!!! {}'.format(x))

    x_string += '{:010b}'.format(x_dec)

    return x_string


def bin_to_float(s):
    x = 0

    x_int = int(s[1:3], 2)
    x_dec = int(s[3:], 2)

    x = x_int + x_dec / 1000

    if s[0] == '1':
        x *= -1

    return x


class Hromozom():

    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = round(random.uniform(min_xy, max_xy), 3)
            self.y = round(random.uniform(min_xy, max_xy), 3)
        else:
            self.x = x
            self.y = y

        self.trosak =  self.izracunaj_trosak()

    def izracunaj_trosak(self):
        f_val = goldstajn_prajs(self.x, self.y)
        self.trosak = abs(min_f - f_val)
        return self.trosak

    def ukrsti(self, h):
        l1 = list(float_to_bin(self.x) + float_to_bin(self.y))
        l2 = list(float_to_bin(h.x) + float_to_bin(h.y))
        i = random.randint(0, len(l1))
        j = 0
        while True:
            j = random.randint(0, len(l1))
            if j != i:
                break

        if j < i: 
            tmp = i
            i = j
            j = tmp

        l1[i:j], l2[i:j] = l2[i:j], l1[i:j] 

        s1 = ''.join(l1)
        x1 = bin_to_float(s1[0:13])
        y1 = bin_to_float(s1[13:])
        if x1 < -2 or x1 > 2:
            l1[1] = '0'
            l1[2] = random.choice(('0', '1'))
            s1 = ''.join(l1)
            x1 = bin_to_float(s1[0:13])

        if y1 < -2 or y1 > 2:
            l1[14] = '0'
            l1[15] = random.choice(('0', '1'))
            s1 = ''.join(l1)
            y1 = bin_to_float(s1[13:])

        s2 = ''.join(l2)
        x2 = bin_to_float(s2[0:13])
        y2 = bin_to_float(s2[13:])
        if x2 < -2 or x2 > 2:
            l2[1] = '0'
            l2[2] = random.choice(('0', '1'))
            s2 = ''.join(l2)
            x2 = bin_to_float(s2[0:13])

        if y2 < -2 or y2 > 2:
            l2[14] = '0'
            l2[15] = random.choice(('0', '1'))
            s2 = ''.join(l2)
            y2 = bin_to_float(s2[13:])

        return Hromozom(x=x1, y=y1), Hromozom(x=x2, y=y2)

    def mutiraj(self):
        l = list(float_to_bin(self.x) + float_to_bin(self.y))
        i = random.randint(0, len(l) - 1)
        l[i] = l[i] = '0' if l[i] == '1' else '1'
        s = ''.join(l)
        x = bin_to_float(s[0:13])
        y = bin_to_float(s[13:])

        if x < -2 or x > 2:
            l[1] = '0'
            l[2] = random.choice(('0', '1'))
            s = ''.join(l)
            x = bin_to_float(s[0:13])

        if y < -2 or y > 2:
            l[14] = '0'
            l[15] = random.choice(('0', '1'))
            s = ''.join(l)
            y = bin_to_float(s[13:])

        self.x = x
        self.y = y

    def __repr__(self):
        return f'[{self.x}, {self.y}] - {self.trosak}'


class Populacija():

    def __init__(self, velicina):
        self.hromozomi = []
        self.najbolji = []
        self.prosecni = []
        self.velicina = velicina
    
        for i in range(velicina):
            self.hromozomi.append(Hromozom())

        self.minimum = self.hromozomi[0].trosak
        self.min_x = self.hromozomi[0].x
        self.min_y = self.hromozomi[0].y

    def sortiraj(self):
        self.hromozomi.sort(key=lambda h: h.trosak)

    def prepolovi(self):
        self.hromozomi = self.hromozomi[0:int(self.velicina / 2)]

    def izracunaj(self):
        suma_troskova = 0
        tren_min = self.hromozomi[0].trosak
        tren_x = self.hromozomi[0].x
        tren_y = self.hromozomi[0].y

        for h in self.hromozomi:
            t = h.izracunaj_trosak()
            suma_troskova += t

            if t < tren_min:
                tren_min = t
                tren_x = h.x
                tren_y = h.y

        prosek = suma_troskova / self.velicina

        if tren_min < self.minimum:
            self.minimum = tren_min
            self.min_x = tren_x
            self.min_y = tren_y

        self.najbolji.append(tren_min)
        self.prosecni.append(prosek)

    def ukrstanje(self):
        for i in range(int(self.velicina / 4)):
            x = random.choice(self.hromozomi)
            y = random.choice(self.hromozomi)

            novi = x.ukrsti(y)

            if random.uniform(0, 1) < mutacija:
                novi[0].mutiraj()

            if random.uniform(0, 1) < mutacija:
                novi[1].mutiraj()

            self.hromozomi.append(novi[0])
            self.hromozomi.append(novi[1])


def init():
    global konf, min_xy, max_xy, min_x, min_y, min_f, evolucija, populacija, iteracija

    with open('konf.json', 'r') as f:
        konf = json.load(f)

    min_xy = konf['min_xy']
    max_xy = konf['max_xy']
    min_x = konf['min_x']
    min_y = konf['min_y']
    min_f = konf['min_f']
    evolucija = konf['evolucija']
    populacija = konf['populacija']
    iteracija = konf['iteracija']


def bga():

     for i in range(iteracija):
        print(f'Pocinje iteracija {i}. Generisem novu populaciju.')
        p = Populacija(populacija)

        for j in range(evolucija):
            p.sortiraj()
            p.prepolovi()
            p.ukrstanje()
            p.izracunaj()
            if j % 50 == 0:
                print(f'{[j]}: Min trosak: {p.najbolji[j]}, Avg trosak: {p.prosecni[j]}')
            
        h = float_to_bin(p.min_x) + float_to_bin(p.min_y)
        print(f'Min trosak: {p.minimum}, X: {p.min_x}, Y: {p.min_y}, F: {goldstajn_prajs(p.min_x, p.min_y)}, Hromozom: {h}')

if __name__ == '__main__':
    init()
    bga()