import pandas as pd
from Scraper import collectMatch

def changeColumnNames(data):
    dictonary = {
        'homeTeam': 'Gospodarz', 
        'awayTeam': 'Przyjezdny', 
        'date': "Data",
        'league': "Liga",
        'season': "Sezon",
        'player': "Zawodnik",
        'team': "Drużyna",
        'goals': 'Gole',
        'assists': 'Asysty',
        'minutes': 'Minuty',
        'cards_yellow': 'Żółte',
        'cards_red': 'Czerwone',
        'fouls': 'Faule',
        'fouled': 'Sfaulowany',
        'age': "Wiek",
        'nationality': 'Narodowość',
        'position': 'Pozycja',
        'matchweek': 'Kolejka',
        'hour': 'Godzina',
        'referee': 'Sędzia',
        'minute': 'Minuta',
        'status': 'Status',
        'eventType': 'Zdarzenie',
        'playerOne': 'Gracz 1',
        'playerTwo': 'Gracz 2',
        'shots': 'Strzały',
        'passes': 'Podania',
        'homePossession': 'Posiadanie gospodarz',
        'awayPossession': 'Posiadanie przyjezdny',
        'homeShotsonTarget': 'Celnosć strzałów gospodarz',
        'awayShotsonTarget': 'Celnosć strzałów przyjezdny',
        'homeCorners': 'Rożne gospodarz',
        'awayCorners': 'Rożne przyjezdny',
        'homeFouls': 'Faule gospodarz',
        'awayFouls': 'Faule przyjezdny',
        'homeYellowCards': "Żółte kartki gospodarz",
        'awayYellowCards': "Żółte kartki przyjezdny",
        'homeRedCards': "Czerwone kartki gospodarz",
        'awayRedCards': "Czerwone kartki przyjezdny",
        
        }
    data.rename(columns=dictonary, inplace=True)

def allTeamsTable(data):
    import pandas as pd
    
    homeTeamData = data[['homeTeam', 'league']].rename(columns={'homeTeam': 'Drużyna'})
    awayTeamData = data[['awayTeam', 'league']].rename(columns={'awayTeam': 'Drużyna'})
    allData = pd.concat([homeTeamData, awayTeamData])
    allData = allData.drop_duplicates().reset_index(drop=True)
    changeColumnNames(allData)
    return allData


def teamMatches(data, season, team):
    data = data.loc[data['season'] == season]
    homeData = data.loc[data['homeTeam'] == team]
    awayData = data.loc[data['awayTeam'] == team]
    data = pd.concat([homeData, awayData])
    
    data = data.sort_values(['date'])
    data.reset_index(inplace=True)
    
    data['Wynik'] = data['homeGoals'].astype(str) + ':' + data['awayGoals'].astype(str)
    
    columns = ['date', 'matchweek', 'homeTeam', 'awayTeam', 'Wynik', 'referee', 'homePossession', 'awayPossession', 'homeShotsonTarget',
               'awayShotsonTarget', 'homeCorners', 'awayCorners', 'homeFouls', 'awayFouls']
    
    ['Liga', 'Sezon', 'homePossession', 'awayPossession', 'homePassingAccuracy',
       'awayPassingAccuracy', 'homeShotsonTarget', 'awayShotsonTarget',
       'homeSaves', 'awaySaves', 'homeFouls', 'awayFouls', 'homeCorners',
       'awayCorners', 'homeCrosses', 'awayCrosses', 'homeTouches',
       'awayTouches', 'homeTackles', 'awayTackles', 'homeInterceptions',
       'awayInterceptions', 'homeAerialsWon', 'awayAerialsWon',
       'homeClearances', 'awayClearances', 'homeOffsides', 'awayOffsides',
       'homeGoalKicks', 'awayGoalKicks', 'homeThrowIns', 'awayThrowIns',
       'homeLongBalls', 'awayLongBalls']
    
    data = data[columns]
    changeColumnNames(data)
    
    return data

def leagueMatches(data, season, league):
    data = data.loc[(data['season'] == season) & (data['league'] == league)]
    
    data = data.sort_values(['date'])
    data['Wynik'] = data['homeGoals'].astype(str) + ':' + data['awayGoals'].astype(str)
    data.reset_index(inplace=True)
    changeColumnNames(data)

    return data

