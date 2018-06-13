import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
import pandas as pd
from Analysis import Modeling
from Prediction import TreeDecision
from functools import partial


LARGE_FONT = ("clearlyu", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # game you can specify the attributes for all widgets simply like this.
        #self.option_add("*Button.Background", )
        self.option_add("*Foreground", "black")

        #self.option_add('*Font', 'arial')
        #self.option_add('*Foreground', 'black')
       # self.option_add('*Label*Font', label_font)
        # self.option_add('*Listbox*Font', listbox_font)
        # self.option_add('*Listbx*Background', 'green')
        # self.option_add('*Listbox*Foreground', 'brown')

        self.title('АнтиВірус')
        # You can set the geometry attribute to change the root windows size
        self.geometry("500x650")  # You want the size of the app to be 500x500
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction


        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageAbout, PageOne, PageTwo, PageFour, PageFive, PageSix):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        buttonabout = tk.Button(self, text="Про програму", font=LARGE_FONT,
                           command=lambda: controller.show_frame(PageAbout), width=50, height=1)
        buttonabout.pack(pady=10, padx=5)

        button1 = tk.Button(self, text="Порівняння 2 терапій", font=LARGE_FONT,
                           command=lambda: controller.show_frame(PageOne), width=50, height=1)
        button1.pack(pady=10, padx=5)

        button2 = tk.Button(self, text="Моделювання швидкості одужання", font=LARGE_FONT,
                            command=lambda: controller.show_frame(PageTwo), width=50, height=1)
        button2.pack(pady=10, padx=5)


        button4 = tk.Button(self, text="Моделювання динаміки клінічного параметру", font=LARGE_FONT,
                           command=lambda: controller.show_frame(PageFour), width=50, height=1)
        button4.pack(pady=10, padx=5)

        button5 = tk.Button(self, text="Порівняння динаміки параметрів 2 терапій",font=LARGE_FONT,
                           command=lambda: controller.show_frame(PageFive), width=50, height=1)
        button5.pack(pady=10, padx=5)

        button6 = tk.Button(self, text="Прогноз вірусного агента",font=LARGE_FONT,
                           command=lambda: controller.show_frame(PageSix), width=50, height=1)
        button6.pack(pady=10, padx=5)

