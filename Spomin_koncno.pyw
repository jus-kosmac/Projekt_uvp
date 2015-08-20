from tkinter import *
import random
import time
import os
import subprocess
from tkinter import messagebox

class Spomin():
    def __init__(self, master):
        self.zacetno_okno = Frame(master)
        self.zacetno_okno.pack()
        master.title('Velikost spomina')
        Label(self.zacetno_okno, text='Izberi velikost spomina :', font=10).grid(row=0, column=0, columnspan=6)
        gumb1 = Button(self.zacetno_okno, text='3 x 4', command=self.klikni1)
        gumb1.grid(row=1, column=0)
        gumb2 = Button(self.zacetno_okno, text='4 x 4', command=self.klikni2)
        gumb2.grid(row=1, column=2)
        gumb3 = Button(self.zacetno_okno, text='4 x 5', command=self.klikni3)
        gumb3.grid(row=1, column=4)
        gumb4 = Button(self.zacetno_okno, text='2 x 2', command=self.klikni4)
        gumb4.grid(row=1, column=6)
        self.master = master

    def klikni1(self):
        self.zacni_spomin(3, 4)

    def klikni2(self):
        self.zacni_spomin(4, 4)

    def klikni3(self):
        self.zacni_spomin(4, 5)

    def klikni4(self):
        self.zacni_spomin(2, 2)

              
    def zacni_spomin(self, i, j):
        self.master.title('Spomin')
        self.zacetno_okno.destroy()
        master = Frame(self.master)
        master.pack()

        menu = Menu(self.master)
        self.master.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label="Možnosti", menu=file_menu)
        file_menu.add_command(label="Poglej rezultate", command=self.poglej)
        file_menu.add_command(label="Najboljši rezultati", command=self.hiscores)
        file_menu.add_command(label="Izhod", command=self.master.destroy)

        self.cas = time.time()
        self.najdeni = 0
        self.count = 0
        
        self.i = i
        self.j = j
        self.gumbi = []
        self.polja = []
        self.moznosti = []
        for a in range((self.i * self.j) // 2):
            self.moznosti.append(a)
            self.moznosti.append(a)
        random.shuffle(self.moznosti)
        self.vrednosti = []
        for i in range(self.i):
            temp = []
            for j in range(self.j):
                temp.append(self.moznosti.pop())
            self.vrednosti.append(temp)
        
        self.dict = {0: 'blue', 1: 'green', 2: 'yellow', 3: 'red', 4: 'orange', 5: 'white', 6: 'brown', 7: 'cyan', 8: 'magenta', 9: 'grey'}

        for i in range(self.i):
            temp = []
            for j in range(self.j):
                polje = Canvas(master, width=100, height=100, bg='black')
                polje.grid(row=2*i+1, column=j)
                temp.append(polje)
            self.polja.append(temp)
            
        for i in range(self.i):
            temp = []
            for j in range(self.j):
                gumb = Button(master, text='Odpri polje : ({0} , {1})'.format(i, j), command=self.odpri(i, j))
                gumb.grid(row=2*i, column=j)
                temp.append(gumb)
            self.gumbi.append(temp)

        self.prvo = None
        self.drugo = None
       
    def odpri(self, i, j):
        def o():
            if self.prvo != None and self.drugo != None:
                (a, b) = self.prvo
                (c, d) = self.drugo
                if self.vrednosti[a][b] != self.vrednosti[c][d]:
                    self.polja[a][b].create_rectangle(0, 0, 100, 100, fill='black')
                    self.polja[c][d].create_rectangle(0, 0, 100, 100, fill='black')
                self.prvo = None
                self.drugo = None
            if self.prvo == None:
                self.prvo = (i, j)
                self.polja[i][j].create_rectangle(0, 0, 100, 100, fill=self.dict[self.vrednosti[i][j]])
            else:
                if (i, j) != self.prvo:
                    self.drugo = (i, j)
                    self.polja[i][j].create_rectangle(0, 0, 100, 100, fill=self.dict[self.vrednosti[i][j]])
                    self.count += 1
            if self.prvo != None and self.drugo != None:
                (a, b) = self.prvo
                (c, d) = self.drugo
                if self.vrednosti[a][b] == self.vrednosti[c][d]:
                    self.najdeni += 1
                    self.gumbi[c][d].configure(state=DISABLED)
                    self.gumbi[a][b].configure(state=DISABLED)
            if self.najdeni == (self.i * self.j) // 2:
                self.sekunde = time.time() - self.cas
                self.rezultat(self.master, self.sekunde, self.count)
        return o

    def rezultat(self, master, sekunde, poteze):
        self.ime = StringVar(master)
        self.ime.set('Vpiši svoje ime.')
        if self.count == 2:
            self.popravek = 'i'
        elif self.count == 3 or self.count == 4:
            self.popravek = 'e'
        else:
            self.popravek = ''
        Label(master, text='Vaš rezultat : {0:.2f} sekund in {1} potez{2}'.format(sekunde, poteze, self.popravek), font=8).pack()
        vpis = Entry(master, textvariable=self.ime)
        vpis.pack()
        self.shranjevalec = Button(master,  text='Shrani rezultat', command=self.shrani)
        self.shranjevalec.pack()

    def shrani(self):
        if self.ime.get() == 'Vpiši svoje ime.':
            messagebox.showerror(title='Napaka', message='Vpišite svoje ime.')
        else:
            self.shranjevalec.configure(state=DISABLED, text='Shranjeno')
            if os.path.exists(os.getcwd() + '\Rezultati.txt'):
                with open(os.getcwd() + '\Rezultati.txt', 'a') as f:
                    print('{0} je porabil/a {1:.2f} sekund in {2} potez{5} za reševanje {3} x {4} spomina.'.format(self.ime.get(), self.sekunde, self.count, self.i, self.j, self.popravek), file=f)
            else:
                with open(os.getcwd() + '\Rezultati.txt', 'w') as f:
                    print('{0} je porabil/a {1:.2f} sekund in {2} potez{5} za reševanje {3} x {4} spomina.'.format(self.ime.get(), self.sekunde, self.count, self.i, self.j, self.popravek), file=f)

    def poglej(self):
        if os.path.exists(os.getcwd() + '\Rezultati.txt'):
            subprocess.call('Notepad.exe ' + os.getcwd() + '\Rezultati.txt')
        else:
            messagebox.showerror(title='Napaka', message='Niste še odigrali nobene igre.')

    def hiscores(self):
        if os.path.exists(os.getcwd() + '\Rezultati.txt'):
            with open(os.getcwd() + '\Rezultati.txt') as f:
                seznam1 = [] #2x2
                seznam2 = [] #3x4
                seznam3 = [] #4x4
                seznam4 = [] #4x5
                for line in f:
                    temp = []
                    line.strip()
                    x = line.split(' ')
                    a = x.index('porabil/a') - 1
                    temp.append(x[-11])
                    temp.append(x[-8])
                    temp.append(' '.join(x[:a]))
                    temp.append(x[-4])
                    temp.append(x[-2])
                    if temp[3] == '2':
                        seznam1.append(temp[:3])
                    elif temp[3] == '3':
                        seznam2.append(temp[:3])
                    elif temp[4] == '5':
                        seznam4.append(temp[:3])
                    else:
                        seznam3.append(temp[:3])

            Label(self.master, text='Najboljši rezultati', font=8).pack()
            
            if seznam1 != []:
                p1 = min([int(x[1]) for x in seznam1])
                for x in seznam1:
                    if int(x[1]) == p1:
                        ime11 = x[2]
                        break
                s1 = min([float(x[0]) for x in seznam1])
                for x in seznam1:
                    if float(x[0]) == s1:
                        ime21 = x[2]
                        break
                Label(self.master, text='2 x 2 : najmanj potez - {2}, {0}   najhitrejši čas - {3}, {1} sekund'.format(p1, s1, ime11, ime21)).pack()

            if seznam2 != []:
                p2 = min([int(x[1]) for x in seznam2])
                for x in seznam2:
                    if int(x[1]) == p2:
                        ime12 = x[2]
                        break
                s2 = min([float(x[0]) for x in seznam2])
                for x in seznam2:
                    if float(x[0]) == s2:
                        ime22 = x[2]
                        break
                Label(self.master, text='3 x 4 : najmanj potez - {2}, {0}   najhitrejši čas - {3}, {1} sekund'.format(p2, s2, ime12, ime22)).pack()

            if seznam3 != []:
                p3 = min([int(x[1]) for x in seznam3])
                for x in seznam3:
                    if int(x[1]) == p3:
                        ime13 = x[2]
                        break
                s3 = min([float(x[0]) for x in seznam3])
                for x in seznam3:
                    if float(x[0]) == s3:
                        ime23 = x[2]
                        break
                Label(self.master, text='4 x 4 : najmanj potez - {2}, {0}   najhitrejši čas - {3}, {1} sekund'.format(p3, s3, ime13, ime23)).pack()

            if seznam4 != []:
                p4 = min([int(x[1]) for x in seznam4])
                for x in seznam4:
                    if int(x[1]) == p4:
                        ime14 = x[2]
                        break
                s4 = min([float(x[0]) for x in seznam4])
                for x in seznam4:
                    if float(x[0]) == s4:
                        ime24 = x[2]
                        break
                Label(self.master, text='4 x 5 : najmanj potez - {2}, {0}   najhitrejši čas - {3}, {1} sekund'.format(p4, s4, ime14, ime24)).pack()
                
        else:
            messagebox.showerror(title='Napaka', message='Niste še odigrali nobene igre.')
            
            
            
root = Tk()

aplikacija = Spomin(root)

root.mainloop()