def matchSquads(data, season, league, homeTeam, awayTeam):
    data = data.loc[data['league'] == league]
    data = data.loc[data['season'] == season]
    data = data.loc[data['homeTeam'] == homeTeam]
    data = data.loc[data['awayTeam'] == awayTeam]
    
    return data

def leaguePlayers(data, season, league):
    data = data.loc[data['league'] == league]
    data = data.loc[data['season'] == season]
        
    groupedData = data.groupby(['player', 'playerTeam']).agg({
        'player': 'count',
        'minutes': 'sum',
        'goals': 'sum',
        'assists': 'sum',
        'cards_red': 'sum',
        'cards_yellow': 'sum'
    })

    return groupedData


    
def H2HMatches(data, teamOne, teamTwo):
    data = data.loc[(data['homeTeam'] == teamOne) & (data['awayTeam'] == teamTwo)]
    data = data.loc[(data['homeTeam'] == teamTwo) & (data['awayTeam'] == teamOne)]
    
    data = data.sort_values(['date'])
    data.reset_index(inplace=True)
    changeColumnNames(data)
    
    return data

def filterPlayers(data, season, nationality, league, club, position):
    data = data[data['season'] == season]
    if nationality:
        data = data[data['nationality'] == nationality]
    if league:
        data = data[data['league'] == league]
    if club:
        data = data[data['club'] == club]
    if position:
        data = data[data['position'] == position]
    
    groupedData = data.groupby(['player', 'playerTeam']).agg({
        'player': 'count',
        'minutes': 'sum',
        'goals': 'sum',
        'assists': 'sum',
        'cards_red': 'sum',
        'cards_yellow': 'sum'
    })

    return groupedData


def listLeagues(data):
    return tuple(data['league'].unique())

def listSeasons(data, league):
    data = data[data['league'] == league]
    return sorted(tuple(data['season'].unique()), reverse=True)

def listAllSeasons(data):
    return sorted(tuple(data['season'].unique()), reverse=True)

def leagueTable(data, league, season):
    data = data.loc[data['season'] == season]
    data = data.loc[data['league'] == league]

    win_mask = data['homeGoals'] > data['awayGoals']
    lose_mask = data['homeGoals'] < data['awayGoals']
    draw_mask = data['homeGoals'] == data['awayGoals']
    
    data[['homeWin', 'homeLose', 'homeDraw', 'awayWin', 'awayLose', 'awayDraw']] = 0

    data.loc[data.loc[win_mask, 'homeTeam'].index, 'homeWin'] += 1
    data.loc[data.loc[lose_mask, 'homeTeam'].index, 'homeLose'] += 1
    data.loc[data.loc[draw_mask, 'homeTeam'].index, 'homeDraw'] += 1
    
    data.loc[data.loc[win_mask, 'awayTeam'].index, 'awayLose'] += 1
    data.loc[data.loc[lose_mask, 'awayTeam'].index, 'awayWin'] += 1
    data.loc[data.loc[draw_mask, 'awayTeam'].index, 'awayDraw'] += 1 

    homeStats = data.groupby('homeTeam').agg({
        'homeTeam': 'count',
        'homeGoals': 'sum',
        'awayGoals': 'sum',
        'homeWin': 'sum',
        'homeLose': 'sum',
        'homeDraw': 'sum',
    })
    homeStats.columns = ['Zagrane', 'Strzelone', 'Stracone', 'Wygrane', 'Przegrane', 'Remisy']
    
    awayStats = data.groupby('awayTeam').agg({
        'awayTeam': 'count',
        'awayGoals': 'sum',
        'homeGoals': 'sum',
        'awayWin': 'sum',
        'awayLose': 'sum',
        'awayDraw': 'sum',
    })
    awayStats.columns = ['Zagrane', 'Strzelone', 'Stracone', 'Wygrane', 'Przegrane', 'Remisy']
    
    teamStats = homeStats.add(awayStats)
    teamStats.reset_index(inplace=True)
    teamStats.rename(columns={'homeTeam': 'Drużyna'}, inplace=True)
    
    teamStats['Punkty'] = teamStats['Wygrane']*3 + teamStats['Remisy']
    teamStats.sort_values(by=['Punkty'], inplace=True, ascending=False)

    
    return teamStats


