from tkinter import *
from tkinter import ttk #themed ttk
import time #計算執行時間
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
mpl.rcParams['font.family']= 'SimSun'
from pandas import DataFrame
import numpy as np
import function as f #import function.py



class Main_Frame(object):
    def __init__(self, root=None):
        self.root = root
        self.l1 = ttk.Label(root, text="統計統一發票特別獎1000萬與特獎200萬中獎次數",font=('Arial', 20)).place(x=100, y=0)
        self.l2 = ttk.Label(root, text="統計方式:", font=('Arial', 15)).place(x=0, y=50)
        self.approach = ttk.Combobox(root, values=['各類別商品', '各個縣市'], font=('Arial', 15))
        self.approach.place(x=100, y=50)
        self.approach.current(0)

        self.start = ttk.Label(root, text="開始統計時間(年/月):",font=('Arial', 15)).place(x=0, y=100)
        self.start_y = ttk.Combobox(root, values=[102, 103, 104, 105,106,107,108,109], font=('Arial', 15), width=5)
        self.start_y.place(x=200, y=100)
        self.start_y.current(0)
        self.start_m = ttk.Combobox(root, values=[1,3,5,7,9,11], font=('Arial', 15), width=5)
        self.start_m.place(x=280, y=100)
        self.start_m.current(0)

        self.end = ttk.Label(root, text="開始統計時間(年/月):",font=('Arial', 15)).place(x=0, y=150)
        self.end_y = ttk.Combobox(root, values=[102, 103, 104, 105,106,107,108,109], font=('Arial', 15), width=5)
        self.end_y.place(x=200, y=150)
        self.end_y.current(7)
        self.end_m = ttk.Combobox(root, values=[1,3,5,7,9,11], font=('Arial', 15), width=5)
        self.end_m.place(x=280, y=150)
        self.end_m.current(5)

        self.btn = Button(root, text='開始計算', width=15, font=('Arial', 15),command=self.generate)
        self.btn.place(x=50, y=200)
        self.btn_quit = Button(root, text='離開', width=5,font=('Arial', 10), command=root.quit)
        self.btn_quit.place(x=730, y=5)
        self.timeLabel = ttk.Label(root,text="",font=('Arial', 15))
        self.timeLabel.place(x=10,y=250)
        self.figure = None
        self.ax = None
        self.start_time = 0
        self.end_time = 0
        #stat1 => 1000萬統計 stat2 => 200萬
        self.stat1 = {"飲品":0,"食品":0,"菸酒":0,"書籍(報紙)":0,"衣服":0,"生活用品":0,"油品":0,"繳費":0,"其他":0}  # set stat as dict 1000萬
        self.stat2 = {"飲品":0,"食品":0,"菸酒":0,"書籍(報紙)":0,"衣服":0,"生活用品":0,"油品":0,"繳費":0,"其他":0}  # set stat as dict 200萬
        self.stat1_area = {"臺北市":0,"新北市":0,"桃園市":0,"臺中市":0,"臺南市":0,"高雄市":0,"新竹縣":0,"苗栗縣":0,"彰化縣":0,"南投縣":0,"雲林縣":0,"嘉義縣":0,"屏東縣":0,"宜蘭縣":0,"花蓮縣":0,"臺東縣":0,"澎湖縣":0,"金門縣":0,"連江縣":0,"基隆市":0,"新竹市":0,"嘉義市":0}
        self.stat2_area = {"臺北市":0,"新北市":0,"桃園市":0,"臺中市":0,"臺南市":0,"高雄市":0,"新竹縣":0,"苗栗縣":0,"彰化縣":0,"南投縣":0,"雲林縣":0,"嘉義縣":0,"屏東縣":0,"宜蘭縣":0,"花蓮縣":0,"臺東縣":0,"澎湖縣":0,"金門縣":0,"連江縣":0,"基隆市":0,"新竹市":0,"嘉義市":0}
        self.root.mainloop()
    def generate(self):
        #歸零 dictionaries
        for key in self.stat1:
            self.stat1[key] = 0
            self.stat2[key] = 0
        for key in self.stat1_area:
            self.stat1_area[key] = 0
            self.stat2_area[key] = 0
        self.start_time = time.time()
        threads = []
        lock = threading.Lock()
        choice = int(self.approach.current())
        Yearx = int(self.start_y.get())
        Yeary = int(self.end_y.get())
        Monthx = int(self.start_m.get())
        Monthy = int(self.end_m.get())
        for i in range(Yearx,Yeary+1):
            if Yearx == Yeary:
                rangej = range(Monthx,Monthy+1,2)
            elif i == Yearx:
                rangej = range(Monthx,12,2)
            elif i == Yeary:
                rangej = range(1,Monthy+1,2)
            else:
                rangej = range(1,12,2)
            for j in rangej:
                if(j<10):
                    month="0"+str(j)
                else:
                    month=str(j)
                if choice == 0:
                    t = threading.Thread(target = f.job_by_item, args = (str(i),month,lock,self.stat1,self.stat2))
                elif choice == 1:
                    t = threading.Thread(target = f.job_by_country, args = (str(i),month,lock,self.stat1_area,self.stat2_area))
                t.start()
                threads.append(t)
        for thread in threads:
            thread.join()
        self.generate_mat(choice,Yearx,Yeary,Monthx,Monthy)

    def generate_mat(self,choice,Yearx,Yeary,Monthx,Monthy):
        self.initUI()
        self.end_time = time.time()
        total_time = round(self.end_time-self.start_time,2)
        self.timeLabel.config(text="共花了"+str(total_time)+"秒")
        title = ""+str(Yearx)+"年"+str(Monthx)+"月到"+str(Yeary)+"年"+str(Monthy)+"月"
        Data1 = {}
        if choice == 0:
            title += "各商品種類中獎次數統計"
            Data1 = {'商品種類名':list(self.stat1.keys()),
                    '1000萬': list(self.stat1.values()),
                    '200萬':list(self.stat2.values())
            }
            df1 = DataFrame(Data1,columns= ['商品種類名', '1000萬','200萬'])
            df1 = df1[['商品種類名','1000萬','200萬']].groupby('商品種類名').sum()
            bar = FigureCanvasTkAgg(self.figure,self.root)
            bar.get_tk_widget().place(x=380, y=50)
            df1.plot(kind='bar', ax=self.ax)
            self.ax.set_title(title)
            #self.ax.set_xticklabels(np.arange(len(listx)),listx)
        else:
            listx = list(self.stat1_area.keys())
            title += "各縣市中獎次數統計"
            Data1 ={'縣市名':list(self.stat1_area.keys()),
                    '1000萬':list(self.stat1_area.values()),
                    '200萬':list(self.stat2_area.values())
            }
            df1 = DataFrame(Data1,columns= ['縣市名', '1000萬','200萬'])
            df1 = df1[['縣市名', '1000萬','200萬']].groupby('縣市名').sum()
            bar = FigureCanvasTkAgg(self.figure,self.root)
            bar.get_tk_widget().place(x=380, y=50)
            df1.plot(kind='bar',legend=True, ax=self.ax)
            self.ax.set_title(title)
            #self.ax.set_xticklabels(np.arange(len(listx)),listx)
    def initUI(self):
        self.figure = Figure(figsize=(8,5.5), dpi=100)
        self.figure.subplots_adjust(bottom = 0.2)
        self.ax = self.figure.add_subplot(111)
        
        
if __name__ == '__main__':
    root = Tk()
    root.title("Python 期末專案")
    root.geometry("1200x800")
    Main_Frame(root=root)