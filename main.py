# coding=utf-8
'''
Created on 2018年3月30日
 @author: Gameplayer0928 Qi Gao
'''

# import matplotlib
# matplotlib.use("Agg")

import codecs

import re
import numpy as np
import matplotlib.pyplot as plt
import time

import tkinter
import tkinter.filedialog
import sys

from pylab import mpl 
mpl.rcParams['font.sans-serif'] = ['SimHei']      # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False        # 解决保存图像是负号'-'显示为方块的问题


CURRENTDATE = int(time.strftime("%Y%m%d"))
DAV = np.dtype([("date",np.str_,8),("value",np.float)])

class MainGui():
    def __init__(self):
        self.maingui = tkinter.Tk()
        self.maingui.title("j10 data clean and show")
        
        
        #         self.scsv1file = None
#         self.scsv2file = None
        self.filename = None
        
        self.data1 = None
        self.data2 = None
        
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        
        self.datatile1 = None
        self.datatile2 = None
        
        button1 = tkinter.Button(self.maingui,text='select text file copy from j10 html, txt file dispose to csv',command = self._load_file_to_csv,relief = "raised",borderwidth = 5)
        button1.pack()

        
        buttonframe = tkinter.Frame(self.maingui,borderwidth = 10,relief = "groove")
        buttonframe.pack()
        label = tkinter.Label(buttonframe,text="Simple CSV data compare")
        label.pack(side='top')
        button2 = tkinter.Button(buttonframe,text='first data',command = self._csv1)
        button2.pack(side='left')
        button3 = tkinter.Button(buttonframe,text='second data',command = self._csv2)
        button3.pack(side='left')
        button4 = tkinter.Button(buttonframe,text='show in matplotlib',command = self._show,bg = 'red')
        button4.pack(side='right')
        

        
        self.maingui.mainloop()
        

        
    def _load_file_to_csv(self):
        fl = tkinter.filedialog.FileDialog(self.maingui)
        fl.title = "load txt file to csv"
        cd = fl.go('./')
        self.filename = cd
        file = codecs.open(self.filename,"r",encoding='gbk')
        text = file.read()
        file.close()
    
    
        mark = '<a data-date="(\d+)" href'
        mark2 ='data-type="今值" data-report="1">(\S+)</a>'
    
        dd = re.findall(mark, text)   ## clean date data
        value = re.findall(mark2,text) ## clean value data
        
        dd.reverse()
        value.reverse()
        
        
        ldav = []
        
        for i in range(len(dd)):
            if int(dd[i]) < CURRENTDATE:
                ldav.append((dd[i],value[i])) 
        
        da = np.array(ldav,dtype = DAV)
            
        np.savetxt(self.filename[:-4]+".csv",da, delimiter=',',fmt='%s,%f',encoding="utf-8")
    
    def _read_csv(self):
        fl = tkinter.filedialog.FileDialog(self.maingui)
        fl.title = "load csv"
        cd = fl.go("./")
        return cd
    
    def _csv1(self):
        self.datatile1 = self._read_csv()
        self.data1 = np.loadtxt(self.datatile1, dtype = DAV,delimiter = ',',usecols = (0,1),encoding = "utf-8")
        
    def _csv2(self):
        self.datatile2 = self._read_csv()
        self.data2 = np.loadtxt(self.datatile2, dtype = DAV,delimiter = ',',usecols = (0,1),encoding = "utf-8")
        
    def _split_data(self):
        self.x1 = self.data1["date"]
        self.y1 = self.data1["value"]
        self.x2 = self.data2["date"]
        self.y2 = self.data2["value"]
    
  
    def _show(self):
        self._split_data()

        
        ax1 = plt.subplot(211)
        ax1.plot(self.x1,self.y1)
        ax1.tick_params('x',labelsize = 8,rotation = 90)
        ax1.grid(True,alpha = 0.5)
        ax1.set_xticks(range(0,len(self.x1),5))
        ax1.set_ylabel(self.datatile1.split("\\")[-1][:-4])
        
        ax2 = plt.subplot(212)
        ax2.plot(self.x2,self.y2)
        ax2.tick_params('x',labelsize = 8,rotation = 90)
        ax2.grid(True,alpha = 0.5)
        ax2.set_xticks(range(0,len(self.x2),5))
        ax2.set_ylabel(self.datatile2.split("\\")[-1][:-4])

        plt.show()

if __name__ == "__main__":
    MG = MainGui()