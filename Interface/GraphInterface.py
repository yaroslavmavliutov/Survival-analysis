import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
import pandas as pd
from Analysis import Modeling
from Prediction import TreeDecision


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
        label = tk.Label(self, text="ПРО ПРОГРАМУ", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        label = tk.Label(self, text="Програма призначена для вибору \n оптимальної терапії", font="clearlyu")
        label.pack(pady=10, padx=10)
        label = tk.Label(self, text="Порівняння противірусних препаратів", font="clearlyu")
        label.pack(pady=5, padx=5)
        label = tk.Label(self, text="Моделювання перебігу захворювання", font="clearlyu")
        label.pack(pady=5, padx=5)

        label = tk.Label(self, text="Прогнозування вірусного агента", font="clearlyu")
        label.pack(pady=5, padx=5)
        label = tk.Label(self, text="Отримання рекомендацій", font="clearlyu")
        label.pack(pady=5, padx=5)
        button1 = tk.Button(self, text="Повернутись на головну сторінку",
                            command=lambda: controller.show_frame(StartPage), font="clearlyu")
        button1.pack(pady=30, padx=30)

        label = tk.Label(self, text="(с) Мавлютов Я.С.", font="clearlyu")
        label.pack(pady=30, padx=30)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ПОРІВНЯННЯ 2 ТЕРАПІЙ", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        button3 = tk.Button(self, text="Завантажити дані 1 терапії", font="clearlyu",
                            command=self.onOpen1)
        button3.pack()

        button3 = tk.Button(self, text="Завантажити дані 2 терапії", font="clearlyu",
                            command=self.onOpen2)
        button3.pack()
        message_button = tk.Button(self, text="Промоделювати", font="clearlyu",
                                   command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button1 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=50, padx=50)

    def onOpen1(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            print(text)
            label = tk.Label(self, text="Завантажено 1 файл "+str(fl.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def onOpen2(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            print(text)
            label = tk.Label(self, text="Завантажено 2 файл "+str(fl.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def readFile(self, filename):
        f = pd.ExcelFile(filename)
        df = f.parse('Вибірка 1')
        return df

    def show_message(self):
        Modeling.main(1, 0)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="МОДЕЛЮВАННЯ ШВИДКОСТІ ОДУЖАННЯ", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message1 = StringVar()
        message_entry = Entry(self, textvariable=message1, bd=1)
        message_entry.pack(padx=7, pady=0)

        L1 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message = StringVar()
        message_entry = Entry(self, textvariable=message, bd=1)
        message_entry.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова локалізація", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Однобічна', 'Двобічна']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        variable = StringVar(self)
        variable.set('Повне розсмоктування')
        w = OptionMenu(self, variable, *choices)
        w.config(font=("clearlyu", 12))
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Стабільний', 'Середньої важкості', 'Важкий']
        variable = StringVar(self)
        variable.set('Стабільний')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        message_button = tk.Button(self, text="Промоделювати", font="clearlyu",
                                   command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button1 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=2, padx=2)

    def show_message(self):
        Modeling.main(1, 1)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="МОДЕЛЮВАННЯ ДИНАМІКИ КЛІНІЧНОГО ПАРАМЕТРУ", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        L2 = Label(self, text="Клінічний параметр", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Температура тіла', 'Характер мокротіння', 'Локалізація', 'Рентгенодинаміка', 'Загальний стан']
        variable = StringVar(self)
        variable.set('Температура тіла')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message = StringVar()
        message_entry = Entry(self, textvariable=message, bd=1)
        message_entry.pack(padx=7, pady=0)

        L1 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message = StringVar()
        message_entry = Entry(self, textvariable=message, bd=1)
        message_entry.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова локалізація", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Однобічна', 'Двобічна']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        variable = StringVar(self)
        variable.set('Повне розсмоктування')
        w = OptionMenu(self, variable, *choices)
        w.config(font=("clearlyu", 12))
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Стабільний', 'Середньої важкості', 'Важкий']
        variable = StringVar(self)
        variable.set('Стабільний')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        message_button = tk.Button(self, text="Промоделювати", font="clearlyu", command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button1 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=2, padx=2)

    def show_message(self):
        Modeling.main(1, 2)

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ПОРІВНЯННЯ ДИНАМІКИ ПАРАМЕТРІВ 2 ТЕРАПІЙ", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        L2 = Label(self, text="Клінічний параметр", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Температура тіла', 'Характер мокротіння', 'Локалізація', 'Рентгенодинаміка', 'Загальний стан']
        variable = StringVar(self)
        variable.set('Температура тіла')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=10)

        button3 = tk.Button(self, text="Завантажити дані 1 терапії", font="clearlyu",
                            command=self.onOpen1)
        button3.pack()

        button3 = tk.Button(self, text="Завантажити дані 2 терапії", font="clearlyu",
                            command=self.onOpen2)
        button3.pack()

        message_button = tk.Button(self, text="Промоделювати", font="clearlyu",
                                   command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button1 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=50, padx=50)

    def onOpen1(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            print(text)
            label = tk.Label(self, text="1 load " + str(fl.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def onOpen2(self):
        ftypes = [('Python files', '*.xlsx'), ('All files', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            print(text)
            label = tk.Label(self, text="2 load " + str(fl.split("/")[-1]), font=LARGE_FONT)
            label.pack(pady=0, padx=0)

    def readFile(self, filename):
        f = pd.ExcelFile(filename)
        df = f.parse('Вибірка 1')
        return df

    def show_message(self):
        Modeling.main(1, 11)

class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ПРОГНОЗ ВІРУСНОГО АГЕНТА", font=LARGE_FONT)
        label.pack(pady=2, padx=15)

        L1 = Label(self, text="Вік", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message = StringVar()
        message_entry = Entry(self, textvariable=message, bd=1)
        message_entry.pack(padx=7, pady=0)

        L1 = Label(self, text="Початкова температура тіла (36-42)", font="clearlyu")
        L1.pack(padx=3, pady=0)
        message = StringVar()
        message_entry = Entry(self, textvariable=message, bd=1)
        message_entry.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий характер мокротіння", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Слизове', 'Слизово-гнійне', 'Гнійне']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова локалізація", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Нема', 'Однобічна', 'Двобічна']
        variable = StringVar(self)
        variable.set('Нема')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початкова рентгенодинаміка", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Повне розсмоктування', 'Часткове розсмоктування', 'Динаміка відсутня', 'Відм\'ємна динаміка']
        variable = StringVar(self)
        variable.set('Повне розсмоктування')
        w = OptionMenu(self, variable, *choices)
        w.config(font=("clearlyu", 12))
        w.pack(padx=7, pady=0)

        L2 = Label(self, text="Початковий загальний стан", font="clearlyu")
        L2.pack(padx=3, pady=0)
        choices = ['Стабільний', 'Середньої важкості', 'Важкий']
        variable = StringVar(self)
        variable.set('Стабільний')
        w = OptionMenu(self, variable, *choices)
        w.config(font="clearlyu")
        w.pack(padx=7, pady=0)

        message_button = tk.Button(self, text="Прогноз", font="clearlyu", command=self.show_message)
        message_button.pack(padx=14, pady=5, anchor="n")

        button1 = tk.Button(self, text="Повернутись на головну сторінку", font="clearlyu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=2, padx=2)

    def show_message(self):
        TreeDecision.predict()


app = SeaofBTCapp()
app.mainloop()


