import pandas as pd

def leagueTable(data, league, season):
    data = data.loc[data['season'] == season]
    data = data.loc[data['league'] == league]
    
    homeStats = data.groupby('homeTeam').agg({
        'homeTeam': 'count',
        'homeGoals': 'sum',
        'awayGoals': 'sum',
    })
    homeStats.columns = ['Zagrane mecze', 'Strzelone', 'Stracone']
    
    awayStats = data.groupby('awayTeam').agg({
        'awayTeam': 'count',
        'awayGoals': 'sum',
        'homeGoals': 'sum',
    })
    awayStats.columns = ['Zagrane mecze', 'Strzelone', 'Stracone']
    
    teamStats = homeStats.add(awayStats)
    teamStats.reset_index(inplace=True)
    teamStats.rename(columns={'homeTeam': 'Drużyna'}, inplace=True)
    
    return teamStats

def teamMatches(data, season, team):
    data = data.loc[data['season'] == season]
    homeData = data.loc[data['homeTeam'] == team]
    awayData = data.loc[data['awayTeam'] == team]
    data = pd.concat([homeData, awayData])
    
    data = data.sort_values(['date'])
    data.reset_index(inplace=True)
    changeColumnNames(data)
    
    return data

def leagueMatches(data, season, league):
    data = data.loc[(data['season'] == season) & (data['league'] == league)]
    
    data = data.sort_values(['date'])
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

def changeColumnNames(data):
    dictonary = {'homeTeam': 'Gospodarz', 'awayTeam': 'Przyjezdny'}
    data.rename(columns=dictonary, inplace=True)
    
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