class PageAbout(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="ПРО ПРОГРАМУ", font=LARGE_FONT)
        label1.pack(pady=15, padx=15)

        label2 = tk.Label(self, text="Програма призначена для вибору \n оптимальної терапії", font="clearlyu")
        label2.pack(pady=10, padx=10)
        label3 = tk.Label(self, text="Порівняння противірусних препаратів", font="clearlyu")
        label3.pack(pady=5, padx=5)
        label4 = tk.Label(self, text="Моделювання перебігу захворювання", font="clearlyu")
        label4.pack(pady=5, padx=5)

        label5 = tk.Label(self, text="Прогнозування вірусного агента", font="clearlyu")
        label5.pack(pady=5, padx=5)
        label6 = tk.Label(self, text="Отримання рекомендацій", font="clearlyu")
        label6.pack(pady=5, padx=5)
        button1 = tk.Button(self, text="Повернутись на головну сторінку",
                            command=lambda: controller.show_frame(StartPage), font="clearlyu")
        button1.pack(pady=30, padx=30)

        label7 = tk.Label(self, text="(с) Мавлютов Я.С.", font="clearlyu")
        label7.pack(pady=30, padx=30)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="ПОРІВНЯННЯ 2 ТЕРАПІЙ", font=LARGE_FONT)
        label1.pack(pady=15, padx=15)

        button1 = tk.Button(self, text="Завантажити дані 1 терапії", font="clearlyu",
                            command=self.onOpen1)
        button1.pack()

        button2 = tk.Button(self, text="Завантажити дані 2 терапії", font="clearlyu",
                            command=self.onOpen2)
        button2.pack()
        message_button = tk.Button(self, text="Промоделювати", font="clearlyu",
                                   command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button3 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button3.pack(pady=50, padx=50)

    def onOpen1(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        self.fl1 = dlg.show()

        if self.fl1 != '':
            text = self.readFile(self.fl1)
            label = tk.Label(self, text="Завантажено 1 файл "+str(self.fl1.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def onOpen2(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        self.fl2 = dlg.show()

        if self.fl2 != '':
            text = self.readFile(self.fl2)
            label = tk.Label(self, text="Завантажено 2 файл "+str(self.fl2.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def readFile(self, filename):
        f = pd.ExcelFile(filename)
        df = f.parse('Вибірка 1')
        return df

    def show_message(self):
        Modeling.main(1, 0, [self.fl1, self.fl2])

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="МОДЕЛЮВАННЯ ШВИДКОСТІ ОДУЖАННЯ", font=LARGE_FONT)
        label1.pack(pady=15, padx=15)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message1 = StringVar()
        self.message_entry1 = Entry(self, textvariable=message1, bd=1)
        self.message_entry1.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L2.pack(padx=3, pady=0)
        message2 = StringVar()
        self.message_entry2 = Entry(self, textvariable=message2, bd=1)
        self.message_entry2.pack(padx=7, pady=0)

        L3 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L3.pack(padx=3, pady=0)
        choices3 = ['Відсутнє', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        self.variable3 = StringVar(self)
        self.variable3.set('Відсутнє')
        w3 = OptionMenu(self, self.variable3, *choices3)
        w3.config(font="clearlyu")
        w3.pack(padx=7, pady=0)

        L4 = Label(self, text="Початкова локалізація", font="clearlyu")
        L4.pack(padx=3, pady=0)
        choices4 = ['Відсутня', 'Однобічна', 'Двобічна']
        self.variable4 = StringVar(self)
        self.variable4.set('Відсутня')
        w4 = OptionMenu(self, self.variable4, *choices4)
        w4.config(font="clearlyu")
        w4.pack(padx=7, pady=0)

        L5 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L5.pack(padx=3, pady=0)
        choices5 = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        self.variable5 = StringVar(self)
        self.variable5.set('Повне розсмоктування')
        w5 = OptionMenu(self, self.variable5, *choices5)
        w5.config(font=("clearlyu", 12))
        w5.pack(padx=7, pady=0)

        L6 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L6.pack(padx=3, pady=0)
        choices6 = ['Стабільний', 'Середньої важкості', 'Важкий']
        self.variable6 = StringVar(self)
        self.variable6.set('Стабільний')
        w6 = OptionMenu(self, self.variable6, *choices6)
        w6.config(font="clearlyu")
        w6.pack(padx=7, pady=0)

        button1 = tk.Button(self, text="Промоделювати", font="clearlyu", command=self.show_message)
        button1.pack(padx=14, pady=5, anchor="n")

        button2 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=2, padx=2)

    def show_message(self):
        print(self.variable3.get())
        Modeling.main(1, 1, [self.message_entry1.get(), self.message_entry2.get(), self.variable3.get(), self.variable4.get(),
                             self.variable5.get(), self.variable6.get()])

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="МОДЕЛЮВАННЯ ДИНАМІКИ КЛІНІЧНОГО ПАРАМЕТРУ", font=LARGE_FONT)
        label1.pack(pady=15, padx=15)

        L0 = Label(self, text="Клінічний параметр", font="clearlyu")
        L0.pack(padx=3, pady=0)
        choices0 = ['Температура тіла', 'Характер мокротіння', 'Локалізація', 'Рентгенодинаміка', 'Загальний стан']
        self.variable0 = StringVar(self)
        self.variable0.set('Температура тіла')
        w0 = OptionMenu(self, self.variable0, *choices0)
        w0.config(font="clearlyu")
        w0.pack(padx=7, pady=0)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message1 = StringVar()
        self.message_entry1 = Entry(self, textvariable=message1, bd=1)
        self.message_entry1.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L2.pack(padx=3, pady=0)
        message2 = StringVar()
        self.message_entry2 = Entry(self, textvariable=message2, bd=1)
        self.message_entry2.pack(padx=7, pady=0)

        L3 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L3.pack(padx=3, pady=0)
        choices3 = ['Відсутнє', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        self.variable3 = StringVar(self)
        self.variable3.set('Відсутнє')
        w3 = OptionMenu(self, self.variable3, *choices3)
        w3.config(font="clearlyu")
        w3.pack(padx=7, pady=0)

        L4 = Label(self, text="Початкова локалізація", font="clearlyu")
        L4.pack(padx=3, pady=0)
        choices4 = ['Відсутня', 'Однобічна', 'Двобічна']
        self.variable4 = StringVar(self)
        self.variable4.set('Відсутня')
        w4 = OptionMenu(self, self.variable4, *choices4)
        w4.config(font="clearlyu")
        w4.pack(padx=7, pady=0)

        L5 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L5.pack(padx=3, pady=0)
        choices5 = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        self.variable5 = StringVar(self)
        self.variable5.set('Повне розсмоктування')
        w5 = OptionMenu(self, self.variable5, *choices5)
        w5.config(font=("clearlyu", 12))
        w5.pack(padx=7, pady=0)

        L6 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L6.pack(padx=3, pady=0)
        choices6 = ['Стабільний', 'Середньої важкості', 'Важкий']
        self.variable6 = StringVar(self)
        self.variable6.set('Стабільний')
        w6 = OptionMenu(self, self.variable6, *choices6)
        w6.config(font="clearlyu")
        w6.pack(padx=7, pady=0)

        button1 = tk.Button(self, text="Промоделювати", font="clearlyu", command=self.show_message)
        button1.pack(padx=14, pady=5, anchor="n")

        button2 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=2, padx=2)

    def show_message(self):
        if self.variable0.get() == 'Температура тіла':
            el = 2
        elif self.variable0.get() == 'Характер мокротіння':
            el = 3
        elif self.variable0.get() == 'Локалізація':
            el = 4
        elif self.variable0.get() == 'Рентгенодинаміка':
            el = 5
        elif self.variable0.get() == 'Загальний стан':
            el = 6
        Modeling.main(1, self.variable0,
                      [self.message_entry1.get(), self.message_entry2.get(), self.variable3.get(), self.variable4.get(),
                       self.variable5.get(), self.variable6.get()])

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="ПОРІВНЯННЯ ДИНАМІКИ ПАРАМЕТРІВ 2 ТЕРАПІЙ", font=LARGE_FONT)
        label1.pack(pady=15, padx=15)

        L1 = Label(self, text="Клінічний параметр", font="clearlyu")
        L1.pack(padx=3, pady=0)
        choices1 = ['Температура тіла', 'Характер мокротіння', 'Локалізація', 'Рентгенодинаміка', 'Загальний стан']
        self.variable1 = StringVar(self)
        self.variable1.set('Температура тіла')
        w1 = OptionMenu(self, self.variable1, *choices1)
        w1.config(font="clearlyu")
        w1.pack(padx=7, pady=10)

        button1 = tk.Button(self, text="Завантажити дані 1 терапії", font="clearlyu",
                            command=self.onOpen1)
        button1.pack()

        button2 = tk.Button(self, text="Завантажити дані 2 терапії", font="clearlyu",
                            command=self.onOpen2)
        button2.pack()

        button3 = tk.Button(self, text="Промоделювати", font="clearlyu",
                                   command=self.show_message)
        button3.pack(padx=14, pady=5, anchor="n")

        button4 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button4.pack(pady=50, padx=50)

    def onOpen1(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        self.fl1 = dlg.show()

        if self.fl1 != '':
            text = self.readFile(self.fl1)
            print(text)
            label = tk.Label(self, text="1 load " + str(self.fl1.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def onOpen2(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        self.fl2 = dlg.show()

        if self.fl2 != '':
            text = self.readFile(self.fl2)
            print(text)
            label = tk.Label(self, text="2 load " + str(self.fl2.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def readFile(self, filename):
        f = pd.ExcelFile(filename)
        df = f.parse('Вибірка 1')
        return df

    def show_message(self):
        if self.variable1.get() == 'Температура тіла':
            el = 7
        elif self.variable1.get() == 'Характер мокротіння':
            el = 8
        elif self.variable1.get() == 'Локалізація':
            el = 9
        elif self.variable1.get() == 'Рентгенодинаміка':
            el = 10
        elif self.variable1.get() == 'Загальний стан':
            el = 11
        Modeling.main(1, el, [self.fl1, self.fl2])

class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="ПРОГНОЗ ВІРУСНОГО АГЕНТА", font=LARGE_FONT)
        label1.pack(pady=2, padx=15)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message1 = StringVar()
        self.message_entry1 = Entry(self, textvariable=message1, bd=1)
        self.message_entry1.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L2.pack(padx=3, pady=0)
        message2 = StringVar()
        self.message_entry2 = Entry(self, textvariable=message2, bd=1)
        self.message_entry2.pack(padx=7, pady=0)

        L3 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L3.pack(padx=3, pady=0)
        choices3 = ['Відсутнє', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        self.variable3 = StringVar(self)
        self.variable3.set('Відсутнє')
        w3 = OptionMenu(self, self.variable3, *choices3)
        w3.config(font="clearlyu")
        w3.pack(padx=7, pady=0)

        L4 = Label(self, text="Початкова локалізація", font="clearlyu")
        L4.pack(padx=3, pady=0)
        choices4 = ['Відсутня', 'Однобічна', 'Двобічна']
        self.variable4 = StringVar(self)
        self.variable4.set('Відсутня')
        w4 = OptionMenu(self, self.variable4, *choices4)
        w4.config(font="clearlyu")
        w4.pack(padx=7, pady=0)

        L5 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L5.pack(padx=3, pady=0)
        choices5 = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        self.variable5 = StringVar(self)
        self.variable5.set('Повне розсмоктування')
        w5 = OptionMenu(self, self.variable5, *choices5)
        w5.config(font=("clearlyu", 12))
        w5.pack(padx=7, pady=0)

        L6 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L6.pack(padx=3, pady=0)
        choices6 = ['Стабільний', 'Середньої важкості', 'Важкий']
        self.variable6 = StringVar(self)
        self.variable6.set('Стабільний')
        w6 = OptionMenu(self, self.variable6, *choices6)
        w6.config(font="clearlyu")
        w6.pack(padx=7, pady=0)

        button1 = tk.Button(self, text="Прогноз", font="clearlyu", command=self.show_message)
        button1.pack(padx=14, pady=5, anchor="n")

        button2 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=2, padx=2)

    def show_message(self):
        TreeDecision.predict([self.message_entry1.get(), self.message_entry2.get(), self.variable3.get(), self.variable4.get(),
                             self.variable5.get(), self.variable6.get()])


app = SeaofBTCapp()
app.mainloop()


