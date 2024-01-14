import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from WyciaganieDanych import allTeamsTable, listLeagues

class OknoWyszukajDruzyne:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("1250x750")
        self.glowneOkno = glowneOkno
        self.windowView()
        
    def windowView(self):
        
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=0)
        
        buttonFrame = customtkinter.CTkFrame(self.root, height=700, fg_color="transparent")
        buttonFrame.grid(row=2, column=0, sticky='n')
        
        emptyFrame = customtkinter.CTkFrame(self.root, height=200, bg_color="transparent", fg_color="transparent")
        emptyFrame.grid(row=1, column=0, sticky='n')
        
        self.przyciskCofania = customtkinter.CTkButton(master=buttonFrame, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)
        self.root.grid_anchor('n')
        buttonFrame.grid_anchor('center')
        self.przyciskCofania.grid(row=0, column=0, pady=5, sticky='n')
        
        self.data = self.glowneOkno.dataMatchStats
        self.dataTeamTable = allTeamsTable(self.data)
        self.displayedData = self.dataTeamTable
        frame = self.createTeamTable(self.root, self.displayedData)
        frame.grid(row=2, column=1, pady=5, padx=10, sticky='n')

        labelTeamName = customtkinter.CTkLabel(buttonFrame, text="Nazwa drużyny:")
        labelTeamName.grid(row=1, column=0, pady=5, sticky='n')
        self.entryTeamName = customtkinter.CTkEntry(buttonFrame)
        self.entryTeamName.grid(row=2, column=0, pady=5, sticky='n')
        self.entryTeamName.bind('<KeyRelease>', self.updateResults)
        
        # combo box do ligi
        labelLeagueName = customtkinter.CTkLabel(buttonFrame, text="Nazwa ligi:")
        labelLeagueName.grid(row=3, column=0, pady=5, sticky='n')
        optionsLeague = listLeagues(self.glowneOkno.dataMatchStats)
        optionsLeague =  ('',) + optionsLeague
        self.leagueList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsLeague, command=self.selectLeague)
        self.leagueList.grid(row=4, column=0, pady=5, sticky='n')
        #self.leagueList.bind("<<ComboboxSelected>>", self.selectLeague)  
        

    def selectLeague(self, event=None):
        leagueName = self.leagueList.get()
        if leagueName != '':
            self.displayedData = self.dataTeamTable[self.dataTeamTable['Liga'] == leagueName]
        else:
            self.displayedData = self.dataTeamTable
        searchName = self.entryTeamName.get()
        self.displayedData = self.displayedData[self.displayedData['Drużyna'].str.contains(searchName, case=False)]
        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, self.displayedData)
        self.tableLeague["height"] = min(self.displayedData.shape[0], 20)

    def updateResults(self, event=None):
        searchName = self.entryTeamName.get()
        self.displayedData = self.dataTeamTable[self.dataTeamTable['Drużyna'].str.contains(searchName, case=False)]
        leagueName = self.leagueList.get()
        if leagueName != '':
            self.displayedData = self.displayedData[self.displayedData['Liga'] == leagueName]
        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, self.displayedData)
        self.tableLeague["height"] = min(self.displayedData.shape[0], 20)
        
        
    def createTeamTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
                
        
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tableLeague = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        self.tableLeague.pack(side=tk.LEFT, fill=tk.Y)
        self.tableLeague["columns"] = list(data.columns)
        self.tableLeague["show"] = "headings"
        self.tableLeague["height"] = min(data.shape[0], 20)
        
        y_scrollbar.config(command=self.tableLeague.yview)
        
        for column in self.tableLeague["columns"]:
            self.tableLeague.column(column, anchor="center", width=200)
        
        for col in data.columns:
            self.tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, self.tableLeague, data))

        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, data)
        self.tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, self.tableLeague))
        
        return frame
        

        

        


        