import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from WyciaganieDanych import leagueTable

class OknoLigowe:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("1250x750")
        self.glowneOkno = glowneOkno
        self.sortingDirection = 1
        self.windowView()
        
    def windowView(self):
        self.przyciskCofania = customtkinter.CTkButton(master=self.root, text="Powrót do menu", command=self.przyciskCofania)

        self.root.grid_anchor('center')
        self.przyciskCofania.grid(row=2, column=2, pady=30)
        
        data = pd.read_csv('./Scraper/PL_23_24_MatchStats.csv', delimiter=';')
        dataLeagueTable = leagueTable(data, 'PremierLeague', '23_24')
        dataResultsTable = data[['homeTeam', 'awayTeam', 'homeGoals', 'awayGoals']]

        self.createLeagueTable(self.root, dataLeagueTable)
        self.createResultsTable(self.root, dataResultsTable)


    def przyciskCofania(self):
        print("Cofanie")
        self.glowneOkno.setView("menuStartowe")
    
    def createLeagueTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        self.tableLeague = ttk.Treeview(root)
        self.tableLeague["columns"] = list(data.columns)
        self.tableLeague["show"] = "headings"
        self.tableLeague.grid(row=0, column=3, pady=5)
        self.tableLeague["height"] = 20
        
        for column in self.tableLeague["columns"]:
            self.tableLeague.column(column, anchor="center", width=100)
        
        for col in data.columns:
            self.tableLeague.heading(col, text=col, command=lambda c=col: self.sortTable(c, self.tableLeague, data))

        self.tableLeague = self.wypelnijTabele(self.tableLeague, data)
        self.tableLeague.bind("<ButtonRelease-1>", lambda event: self.showValue(event))
        
    def createResultsTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        self.tableResults = ttk.Treeview(root)
        self.tableResults["columns"] = list(data.columns)
        self.tableResults["show"] = "headings"
        self.tableResults.grid(row=0, column=1, pady=5)
        self.tableResults["height"] = 20
        
        for column in self.tableResults["columns"]:
            self.tableResults.column(column, anchor="center", width=100)
        
        for col in data.columns:
            self.tableResults.heading(col, text=col, command=lambda c=col: self.sortTable(c, self.tableResults, data))

        self.tableResults = self.wypelnijTabele(self.tableResults, data)
        self.tableResults.bind("<ButtonRelease-1>", lambda event: self.showValue(event))


    def showValue(self, event):
        if self.table.identify_region(event.x, event.y) == 'cell':
            selected_row = self.table.selection()[0]
            column = self.table.identify_column(event.x)  # Znajdowanie kolumny na którą kliknięto
            column = int(column.lstrip('#')) - 1  # Konwersja numeru kolumny do indeksu (indeksowane od 0)
            value = self.table.item(selected_row)['values'][column]
            print(f"Wartość klikniętego pola: {value}")

    def sortTable(self, column, table, data):
        print(f"Sortowanie tabeli po kolumnie: {column}")
        if self.sortingDirection:
            data = data.sort_values(by=column, ascending=False)
            self.sortingDirection = 0
        else:
            data = data.sort_values(by=column, ascending=True)
            self.sortingDirection = 1
            
        self.wypelnijTabele(table, data)
    
    def clearTable(self, table):
        for item in table.get_children():
            table.delete(item)
    
    def wypelnijTabele(self, table, data):
        self.clearTable(table)
        for i, row in data.iterrows():
            if i % 2 == 1:
                table.insert("", "end", values=list(row))
            else:
                table.insert("", "end", values=list(row))
    
        return table