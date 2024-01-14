import asyncio
import nest_asyncio
nest_asyncio.apply()
import threading
import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter
from Okno import Okno
from WyciaganieDanych import updateMatches, checkUpdateStatus

async def async_function(par1):
    print("Rozpoczęcie aktualizacji danych")
    data = pd.read_csv('./Scraper/MatchStats.csv', delimiter=';')
    dataFuture = pd.read_csv('./Scraper/FutureMatches.csv', delimiter=';')
    season = par1.okno.defaultSeason
    
    print(par1.okno.defaultSeason)
    for league in ['SerieA', 'PremierLeague', 'LaLiga', 'SerieA', 'Ligue1']:
        print(league)
        dataToUpdate = checkUpdateStatus(data, dataFuture, league, season)
        updateMatches(dataToUpdate, league)
    
    par1.okno.dataMatchStats = pd.read_csv('./Scraper/MatchStats.csv', delimiter=';')
    par1.okno.futureData = pd.read_csv('./Scraper/FutureMatches.csv', delimiter=';')
    par1.okno.playerStatsData = pd.read_csv('./Scraper/AllPlayerStats.csv', delimiter=';')
    par1.okno.matchSquadsData = pd.read_csv('./Scraper/MatchSquads.csv', delimiter=';')
    par1.okno.matchEventsData = pd.read_csv('./Scraper/MatchEvents.csv', delimiter=';')
    print("Zakończenie aktualizacji danych")
    
    return 0

def run_async_function(par1):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_function(par1))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Football stats")
        self.center_window()
        self.futureData = pd.read_csv('./Scraper/FutureMatches.csv', delimiter=';')
        self.playerStatsData = pd.read_csv('./Scraper/AllPlayerStats.csv', delimiter=';')
        self.matchSquadsData = pd.read_csv('./Scraper/MatchSquads.csv', delimiter=';')
        self.matchEventsData = pd.read_csv('./Scraper/MatchEvents.csv', delimiter=';')
        self.okno = Okno(self)

        # Uruchomienie funkcji asynchronicznej w osobnym wątku
        self.thread = threading.Thread(target=run_async_function, args=(self,))
        self.thread.start()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (1250 // 2)
        y = (screen_height // 2) - (750 // 2)

        self.geometry(f'1250x750+{x}+{y}')
        


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = App()
app.mainloop()