def futureMatches(data, league, season):
    data = data[data['league'] == league]
    data = data[data['season'] == season]

    columns = ['date', 'homeTeam', 'awayTeam']
    data = data[columns]
    changeTeamNames(data)
    
    from datetime import datetime
    current_date = datetime.now().date()
    data = data.copy()
    data['date'] = pd.to_datetime(data['date'])
    
    current_date_datetime64 = pd.to_datetime(current_date)
    data = data[data['date'] >= current_date_datetime64]
    
    data['date'] = data['date'].astype(str)
    
    changeColumnNames(data)
    return data

def leaguePlayersStats(data, league, season):
    data = data[data['league'] == league]
    data = data[data['season'] == season]
    
    playerStats = data.groupby(['player', 'team']).agg({
    'goals': 'sum',
    'assists': 'sum',
    'minutes': 'sum',
    'cards_yellow': 'sum',
    'cards_red': 'sum',
    'homeTeam': 'count',
    })
    playerStats.rename(columns={'homeTeam': "Mecze"}, inplace=True)
    playerStats.reset_index(inplace=True)
    changeColumnNames(playerStats)
    
    return playerStats



def listPositions(data):
    data = data['position']
    data = data.apply(lambda text: text[:2])
    return tuple(data.unique())


def listReferee(data):
    
    refereeList = data.groupby('referee').agg({
        'date': 'count',
        'homeFouls': 'mean',
        'awayFouls': 'mean',
        'homeCorners': 'mean',
        'awayCorners': 'mean'
        })
    
    refereeList = refereeList.round(2)
    refereeList.rename(columns={'date': "Mecze",
                                'homeFouls': 'Średnio faule gospodarzy',
                                'awayFouls': 'Średnio faule przyjezdnych',
                                'homeCorners': 'Średnio rożne gospodarzy',
                                'awayCorners': 'Średnio rożne przyjezdnych'
                                }, inplace=True)
    refereeList.reset_index(inplace=True)
    changeColumnNames(refereeList)
    
    return refereeList




def listPlayerSeasons(data, player):
    data = data[data['player'] == player]
    return sorted(tuple(data['season'].unique()), reverse=True)

def playerFutureMatches(data, dataFuture, player):
    data = data[data['player'] == player]
    
    if not data.empty:
        lastMatchDate = max(data['date'])
        team = data[data['date'] == lastMatchDate]
        team = team['team']
        team = team.iloc[0]
    
        columns = ['player', 'date', 'homeTeam', 'awayTeam']
        data = data[columns]
        
        matches = dataFuture[(dataFuture['homeTeam'] == team) | (dataFuture['awayTeam'] == team)]
        
        from datetime import datetime
        current_date = datetime.now().date()
        matches = matches.copy()
        matches['date'] = pd.to_datetime(matches['date'])
        
        current_date_datetime64 = pd.to_datetime(current_date)
        matches = matches[matches['date'] >= current_date_datetime64]
        matches['date'] = matches['date'].astype(str)

    else:
        columns = ['player', 'date', 'homeTeam', 'awayTeam']
        matches = pd.DataFrame(columns=columns)
        
    changeColumnNames(matches)
    return matches

def playerOverallStats(data, player, season):
    data = data[data['player'] == player]
    data = data[data['season'] == season]
    
    if data.shape[0] > 0:
        age = max(data['age'])
        shirtnumber = max(data['shirtnumber'])
        nationality = max(data['nationality'])
        goals = sum(data['goals'])
        assists = sum(data['assists'])
        team = data['team'].iloc[-1]
        
        dataStats = pd.DataFrame({
            'player': [player], 
            'age': [age],
            'shirtnumber': [shirtnumber],
            'nationality': [nationality],
            'goals': [goals],
            'assists': [assists],
            'team': [team]
            })
    
        changeCountryNames(dataStats)
        changeColumnNames(dataStats)
        
        return dataStats
    
    else:
        return pd.DataFrame()



def listRefereeSeasons(data, referee):
    data = data[data['referee'] == referee]
    return sorted(tuple(data['season'].unique()), reverse=True)

def listTeamSeasons(data, team):
    data = data[data['homeTeam'] == team]
    return sorted(tuple(data['season'].unique()), reverse=True)

