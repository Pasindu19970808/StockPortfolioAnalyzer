import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import ssl
import datetime
from tkcalendar import Calendar



class Main(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args)
        s = ttk.Style(self)
        s.theme_use('clam')
        nb = ttk.Notebook(self)
        
        containerbuy = tk.Frame(nb)

        #containerprogress = tk.Frame(nb)
        #containersell = tk.Frame(nb)
        self.buyframes = {}
        buypage = buypageclass(containerbuy,self)
        self.buyframes[buypageclass] = buypage
        buypage.grid(row = 1, column = 1, sticky = 'nsew')
        buypage.tkraise()
        
       
        
        nb.add(containerbuy, text = 'Buy Page')
        nb.pack(expand = 1, fill = 'both')
        
    def showdateframe(self, controller):
        def select_date():
            dateofbuy = cal.selection_get()
            self.passondate(dateofbuy)
       
        datechildwindow = tk.Toplevel(self)
        cal = Calendar(datechildwindow,\
                   font="Arial 14", selectmode='day',\
                   cursor="hand1", year=2020, month=1, day=1)
        cal.pack(side = 'top',fill="both", expand=True)
        dateselectionbutton = tk.Button(datechildwindow, text = 'Confirm', command = select_date)
        dateselectionbutton.pack(side = 'top')
    
    def passondate(self,dateofbuy):
        buypage = self.buyframes[buypageclass]
        buypage.datelabel.configure(text = dateofbuy)
        buypage.buydate = dateofbuy
        print(buypage.buydate)
        

class buypageclass(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        s = ttk.Style(self)
        s.theme_use('clam')
        
        self.controller = controller
        
        
        #SQL section
        self.conn = sqlite3.connect('stockportfoliodb.sqlite')
        self.curs = self.conn.cursor()
        
        self.curs.execute('''CREATE TABLE IF NOT EXISTS StocksInPortfolio(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                ticker_name TEXT)''')
        
        self.conn.commit()
        self.conn.close()
        
        self.buyframeone = tk.LabelFrame(self, text = 'Entry for newly bought shares')
        self.buyframeone.pack(side = 'left', padx = 10, pady = 10)
        
       
        
        radiovar = tk.IntVar()
        self.radiobuttonframe = tk.LabelFrame(self.buyframeone, text = 'Is This Company A New Addition To Your Portfolio?')
        self.radiobuttonframe.pack(side = 'top',padx = 10, pady = 10)
        #radiobutton2
        self.newstockbutton = tk.Radiobutton(self.radiobuttonframe, text = 'Yes, This Is A New Addition To My Portfolio', variable = radiovar, value = 0, command = lambda: self.activation(radiovar.get()))
        self.newstockbutton.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
        #radiobutton1
        self.existingstockbutton = tk.Radiobutton(self.radiobuttonframe, text = 'No, The Company Exists in My Portfolio', variable = radiovar, value = 1, command =  lambda: self.activation(radiovar.get()))
        self.existingstockbutton.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'w')
        
       
        #entryframe
        self.entryframe = tk.LabelFrame(self.buyframeone)
        self.entryframe.pack(side = 'top', padx = 10, pady = 10)
        #entrylabel
        self.entrylabel = tk.Label(self.entryframe, text = 'Ticker Symbol', relief = 'solid')
        self.entrylabel.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
        #entrytypebox
        self.tickerentrybox = tk.Entry(self.entryframe, bd = 2, relief = 'sunken',state = 'disabled')
        self.tickerentrybox.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        
        self.costlabel = tk.Label(self.entryframe, text = 'Buying Price', relief = 'solid')
        self.costlabel.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')
        #Buy price
        self.priceentrybox = tk.Entry(self.entryframe,bd = 2, relief = 'sunken', state = 'disabled')
        self.priceentrybox.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = 'w')
       
       
        
        #quantity of shares
        self.quantitylabel = tk.Label(self.entryframe, text = 'Amount of Shares', relief = 'solid')
        self.quantitylabel.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'w')
        
        self.numberofshares = tk.IntVar()
        self.quantity = list(range(0,101))
        self.quantitydropdown = tk.OptionMenu(self.entryframe, self.numberofshares,())
        self.quantitydropdown.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = 'w')
        self.quantitymenu = self.quantitydropdown['menu']
        for quant in self.quantity:
            self.quantitymenu.add_command(label = quant, command = lambda value = quant:self.numberofshares.set(value))
        self.quantitydropdown.configure(state = 'disabled')


        
        #exitingstockframe
        self.existingframe = tk.LabelFrame(self.buyframeone)
        self.existingframe.pack(side = 'top', padx = 10, pady = 10)
        
        #existinglabel
        self.existinglabel = tk.Label(self.existingframe, text = 'Ticker Symbol', relief = 'solid')
        self.existinglabel.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
        self.existingticker = tk.StringVar()
        self.existingticker.set('Select Ticker Symbol')
        self.portfolioshares = tk.OptionMenu(self.existingframe,self.existingticker,())
        self.portfolioshares.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        #quantity of shares
        self.numberofsharesexisting = tk.IntVar()
        self.quantitydropdownexisting = tk.OptionMenu(self.existingframe, self.numberofsharesexisting,())
        self.quantitydropdownexisting.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = 'w')
        self.quantitymenuexisting = self.quantitydropdownexisting['menu']
        for quant in self.quantity:
            self.quantitymenuexisting.add_command(label = quant, command = lambda value = quant:self.numberofsharesexisting.set(value))
        self.quantitydropdownexisting.configure(state = 'disabled')
        
        
                #dateframe
        self.dateframe = tk.LabelFrame(self.buyframeone, text = 'Select Date of Buy')
        self.dateframe.pack(side = 'top',padx = 10, pady = 10)
        #date selection button
        self.datebutton = tk.Button(self.dateframe,text = 'Select Date', command = lambda:self.controller.showdateframe(controller))
        self.datebutton.pack(side = 'left',padx = 10, pady = 10)
        
        self.datelabel = tk.Label(self.dateframe, text = 'Date Is Not Selected')
        self.datelabel.pack(side = 'left', padx = 10, pady = 10)
        self.buydate = tk.StringVar()
        
        
        
        
        #entrydropdown
        #self.label1 = tk.Label(self.buyframeone, text = 'hi')
        #self.label1.grid(row = 6, column = 1)
    def activation(self,radiovar):
        if radiovar == 1:
            self.numberofshares.set(0)
            self.tickerentrybox.configure(state = 'disabled')
            self.priceentrybox.configure(state = 'disabled')
            self.quantitydropdown.configure(state = 'disabled')
            self.quantitydropdownexisting.configure(state = 'normal')
            
            #SQL section(getting the existing stocks)
            self.conn = sqlite3.connect('stockportfoliodb.sqlite')
            self.curs = self.conn.cursor()
            
            row = self.curs.execute('''SELECT ticker_name FROM StocksInPortfolio''')
            tickernames = row.fetchall()
            if len(tickernames) == 0:
                tk.messagebox.showinfo('Attention','No Companies available in your Portfolio')
            print(row)
            
            
        elif radiovar == 0:
            self.numberofsharesexisting.set(0)
            self.tickerentrybox.configure(state = 'normal')
            self.priceentrybox.configure(state = 'normal')
            self.quantitydropdown.configure(state = 'normal')
            self.quantitydropdownexisting.configure(state = 'disabled')


        
            
            
        


root = Main()
root.mainloop()

        
        