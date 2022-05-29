"""
Plik zawiera funkcje i klasy pozwalające na komunikowanie się z bazą danych
"""
from datetime import datetime

import sqlalchemy as sql
from sqlalchemy import create_engine, select, MetaData, Table
from sqlalchemy import Column, Text, Integer, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Zmienne globalne
dbName = "StockData.db"

# Nawiązywanie połączenia z bazą
db_string = 'sqlite:///' + dbName
engine = create_engine(db_string)
metadata = MetaData()
insp = sql.inspect(engine)

session = (sessionmaker(bind=engine))()
Base = declarative_base()

# Pobieranie listy tablic
insp = sql.inspect(engine)
print("Nawiązano połączenie z bazą danych")
print("Lista tablic:", insp.get_table_names())


def IntDateToStr(IntDate):
    """
    Funkcja konwertuje date w formacie int YYYYMMDD(format używany w bazie danych) na datę w formacie str 'YYYY-MM-DD'.
    Args:
        IntDate (int): Data w formacie liczbowym int YYYYMMDD
    Returns:
        (str): Data w formacie string 'YYYY-MM-DD'
    """
    return str(IntDate)[:4] + '-' + str(IntDate)[4:6] + '-' + str(IntDate)[6:]


def StrDateToInt(StrDate):
    """
    Funkcja konwertuje date w formacie str 'YYYY-MM-DD' na datę w formacie int YYYYMMDD(format używany w bazie danych).
    Args:
        StrDate (str): Data w formacie string 'YYYY-MM-DD'
    Returns:
        (int): Data w formacie liczbowym int YYYYMMDD lub data 11111111 jeżeli ciąg był niepoprawny
    """
    StrDate = StrDate.replace('-', '')
    if StrDate.isdecimal():
        return int(StrDate)
    else:
        return 11111111


# Tworzenie klas danych
class Companies(Base):
    __tablename__ = 'Companies'
    CompanyID = Column(Integer, primary_key=True)
    CompanyName = Column(Text)
    CompanyType = Column(Text)
    CompanyDate = Column(Integer)

    def __str__(self):
        CompanyInfo = self.CompanyName + " " + self.CompanyType + ", zołożono: " + IntDateToStr(self.CompanyDate)
        return CompanyInfo


class Records(Base):
    __tablename__ = 'Records'
    RecordID = Column(Integer, primary_key=True)
    CompanyID = Column(Integer, ForeignKey('Companies.CompanyID'))
    Date = Column(Integer)
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(Integer)


def GetCompaniesList():
    """
    Funkcja zwraca listę nazw wszystkich firm występujących w bazie danych.
    Returns:
        ( list[string] ): Lista nazw firm
    """
    mapper_task = select(Companies.CompanyName)
    mapper_results = engine.execute(mapper_task).fetchall()
    return [mapper_results[i][0] for i in range(len(mapper_results))]


def GetCompaniesInfo(CompaniesList=[]):
    """
    Funkcja zwraca listę skrótu informacji o firmach
    Args:
        CompaniesList ( list[str] ): Lista firm do załądowania
    Returns:
        ( dic[str, str] ): Słownik informacji o firmie. Format klucza to "firma"
    """
    result = {}
    for company in CompaniesList:
        info = session.query(Companies).filter_by(CompanyName=company).all()[0].__str__()
        result[company] = info
    return result


def GetData(CompaniesList=[], FieldsList=[], DateRange=[20220101, 20220407]):
    """
    Funkcja zwraca listę obiektów Records przefiltrowaną względem pól i zakresu daty
    Args:
        CompaniesList ( list[str] ): Lista firm do załądowania
        FieldsList ( list[str] ): Lista pól do załadowania z podanych firm
        DateRange ( list[int, int] ): Zakres dat w formacie YYYYMMDD
    Returns:
        ( dic[str, (float, float)] ): Słownik danych do splotowania. Format klucza to "firma:pole"
    """
    result = {}
    for company in CompaniesList:
        # Pozyskiwanie ID firmy
        id = session.query(Companies).filter_by(CompanyName=company).all()[0].CompanyID
        companydata = session.query(Records) \
            .filter_by(CompanyID=id) \
            .filter(Records.Date > DateRange[0]) \
            .filter(Records.Date < DateRange[1]) \
            .all()
        # Pozyskiwanie elementów
        if "Open" in FieldsList:
            datX = [DateConverter(companydata[i].Date) for i in range(len(companydata))]
            datY = [companydata[i].Open for i in range(len(companydata))]
            result[company + ":Open [PLN]"] = (datX, datY)
        if "High" in FieldsList:
            datX = [DateConverter(companydata[i].Date) for i in range(len(companydata))]
            datY = [companydata[i].High for i in range(len(companydata))]
            result[company + ":High [PLN]"] = (datX, datY)
        if "Low" in FieldsList:
            datX = [DateConverter(companydata[i].Date) for i in range(len(companydata))]
            datY = [companydata[i].Low for i in range(len(companydata))]
            result[company + ":Low [PLN]"] = (datX, datY)
        if "Close" in FieldsList:
            datX = [DateConverter(companydata[i].Date) for i in range(len(companydata))]
            datY = [companydata[i].Close for i in range(len(companydata))]
            result[company + ":Close [PLN]"] = (datX, datY)
        if "Volume" in FieldsList:
            datX = [DateConverter(companydata[i].Date) for i in range(len(companydata))]
            datY = [companydata[i].Volume for i in range(len(companydata))]
            result[company + ":Volume [Ilość]"] = (datX, datY)
    return result


def DateConverter(date):
    date_str = IntDateToStr(date)
    return datetime.strptime(date_str, "%Y-%m-%d")
