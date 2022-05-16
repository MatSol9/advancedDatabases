# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:11:25 2022

@author: Jasio
"""

from MainWindow import MainWindow
from tkfactory.TkFactory import TkFactory

# Inicjowanie fabryki abstrakcyjnej
factory = TkFactory.getFactory()

# Tworzenie głównego okna
root = MainWindow()
factory.addExternalWidget(root, "root")

# Ustawianie ikony i nazwy programu
# root.iconbitmap('databasefolder/programicon.ico')
root.title("Przeglądarka danych giełdowych")

# Uruchamianie programu
root.mainloop()