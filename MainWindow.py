# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:12:28 2022

@author: Jasio
"""

import tkinter as tk
from tkinter import X, Y, BOTH, YES, LEFT, RIGHT, TOP, BOTTOM, END, E, W

from tkfactory.TkFactory import TkFactory
from tkfactory.MyFactory import MyFactory
import matplotlib.pyplot as plt
import numpy as np

import parameters
import DataLoader
from PlotObject import PlotObject

factory = TkFactory.getFactory()
mfactory = MyFactory.getFactory()


class MainWindow(tk.Tk):
    '''
        Główne okno programu
    '''
    
    
    def __init__(self):
        """
        Inicjacja głównego okna
        Zmienne:
            widgets (dic): Słownik zawierający łącza do widgetów
            pltIndex (int): Numer obecnie wyświetlanego wykresu
        """
        # Wywołanie konstruktora okna Tk
        tk.Tk.__init__(self)
        # Słownik z ikonami interfejsu pozwalający na łatwy dostęp do nich po używym kluczu
        self.widgets = {}
        # Licznik numeru obecnie wyświetlanego wykresu
        self.pltIndex = 1
        # Inicjowanie zmiennych parametrów
        parameters.InitVariables()
        # Budowanie interfejsu
        self.build()
        # Inicjalizacja połączenia z bazą danych
        self.initActions()
    
    
    def initActions(self):
        """
        Funkcja łąduje łącze do bazy danych i inicjuje domyślne zachowania gui takie jak reakcja na zmianę pola
        """
        # Ustawianie zestwów danych i wartości początkowych
        ComboboxDataSet = tuple( ["brak"] + sorted( DataLoader.GetCompaniesList() ) )
        self.widgets["companyCombo1"].config(values=ComboboxDataSet)
        self.widgets["companyCombo1"].current(0)
        self.widgets["companyCombo2"].config(values=ComboboxDataSet)
        self.widgets["companyCombo2"].current(0)
        # Ustawianie informacji początkowej o firmie
        parameters.DataFlag_About.set("Nie wybrano firmy")


    def build(self):
        """
        Funkcja budująca interfejs
        """
        # Tworzenie menu
        self.widgets["menu"] = factory.getMenu(self)

        self.widgets["databaseMenu"] = factory.getMenu(self.widgets["menu"])
        self.widgets["menu"].add_cascade(label="Symulacja", menu=self.widgets["databaseMenu"])

        self.widgets["infoMenu"] = factory.getMenu(self.widgets["menu"])
        self.widgets["menu"].add_cascade(label="Info", menu=self.widgets["infoMenu"])
        self.widgets["infoMenu"].add_command(label="O programie", command=self.showInfoAboutProgram)

        self.config(menu=self.widgets["menu"])

        # Tworzenie głównego okna wyboru parametrów
        self.widgets["mChoiceFrame"] = factory.getFrame(self)
        self.widgets["mChoiceFrame"].pack(side=LEFT, fill=BOTH)
        self.widgets["mChoiceFrame"].config(borderwidth=2)

        self.widgets["commentLabel1"] = factory.getLabel(self.widgets["mChoiceFrame"], "Zakres czasu")
        self.widgets["commentLabel1"].grid(row=0, column=1, columnspan=2)

        # Menu wyboru daty
        # Pola danych: DataFlag_StartTime, DataFlag_EndTime
        self.widgets["startDateLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Data Startowa")
        self.widgets["startDateLabel"].grid(row=1, column=1)
        self.widgets["startDateEntry"] = factory.getEntry(self.widgets["mChoiceFrame"])
        self.widgets["startDateEntry"].config(textvariable=parameters.DataFlag_StartTime)
        self.widgets["startDateEntry"].insert(0, "2022-01-01")
        self.widgets["startDateEntry"].grid(row=1, column=2)
        self.widgets["endDateLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Data Końcowa")
        self.widgets["endDateLabel"].grid(row=2, column=1)
        self.widgets["endDateEntry"] = factory.getEntry(self.widgets["mChoiceFrame"])
        self.widgets["endDateEntry"].config(textvariable=parameters.DataFlag_EndTime)
        self.widgets["endDateEntry"].insert(0, "2022-02-01")
        self.widgets["endDateEntry"].grid(row=2, column=2)
        self.widgets["dateFormatLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Dostępny zakres od 2022-01-01 do 2022-04-26")
        self.widgets["dateFormatLabel"].grid(row=3, column=1, columnspan=2)
        self.widgets["separator1"] = factory.getSeparator(self.widgets["mChoiceFrame"])
        self.widgets["separator1"].grid(row=4, column=1, columnspan=2, sticky="ew")

        # Menu wyboru wyświetlanych serii danych
        # Pola danych z parameters: DataFlag_Open, DataFlag_High, DataFlag_Low, DataFlag_Close, DataFlag_Volume
        self.widgets["displayDataLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Wyświetlane serie danych")
        self.widgets["displayDataLabel"].grid(row=5, column=1, columnspan=2)
        self.widgets["displayDataCheck_Open"] = factory.getCheckbutton(self.widgets["mChoiceFrame"], "Open", parameters.DataFlag_Open)
        self.widgets["displayDataCheck_Open"].grid(row=6, column=1, columnspan=2, sticky=W)
        self.widgets["displayDataCheck_High"] = factory.getCheckbutton(self.widgets["mChoiceFrame"], "High", parameters.DataFlag_High)
        self.widgets["displayDataCheck_High"].grid(row=7, column=1, columnspan=2, sticky=W)
        self.widgets["displayDataCheck_Low"] = factory.getCheckbutton(self.widgets["mChoiceFrame"], "Low", parameters.DataFlag_Low)
        self.widgets["displayDataCheck_Low"].grid(row=8, column=1, columnspan=2, sticky=W)
        self.widgets["displayDataCheck_Close"] = factory.getCheckbutton(self.widgets["mChoiceFrame"], "Close", parameters.DataFlag_Close)
        self.widgets["displayDataCheck_Close"].grid(row=9, column=1, columnspan=2, sticky=W)
        self.widgets["displayDataCheck_Volume"] = factory.getCheckbutton(self.widgets["mChoiceFrame"], "Volume", parameters.DataFlag_Volume)
        self.widgets["displayDataCheck_Volume"].grid(row=10, column=1, columnspan=2, sticky=W)
        self.widgets["separator2"] = factory.getSeparator(self.widgets["mChoiceFrame"])
        self.widgets["separator2"].grid(row=11, column=1, columnspan=2, sticky="ew")

        # Menu wybierania wyświetlanych firm
        # Pola parametrów: DataFlag_Company1, DataFlag_Company2
        self.widgets["displayCompanyLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Wyświetlane firmy")
        self.widgets["displayCompanyLabel"].grid(row=12, column=1, columnspan=2)
        self.widgets["companyCombo1"] = factory.getCombobox(self.widgets["mChoiceFrame"], [])
        self.widgets["companyCombo1"].config(textvariable=parameters.DataFlag_Company1)
        self.widgets["companyCombo1"].grid(row=13, column=1, columnspan=2, sticky="ew")
        self.widgets["companyCombo2"] = factory.getCombobox(self.widgets["mChoiceFrame"], [])
        self.widgets["companyCombo2"].config(textvariable=parameters.DataFlag_Company2)
        self.widgets["companyCombo2"].grid(row=14, column=1, columnspan=2, sticky="ew")
        self.widgets["emptyLabel1"] = factory.getLabel(self.widgets["mChoiceFrame"], "")
        self.widgets["emptyLabel1"].grid(row=17, column=1, columnspan=2)
        self.widgets["separator3"] = factory.getSeparator(self.widgets["mChoiceFrame"])
        self.widgets["separator3"].grid(row=18, column=1, columnspan=2, sticky="ew")

        # Przycisk wywołujący stworzenie nowego wykresu
        self.widgets["actionLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Dostępne akcje")
        self.widgets["actionLabel"].grid(row=19, column=1, columnspan=2)
        self.widgets["refreshButton"] = factory.getButton(self.widgets["mChoiceFrame"], "Odśwież wykres", command=self.refreshGui)
        self.widgets["refreshButton"].grid(row=20, column=1, columnspan=2, sticky="ew")
        self.widgets["emptyLabel2"] = factory.getLabel(self.widgets["mChoiceFrame"], "")
        self.widgets["emptyLabel2"].grid(row=21, column=1, columnspan=2)
        self.widgets["separator4"] = factory.getSeparator(self.widgets["mChoiceFrame"])
        self.widgets["separator4"].grid(row=22, column=1, columnspan=2, sticky="ew")

        # Panel informacji o wybranych firmach
        self.widgets["infoLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "Informacje o wybranych firmach")
        self.widgets["infoLabel"].grid(row=23, column=1, columnspan=2)
        self.widgets["aboutLabel"] = factory.getLabel(self.widgets["mChoiceFrame"], "")
        self.widgets["aboutLabel"].config(justify=LEFT, textvariable=parameters.DataFlag_About)
        self.widgets["aboutLabel"].grid(row=24, column=1, columnspan=2)

        # Dodawanie okienka wykresów
        self.widgets["chartFrame"] = factory.getFrame(self)
        self.widgets["chartFrame"].pack(side=RIGHT, fill=BOTH, expand=YES)
        # self.widgets["chartFrame"].config(borderwidth=2)
        self.widgets["chart1"] = PlotObject(self.widgets["chartFrame"], 1)
        newF = plt.figure(num=self.pltIndex, dpi=100)
        self.pltIndex += 1
        plt.plot([], [])
        plt.title('Dane giełdowe')
        self.widgets["chart1"].replace_plot(newF)
        plt.close()


    def refreshGui(self):
        """
        Funkcja rysująca nowy wykres na podstawie załadowanych danych
        """
        # Pobieranie informacji o wybranym zakresie czasu i ich konwersja na format int
        DateRange = [parameters.DataFlag_StartTime.get(), parameters.DataFlag_EndTime.get()]
        DateRange = [DataLoader.StrDateToInt(i) for i in DateRange]

        # Pobieranie informacji o wybranych polach
        selected_params = []
        if parameters.DataFlag_Open.get() == 1:
            selected_params.append("Open")
        if parameters.DataFlag_High.get() == 1:
            selected_params.append("High")
        if parameters.DataFlag_Low.get() == 1:
            selected_params.append("Low")
        if parameters.DataFlag_Close.get() == 1:
            selected_params.append("Close")
        if parameters.DataFlag_Volume.get() == 1:
            selected_params = ["Volume"]
            parameters.DataFlag_Open.set(0)
            parameters.DataFlag_High.set(0)
            parameters.DataFlag_Low.set(0)
            parameters.DataFlag_Close.set(0)

        # Pobieranie informacji o wybranych firmach
        selected_companies = []
        if parameters.DataFlag_Company1.get() != "brak":
            selected_companies.append(parameters.DataFlag_Company1.get())
        if parameters.DataFlag_Company2.get() != "brak":
            selected_companies.append(parameters.DataFlag_Company2.get())
        
        # Ustawianie informacji o firmach
        if len(selected_companies) == 0: # Nie wybrano żadnej firmy
            parameters.DataFlag_About.set("Nie wybrano firmy")
        else:
            about_new_text = ""
            CompaniesInfo = DataLoader.GetCompaniesInfo(selected_companies)
            for i in CompaniesInfo.keys():
                about_new_text += CompaniesInfo[i] + "\n"
            parameters.DataFlag_About.set(about_new_text)
        
        # Pobieranie informacji do wykresu
        data = DataLoader.GetData(selected_companies, selected_params, DateRange)

        # Tworzenie nowego wykresu
        newPlot = plt.figure(self.pltIndex, dpi=100)
        self.pltIndex += 1
        legenda = []
        for i in data.keys():
            plt.plot(data[i][0], data[i][1])
            legenda.append(i)
        plt.title('Dane Giełdowe')
        plt.legend(legenda)
        plt.grid(True)
        # Pushowanie wykresu
        self.widgets["chart1"].replace_plot(newPlot)



    def showInfoAboutProgram(self):
        """
        Funkcja wyświetla informacje o programie
        """

        info = """
        Autorzy: Jan Sawicki, Agata Swatowska, Mateusz Sołtys
        Wersja: 2.0
        Użyto:
        - python 3.9(conda)
        - tkinter
        - numpy
        - matplotlib
        - sqlalchemy
        """
        popup = factory.getToplevel(factory.getWidget("root"))
        popup.title("O programie")
        txt = factory.getText(popup)
        txt.insert(END, info)
        txt.pack(fill=BOTH, expand=YES)