import tkinter as tk

DataFlag_Open = None
DataFlag_High = None
DataFlag_Low = None
DataFlag_Close = None
DataFlag_Volume = None

DataFlag_StartTime = None
DataFlag_EndTime = None
DataFlag_Company1 = None
DataFlag_Company2 = None

DataFlag_About = None

def InitVariables():
    """
    Funkcja inicjalizująca kontenery zmiennych tk po wstępnej inicjalizacji okna głównego MainWindow.
    Wywoływana w konstruktorze MainWindow.
    """
    global DataFlag_Open, DataFlag_High, DataFlag_Low, DataFlag_Close, DataFlag_Volume, DataFlag_StartTime, DataFlag_EndTime, DataFlag_Company1, DataFlag_Company2, DataFlag_About
    DataFlag_Open = tk.IntVar()
    DataFlag_High = tk.IntVar()
    DataFlag_Low = tk.IntVar()
    DataFlag_Close = tk.IntVar()
    DataFlag_Volume = tk.IntVar()
    DataFlag_StartTime = tk.StringVar()
    DataFlag_EndTime = tk.StringVar()
    DataFlag_Company1 = tk.StringVar()
    DataFlag_Company2 = tk.StringVar()
    DataFlag_About = tk.StringVar()