def listLeagueTeams(data, league):
    data = data[data['league'] == league]
    return tuple(data['homeTeam'].unique())


def changeTeamNames(data):
    dictionary = {
        'Manchester Utd': 'Manchester United',
        'Tottenham': 'Tottenham Hotspur',
        "Nott'ham Forest": 'Nottingham Forest',
        'West Ham': 'West Ham United',
        'Brighton': 'Brighton & Hove Albion',
        'Newcastle Utd': 'Nottingham Forest',
        'Wolves': 'Wolverhampton Wanderers',
        'Sheffield Utd': 'Sheffield United',
        'Leicester City': 'Leicester City',
        'Southampton': 'Southampton',
        'Paris S-G': 'Paris Saint-Germain',
        'Betis': 'Real Betis',
        'Inter': 'Internazionale',
        'Leverkusen': 'Bayer Leverkusen',
        'Eint Frankfurt': 'Eintracht Frankfurt',
        "M'Gladbach": 'Mönchengladbach',
        'Newcastle Utd': 'Newcastle United',
        
        }
    data.replace({'homeTeam': dictionary, 'awayTeam': dictionary}, inplace=True)

def teamFutureMatches(data, team):
    
    columns = ['date', 'homeTeam', 'awayTeam']
    data = data[columns]
    
    changeTeamNames(data)
    
    matches = data[(data['homeTeam'] == team) | (data['awayTeam'] == team)]
    
    from datetime import datetime
    current_date = datetime.now().date()
    matches = matches.copy()
    matches['date'] = pd.to_datetime(matches['date'])
    
    current_date_datetime64 = pd.to_datetime(current_date)
    matches = matches[matches['date'] >= current_date_datetime64]
    matches['date'] = matches['date'].astype(str)

    changeColumnNames(matches)
    return matches

def teamSquad(data, team, season):
    data = data[data['team'] == team]
    data = data[data['season'] == season]
    data['player'] = data['player'].apply(lambda x: x.strip())
    players = data['player'].unique()
    players = pd.DataFrame(players, columns=['Zawodnik'])
    return players
    
def matchStats(data, date, homeTeam, awayTeam):
    data = data.loc[data['date'] == date]
    data = data.loc[data['homeTeam'] == homeTeam]
    data = data.loc[data['awayTeam'] == awayTeam]
    
    changeColumnNames(data)
    
    return data

def teamMatchSquad(data, date, team):
    data = data.loc[data['date'] == date]
    data = data.loc[data['team'] == team]
    data['status'] = data['status'].replace({'bench': 'Rezerwa', 'firstSquad': 'Pierwszy skład'})
    changeColumnNames(data)

    return data

def obliczMinute(minuta):
    parts = minuta.split('+')
    if len(parts) == 2:
        return int(parts[0]) + int(parts[1])
    else:
        return int(minuta)

def matchEvents(data, date, homeTeam, awayTeam):
    data = data[data['date'] == date]
    data = data[data['homeTeam'] == homeTeam]
    data = data[data['awayTeam'] == awayTeam]

    dataFirstHalf = data[(data['minute'] < '46') | (data['minute'].str.len() < 2)]
    dataSecondHalf = data[(data['minute'] >= '46') & (data['minute'].str.len() > 1)]
    
    dataFirstHalf = dataFirstHalf.copy()
    dataSecondHalf = dataSecondHalf.copy()
    
    dataFirstHalf['minute'] = dataFirstHalf['minute'].apply(obliczMinute)
    dataFirstHalf = dataFirstHalf.sort_values(['minute'])
    
    dataSecondHalf['minute'] = dataSecondHalf['minute'].apply(obliczMinute)
    dataSecondHalf = dataSecondHalf.sort_values(['minute'])
    
    columns = ['minute', 'team', 'eventType', 'playerOne', 'playerTwo']
    dataFirstHalf = dataFirstHalf[columns]
    dataSecondHalf = dataSecondHalf[columns]
    
    dataFirstHalf['eventType'] = dataFirstHalf['eventType'].replace({
        'yellow_card': 'Żółta kartka', 
        'red_card': 'Czerwona kartka',
        'substitute_in': 'Zmiana',
        'goal': 'Gol'})
    
    dataFirstHalf['eventType'] = dataFirstHalf['eventType'].fillna('Penalty goal')
    dataFirstHalf['playerTwo'] = dataFirstHalf['playerTwo'].fillna('')
    
    dataSecondHalf['eventType'] = dataSecondHalf['eventType'].replace({
        'yellow_card': 'Żółta kartka', 
        'red_card': 'Czerwona kartka',
        'substitute_in': 'Zmiana',
        'goal': 'Gol'})
    
    dataFirstHalf['eventType'] = dataFirstHalf['eventType'].fillna('Penalty goal')
    dataSecondHalf['playerTwo'] = dataSecondHalf['playerTwo'].fillna('')

    changeColumnNames(dataFirstHalf)
    changeColumnNames(dataSecondHalf)
    
    return dataFirstHalf, dataSecondHalf



