import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from OknoStartowe import OknoStartowe
from OknoLigowe import OknoLigowe
from OknoWyszukajDruzyne import OknoWyszukajDruzyne
from OknoDruzyny import OknoDruzyny
from OknoWyszukajZawodnika import OknoWyszukajZawodnika
from OknoWyszukajSedziego import OknoWyszukajSedziego
from OknoZawodnika import OknoZawodnika
from OknoSedziego import OknoSedziego
from OknoMeczu import OknoMeczu


class Okno:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x750")
        self.root.bind("<Key>", self.previousView)
        self.dataMatchStats = pd.read_csv('./Scraper/MatchStats.csv', delimiter=';')
        self.futureData = pd.read_csv('./Scraper/FutureMatches.csv', delimiter=';')
        self.playerStatsData = pd.read_csv('./Scraper/AllPlayerStats.csv', delimiter=';')
        self.matchSquadsData = pd.read_csv('./Scraper/MatchSquads.csv', delimiter=';')
        self.matchEventsData = pd.read_csv('./Scraper/MatchEvents.csv', delimiter=';')
        self.viewHistory = [('menuStartowe', None)]
        self.aktywneOkno = OknoStartowe(self.root, self)
        self.sortingDirection = 0
        self.defaultSeason = '23_24'
        
    
    def clearFrame(self):
       for widgets in self.root.winfo_children():
          widgets.destroy()
          
          
    def setView(self, view, pom=None):
        self.clearFrame()
        self.viewHistory.append((view, pom))
        
        if view == "ligowe":
            self.aktywneOkno = OknoLigowe(self.root, self, pom)
        elif view == "menuStartowe":
            self.aktywneOkno = OknoStartowe(self.root, self)
        elif view == "searchTeam":
            self.aktywneOkno = OknoWyszukajDruzyne(self.root, self)
        elif view == "teamStats":
            self.aktywneOkno = OknoDruzyny(self.root, self, pom)
        elif view == "searchPlayer":
            self.aktywneOkno = OknoWyszukajZawodnika(self.root, self)
        elif view == "searchReferee":
            self.aktywneOkno = OknoWyszukajSedziego(self.root, self)
        elif view == "playerDetails":
            self.aktywneOkno = OknoZawodnika(self.root, self, pom)
        elif view == "refereeDetails":
            self.aktywneOkno = OknoSedziego(self.root, self, pom)
        elif view == "teamDetails":
            self.aktywneOkno = OknoMeczu(self.root, self, pom)
        elif view == "matchDetails":
            self.aktywneOkno = OknoMeczu(self.root, self, pom)
            
    def setPreviousView(self, view, pom=None):
        self.clearFrame()
        del self.aktywneOkno
        
        if view == "ligowe":
            self.aktywneOkno = OknoLigowe(self.root, self, pom)
        elif view == "menuStartowe":
            self.aktywneOkno = OknoStartowe(self.root, self)
        elif view == "searchTeam":
            self.aktywneOkno = OknoWyszukajDruzyne(self.root, self)
        elif view == "teamStats":
            self.aktywneOkno = OknoDruzyny(self.root, self, pom)
        elif view == "searchPlayer":
            self.aktywneOkno = OknoWyszukajZawodnika(self.root, self)
        elif view == "searchReferee":
            self.aktywneOkno = OknoWyszukajSedziego(self.root, self)
        elif view == "playerDetails":
            self.aktywneOkno = OknoZawodnika(self.root, self, pom)
        elif view == "refereeDetails":
            self.aktywneOkno = OknoSedziego(self.root, self, pom)
        elif view == "teamDetails":
            self.aktywneOkno = OknoMeczu(self.root, self, pom)
        elif view == "matchDetails":
            self.aktywneOkno = OknoMeczu(self.root, self, pom)
            
    def previousView(self, event):
        if event.keysym == 'x':
            if(len(self.viewHistory) == 1):
                self.setPreviousView('menuStartowe')
            else:
                view, pom = self.viewHistory.pop(len(self.viewHistory) - 1)
                view, pom = self.viewHistory[len(self.viewHistory) - 1]
                self.setPreviousView(view, pom)

    def przyciskPreviousView(self):
        if(len(self.viewHistory) == 1):
            self.setPreviousView('menuStartowe')
        else:
            view, pom = self.viewHistory.pop(len(self.viewHistory) - 1)
            view, pom = self.viewHistory[len(self.viewHistory) - 1]
            self.setPreviousView(view, pom)
      
    def przyciskCofania(self):
        self.setView("menuStartowe")
        
    def wypelnijTabele(self, table, data):
        self.clearTable(table)
        for i, row in data.iterrows():
            table.insert("", "end", values=list(row))
        return table
    
    def clearTable(self, table):
        for item in table.get_children():
            table.delete(item)
            
    def showValue(self, event, table):
        if table.identify_region(event.x, event.y) == 'cell':
            if table.selection():
                selected_row = table.selection()[0]
                column = table.identify_column(event.x)  # Znajdowanie kolumny na którą kliknięto
                column = int(column.lstrip('#')) - 1  # Konwersja numeru kolumny do indeksu (indeksowane od 0)
                
                value = table.item(selected_row)['values'][column]
                if value != '':
                    print(f"Wartość klikniętego pola: {value}")
                    columnName = table.heading(column)['text']
                    if columnName in ['Gospodarz', 'Przyjezdny', 'Drużyna']:
                        self.setView("teamStats", value)
                    if columnName in ['League', 'Liga', 'league']:
                        self.setView("ligowe", value)
                    if columnName in ["Zawodnik", "Gracz 1", "Gracz 2"]:
                        self.setView("playerDetails", value)   
                    if columnName in ["Sędzia", 'referee']:
                        self.setView("refereeDetails", value)  
                    if columnName in ["Wynik", "Data"]:
                        # indeksy kolumn w tabeli
                        indexColumnDate = table['columns'].index('Data')
                        indexColumnHomeTeam = table['columns'].index('Gospodarz')
                        indexColumnAwayTeam = table['columns'].index('Przyjezdny')
                        value = [table.item(selected_row)['values'][indexColumnDate], # data
                                 table.item(selected_row)['values'][indexColumnHomeTeam], # home team
                                 table.item(selected_row)['values'][indexColumnAwayTeam]] # away team
                        self.setView("matchDetails", value)  
            
                
    def sortTable(self, column, table, data):
        print(f"Sortowanie tabeli po kolumnie: {column}")
        if self.sortingDirection:
            data = data.sort_values(by=column, ascending=False)
            self.sortingDirection = 0
        else:
            data = data.sort_values(by=column, ascending=True)
            self.sortingDirection = 1
            
        self.wypelnijTabele(table, data)
        
        
    def updateData(self):
        print("test")
        
        
        
        
    
