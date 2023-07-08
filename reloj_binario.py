from datetime import datetime as dttm
import tkinter as tk
from threading import Thread


class TiempoBin:
    def datos(self):
        t = dttm.now().time()
        h = f"{t.hour:02d}"
        m = f"{t.minute:02d}"
        s = f"{t.second:02d}"
        dc = {
            'horas':h, 'minutos':m, 'segundos':s,
            'hb':self.digitos_bin(h),
            'mb':self.digitos_bin(m),
            'sb':self.digitos_bin(s)
        }
        return dc

    def digitos_bin(self, numeros):
        return [f"{int(num):04b}" for num in numeros]
    

class Interfaz(tk.Tk):
    def __init__(self):
        super(Interfaz, self).__init__()
        self.geometry('200x140')
        self.cnv = tk.Canvas(bg='#09100C')
        self.cnv.pack(expand=1, fill='both')
        self.valores()
        self.grafica()

    def valores(self):
        self.cf = {
            'pto': (30, 110, 45, 125),
            'vars_h': [
                ['h11','h12','h14','h18'],
                ['h21','h22','h24','h28']
            ],
            'vars_m': [
                ['m11','m12','m14','m18'],
                ['m21','m22','m24','m28']
            ],
            'vars_s': [
                ['s11','s12','s14','s18'],
                ['s21','s22','s24','s28']
            ],
            'txtn':[1,2,4,8],
            'tms':[
                'hor2', 'hor1', 'min2', 'min1', 'seg2', 'seg1'
            ]
        }
    
    def crea_ovalo(self, distx, y=0):
        fy = (y*20)
        pto = self.cf.get('pto')
        return self.cnv.create_oval(
            pto[0]+distx, pto[1]-fy, pto[2]+distx, pto[3]-fy,
            fill='gray30', outline='gray10'
        )

    def crea_nums(self, distx, disty=0):
        pto = self.cf.get('pto')
        return self.cnv.create_text(
            pto[0]+8+distx, pto[1]-disty, fill='gray40',
            font=('Bahnschrift SemiBold SemiConden', 28, 'bold'), text='0'
        )
    
    def grafica(self):
        vars_h = self.cf.get('vars_h')
        vars_m = self.cf.get('vars_m')
        vars_s = self.cf.get('vars_s')
        for x in range(2):
            dist = 25*x
            for y in range(4):
                vars_h[x][y] = self.crea_ovalo(dist, y)
                vars_m[x][y] = self.crea_ovalo(dist+60, y)
                vars_s[x][y] = self.crea_ovalo(dist+120, y)

        tms = self.cf.get('tms')
        for x in range(0, len(tms), 2):
            dx = x*30
            tms[x] = self.crea_nums(dx, 85)
            tms[x+1] = self.crea_nums(dx+25, 85)

        pto = self.cf.get('pto')
        for x in range(4):
            self.cnv.create_text(
                pto[0]-10, pto[1]-(x*20)+8, fill='gray60',
                font=('Arial', 8, 'bold'),
                text=self.cf.get('txtn')[x]
            )


class RelojBin(Interfaz):
    def __init__(self):
        super(RelojBin, self).__init__()
        self.tbin = TiempoBin()

    def _movimiento(self, valor_bin, variables, tipo, indice):
        d = self.tbin.datos()
        tiempo_bin = d.get(valor_bin)
        for x, numeros in enumerate(tiempo_bin):
            for y, num in enumerate(numeros[::-1]):
                bg = 'red' if num=='1' else 'gray30'
                self.cnv.itemconfig(variables[x][y], fill=bg)

        tms = self.cf.get('tms')
        digitos = d.get(tipo)
        self.cnv.itemconfig(tms[indice], text=digitos[1])
        self.cnv.itemconfig(tms[indice-1], text=digitos[0])

    def _segundero(self):
        self._movimiento('sb',  self.cf.get('vars_s'), 'segundos', 5)
        self.cnv.after(1000, self._segundero)
        d = self.tbin.datos()
        if d.get('segundos')=='00':
            self._minutero()
        if d.get('minutos')=='00':
            self._horero()

    def _minutero(self):
        self._movimiento('mb', self.cf.get('vars_m'), 'minutos', 3)

    def _horero(self):
        self._movimiento('hb', self.cf.get('vars_h'), 'horas', 1)

    def inicia_contador(self):
        Thread(target=self._segundero()).start()
        Thread(target=self._minutero()).start()
        Thread(target=self._horero()).start()


rbin = RelojBin()
rbin.inicia_contador()
rbin.mainloop()