def changeCountryNames(data):
    dictionary = {
    'ch SUI': 'Szwajcaria',
    'ma MAR': 'Maroko',
    'za RSA': 'Republika Południowej Afryki',
    'eng ENG': 'Anglia',
    'ie IRL': 'Irlandia',
    'no NOR': 'Norwegia',
    'it ITA': 'Włochy',
    'dk DEN': 'Dania',
    'br BRA': 'Brazylia',
    'de GER': 'Niemcy',
    'be BEL': 'Belgia',
    'wls WAL': 'Walia',
    'pt POR': 'Portugalia',
    'ar ARG': 'Argentyna',
    'es ESP': 'Hiszpania',
    'hr CRO': 'Chorwacja',
    'nl NED': 'Holandia',
    'jp JPN': 'Japonia',
    'fr FRA': 'Francja',
    'gh GHA': 'Ghana',
    'se SWE': 'Szwecja',
    'ng NGA': 'Nigeria',
    'sn SEN': 'Senegal',
    'ci CIV': 'Wybrzeże Kości Słoniowej',
    'sct SCO': 'Szkocja',
    'nz NZL': 'Nowa Zelandia',
    'us USA': 'Stany Zjednoczone',
    'ml MLI': 'Mali',
    'mx MEX': 'Meksyk',
    'rs SRB': 'Serbia',
    'jm JAM': 'Jamajka',
    'au AUS': 'Australia',
    'eg EGY': 'Egipt',
    'ir IRN': 'Iran',
    'ua UKR': 'Ukraina',
    'al ALB': 'Albania',
    'co COL': 'Kolumbia',
    'tr TUR': 'Turcja',
    'cl CHI': 'Czile',
    'gr GRE': 'Grecja',
    'is ISL': 'Islandia',
    'am ARM': 'Armenia',
    'pl POL': 'Polska',
    'Meksyk': 'Meksyk',
    'kr KOR': 'Korea Południowa',
    'uy URU': 'Urugwaj',
    'Serbia': 'Serbia',
    'ba BIH': 'Bośnia i Hercegowina',
    'sk SVK': 'Słowacja',
    'zw ZIM': 'Zimbabwe',
    'cz CZE': 'Czechy',
    'Japonia': 'Japonia',
    'tz TAN': 'Tanzania',
    'dz ALG': 'Algieria',
    'gn GUI': 'Gwinea',
    'cu CUB': 'Kuba',
    'ga GAB': 'Gabon',
    'cw CUW': 'Curaçao',
    'fi FIN': 'Finlandia',
    'ke KEN': 'Kenia',
    'tn TUN': 'Tunezja',
    'nir NIR': 'Irlandia Północna',
    'py PAR': 'Paragwaj',
    'ro ROU': 'Rumunia',
    'cm CMR': 'Kamerun',
    'at AUT': 'Austria',
    'ca CAN': 'Kanada',
    'bf BFA': 'Burkina Faso',
    'si SVN': 'Słowenia',
    'hu HUN': 'Węgry',
    'cd COD': 'Demokratyczna Republika Konga',
    'xk KVX': 'Kosowo',
    'sr SUR': 'Surinam',
    'ec ECU': 'Ekwador',
    'cr CRC': 'Kostaryka',
    'bg BUL': 'Bułgaria',
    'lu LUX': 'Luksemburg',
    'tg TOG': 'Togo',
    'me MNE': 'Czarnogóra',
    'tt TRI': 'Trynidad i Tobago',
    'cg CGO': 'Kongo',
    'cv CPV': 'Republika Zielonego Przylądka',
    'nc NCL': 'Nowa Kaledonia',
    'cf CTA': 'Republika Środkowoafrykańska',
    'mq MTQ': 'Martynika',
    'mg MAD': 'Madagaskar',
    'gw GNB': 'Gwinea Bissau',
    'gf GUF': 'Gujana Francuska',
    'mz MOZ': 'Mozambik',
    'do DOM': 'Dominikana',
    'mr MTN': 'Mauretania',
    'bj BEN': 'Benin',
    'td CHA': 'Czad',
    'ht HAI': 'Haiti',
    'km COM': 'Komory',
    'gp GLP': 'Gwadelupa',
    'ne NIG': 'Niger',
    'ru RUS': 'Rosja',
    'mf SMN': 'Saint-Martin',
    'pe PER': 'Peru',
    'zm ZAM': 'Zambia',
    'mk MKD': 'Macedonia Północna',
    've VEN': 'Wenezuela',
    'ge GEO': 'Gruzja',
    'hn HON': 'Honduras',
    'ao ANG': 'Angola',
    'bi BDI': 'Burundi',
    'mt MLT': 'Malta',
    'jo JOR': 'Jordania',
    'gm GAM': 'Gambia',
    'uz UZB': 'Uzbekistan',
    'pa PAN': 'Panama',
    'cn CHN': 'Chiny',
    'il ISR': 'Izrael',
    'gq EQG': 'Gwinea Równikowa',
    'gt GUA': 'Gwatemala',
    'ph PHI': 'Filipiny',
    'kn SKN': 'Saint Kitts i Nevis',
    'gd GRN': 'Grenada',
    'md MDA': 'Mołdawia',
    'ee EST': 'Estonia',
    'lt LTU': 'Litwa',
    'bo BOL': 'Boliwia',
    'sl SLE': 'Sierra Leone',
    'ly LBY': 'Libia',
    'cy CYP': 'Cypr',
    'lv LVA': 'Łotwa',
}

    data.replace({'nationality': dictionary}, inplace=True)
    
def searchPlayers(data, season):
    import numpy as np
    data = data[data['season'] == season]
    data = data.copy()
    
    data['age'] = data['age'].apply(lambda x: x[:2] if not pd.isna(x) else np.nan)
    data['position'] = data['position'].apply(lambda x: x[:2])
    data['player'] = data['player'].apply(lambda x: x.strip())

    players = data.groupby(['player', 'league', 'nationality']).agg({
        'team': 'last',
        'age': 'max',
        'position': lambda x: x.mode().iat[0] if len(x.mode()) > 0 else None
        })
    players.reset_index(inplace=True)
    changeCountryNames(players)
    changeColumnNames(players)
    return players

def findTeamLeague(data, team, season):
    data = data[data['season'] == season]
    data = data[(data['homeTeam'] == team) | (data['awayTeam'] == team)]
    league = data['league'].value_counts().idxmax()
    
    return league
    

def checkUpdateStatus(data, dataFuture, league, season):
    # zwraca liste meczy dla ktorych nie ma danych w bazie i data ich odbycia jest mniejsza lub taka sama jak obecna data
    print(league, season)
    data = data[data['season'] == season]
    data = data[data['league'] == league]
    
    dataFuture = dataFuture[dataFuture['season'] == season]
    dataFuture = dataFuture[dataFuture['league'] == league]
    
    if data.shape[0] > 0:
    
        data['date'] = pd.to_datetime(data['date'])
        dataFuture['date'] = pd.to_datetime(dataFuture['date'])
        
        # usuniecie meczy ktore juz sa zaktualizowane
        dataAktualizacji = max(data['date'])
        dataFuture = dataFuture[dataFuture['date'] > dataAktualizacji]
    
        # usuniecie meczy ktore maja date przyszla wzgledem obecnej
        from datetime import datetime
        current_date = datetime.now().date()
        current_date = pd.to_datetime(current_date)
    
        dataFuture = dataFuture[dataFuture['date'] <= current_date]
        
        print(dataFuture)
        return dataFuture
    else:
        return pd.DataFrame()

def updateMatches(matchesToUpdate, league):
    import requests
    import time
    from bs4 import BeautifulSoup
    import pandas as pd

    if matchesToUpdate.shape[0] == 0:
        return
    else:
        # wczytanie istniejacych plikow z danymi
        matchStatsExisting = pd.read_csv("./Scraper/MatchStats.csv", sep=";", encoding='UTF-8')
        matchSquadsExisting = pd.read_csv("./Scraper/MatchSquads.csv", sep=";", encoding='UTF-8')
        matchShotsExisting = pd.read_csv("./Scraper/MatchShots.csv", sep=";", encoding='UTF-8')
        matchEventsExisting = pd.read_csv("./Scraper/MatchEvents.csv", sep=";", encoding='UTF-8')
        allPlayerStatsExisting = pd.read_csv("./Scraper/AllPlayerStats.csv", sep=";", encoding='UTF-8')
    
        if league == 'PremierLeague':
            URL = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
        elif league == 'SerieA':
            URL = 'https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures'
        elif league == 'Bundesliga':
            URL = 'https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures'
        elif league == 'LaLiga':
            URL = 'https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures'
        elif league == 'Ligue1':
            URL = 'https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures'
    
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        matches = soup.select('div[id="content"] tbody tr')
        matchList = []
        matchStatList = []
    
        for i in range(len(matches)):
            if (matches[i].select('th[data-stat="gameweek"]')):
                matchWeek = matches[i].select('th[data-stat="gameweek"]')[0].text
                matchURL = matches[i].select('td[data-stat="score"]')
                matchData = matches[i].select('td[data-stat="date"]')
                matchHomeTeam = matches[i].select('td[data-stat="home_team"]')
                matchAwayTeam = matches[i].select('td[data-stat="away_team"]')
                if (matchURL[0].find('a')):
                    matchList.append((matchWeek, matchURL[0].a['href'], matchData[0].text, matchHomeTeam[0].text, matchAwayTeam[0].text))
    
    
        allMatchesDF = pd.DataFrame(matchList, columns=['matchweek', 'URL', 'date', 'homeTeam', 'awayTeam'])
        allMatchesDF['date'] = pd.to_datetime(allMatchesDF['date'])
        
    
        merged_df = pd.merge(matchesToUpdate, allMatchesDF[['date', 'homeTeam', 'awayTeam', 'URL', 'matchweek']], on=['date', 'homeTeam', 'awayTeam'], how='left')
       
        requestsTimes = [] 
       
        for index, row in merged_df.iterrows():
            if pd.notna(row['URL']):
                # mecze ktore sa do aktualizacji i wyniki sa juz na strone
                completeURL = 'https://fbref.com' + row['URL']
                league = league
                season = '23_24'
                matchweek = row['matchweek']
                
                if len(requestsTimes) == 20:
                    if time.time() - requestsTimes[0] < 60:
                        time.sleep(60 - (time.time() - requestsTimes[0]))
                        requestsTimes.pop(0)
                    else:
                        requestsTimes.pop(0)
                
                matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, requestTime = collectMatch(completeURL,
                                                                                                             league, season,
                                                                                                             matchweek)
                
                from DataProcessing import processMatchStats, processPlayerStats
                matchStats = processMatchStats(matchStats)
                allPlayerStats = processPlayerStats(allPlayerStats)
                
                requestsTimes.append(requestTime)
                #print(matchStats)
                matchStatsExisting = pd.concat([matchStatsExisting, matchStats])
                matchSquadsExisting = pd.concat([matchSquadsExisting, matchSquads])
                matchShotsExisting = pd.concat([matchShotsExisting, matchShots])
                matchEventsExisting = pd.concat([matchEventsExisting, matchEvents])
                allPlayerStatsExisting = pd.concat([allPlayerStatsExisting, allPlayerStats])
    
        matchStatsExisting.to_csv("./Scraper/MatchStats.csv", index=False, sep=";", encoding='UTF-8')
        matchSquadsExisting.to_csv("./Scraper/MatchSquads.csv", index=False, sep=";", encoding='UTF-8')
        matchShotsExisting.to_csv("./Scraper/MatchShots.csv", index=False, sep=";", encoding='UTF-8')
        matchEventsExisting.to_csv("./Scraper/MatchEvents.csv", index=False, sep=";", encoding='UTF-8')
        allPlayerStatsExisting.to_csv("./Scraper/AllPlayerStats.csv", index=False, sep=";", encoding='UTF-8')
        
def playerFinishedMatches(data, dataMatches, player, season):
    data = data[data['player'] == player]
    data = data[data['season'] == season]
    
    dataMatches = dataMatches[dataMatches['season'] == season]
    
    columns = ['date','homeTeam', 'awayTeam','minutes', 'goals', 'assists', 'cards_yellow', 'cards_red', 'shots', 'passes', 
               'fouls', 'position',]
    data = data[columns]

    dataMerged = pd.merge(data, dataMatches[['date', 'homeTeam', 'awayTeam','homeGoals', 'awayGoals']], on=['date','homeTeam', 'awayTeam'], how='left')
    
    dataMerged['Wynik'] = dataMerged['homeGoals'].astype(str) + ':' + dataMerged['awayGoals'].astype(str)
    
    columns = ['date','homeTeam', 'awayTeam', 'Wynik','minutes', 'goals', 'assists', 'cards_yellow', 'cards_red', 'shots', 'passes', 
               'fouls', 'position',]
    dataMerged = dataMerged[columns]
    
    changeColumnNames(dataMerged)
    return dataMerged

def countCardsMatch(dataEvents, date, homeTeam, awayTeam):
    homeYellowCards = 0
    awayYellowCards = 0 
    homeRedCards = 0
    awayRedCards = 0
    dataEvents = dataEvents[dataEvents['date'] == date]
    dataEvents = dataEvents[dataEvents['homeTeam'] == homeTeam]
    dataEvents = dataEvents[dataEvents['awayTeam'] == awayTeam]
    
    dataEventsHome = dataEvents[dataEvents['team'] == homeTeam]
    homeYellowCards = dataEventsHome['eventType'].str.count('yellow_card').sum()
    homeRedCards = dataEventsHome['eventType'].str.count('red_card').sum()
    
    dataEventsAway = dataEvents[dataEvents['team'] == awayTeam]
    awayYellowCards = dataEventsAway['eventType'].str.count('yellow_card').sum()
    awayRedCards = dataEventsAway['eventType'].str.count('red_card').sum()
    
    return homeYellowCards, awayYellowCards, homeRedCards, awayRedCards

def refereeMatches(data, dataEvents, referee, season):
    data = data[data['referee'] == referee]
    data = data[data['season'] == season]
    
    if data.shape[0] > 0:
        columns = ['date', 'hour', 'league', 'season', 'homeTeam', 'awayTeam', 'homeGoals', 'awayGoals']
        data = data[columns]
        
        # Utwórz nowe kolumny, wypełnione początkowo wartościami None
        data['homeYellowCards'] = None
        data['awayYellowCards'] = None
        data['homeRedCards'] = None
        data['awayRedCards'] = None
    
        # Przypisz wyniki funkcji countCardsMatch do nowych kolumn
        data['homeYellowCards'], data['awayYellowCards'], data['homeRedCards'], data['awayRedCards'] = zip(*data.apply(lambda row: countCardsMatch(dataEvents, row['date'], row['homeTeam'], row['awayTeam']), axis=1))
    
        data['Wynik'] = data['homeGoals'].astype(str) + ':' + data['awayGoals'].astype(str)
        columns = ['date', 'hour', 'league', 'season', 'homeTeam', 'awayTeam', 'Wynik', 'homeYellowCards', 'awayYellowCards', 'homeRedCards', 'awayRedCards']
        data = data[columns]
        changeColumnNames(data)
        
        return data
    else:
        return pd.DataFrame()


#data = pd.read_csv('./Scraper/MatchStats.csv', delimiter=';')
#dataFuture = pd.read_csv('./Scraper/futureMatches.csv', delimiter=';')
#dataSquads = pd.read_csv('./Scraper/MatchSquads.csv', delimiter=';')
#dataPlayerStats = pd.read_csv('./Scraper/allPlayerStats.csv', delimiter=';')
#dataEvents = pd.read_csv('./Scraper/MatchEvents.csv', delimiter=';')
#changeCountryNames(dataPlayerStats)
#print(dataPlayerStats['nationality'].unique())
#print(data[['homeYellowCards']])















