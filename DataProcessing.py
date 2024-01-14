


def repeatingRows(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches):
    # sprawdzanie czy sa jakies powtarzajace sie wiersze
    print("Repeating rows:")
    print(matchStats.duplicated().any())
    print(matchSquads.duplicated().any())
    print(matchShots.duplicated().any())
    print(matchEvents.duplicated().any())
    print(allPlayerStats.duplicated().any())
    print(futureMatches.duplicated().any())

def checkMatchNumber(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches):
    # sprawdzanie liczby meczy w danym pliku z danego sezonu i danej ligi
    matches_count = matchStats.groupby(['league', 'season']).size().reset_index(name='matches_count')
    print(matches_count)
    
    df_lineups = matchSquads[['league', 'season', 'homeTeam', 'awayTeam']].copy()
    df_lineups['teamCombination'] = df_lineups['homeTeam'] + '-' + df_lineups['awayTeam']
    unique_team_combinations_count = df_lineups.groupby(['league', 'season'])['teamCombination'].nunique()
    print(unique_team_combinations_count)
    
    df_shots = matchShots[['league', 'season', 'homeTeam', 'awayTeam']].copy()
    df_shots['teamCombination'] = df_shots['homeTeam'] + '-' + df_shots['awayTeam']
    unique_team_combinations_count = df_shots.groupby(['league', 'season'])['teamCombination'].nunique()
    print(unique_team_combinations_count)
    
    df_events = matchEvents[['league', 'season', 'homeTeam', 'awayTeam']].copy()
    df_events['teamCombination'] = df_events['homeTeam'] + '-' + df_events['awayTeam']
    unique_team_combinations_count = df_events.groupby(['league', 'season'])['teamCombination'].nunique()
    print(unique_team_combinations_count)
    
    df_players = allPlayerStats[['league', 'season', 'homeTeam', 'awayTeam']].copy()
    df_players['teamCombination'] = df_players['homeTeam'] + '-' + df_players['awayTeam']
    unique_team_combinations_count = df_players.groupby(['league', 'season'])['teamCombination'].nunique()
    print(unique_team_combinations_count)
    
    df_futureMatches = futureMatches[['league', 'season', 'homeTeam', 'awayTeam']].copy()
    df_futureMatches['teamCombination'] = df_futureMatches['homeTeam'] + '-' + df_futureMatches['awayTeam']
    unique_team_combinations_count = df_futureMatches.groupby(['league', 'season'])['teamCombination'].nunique()
    print(unique_team_combinations_count)

def saveProcessedData(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches):
    # zapisuje przetworzone dane do csv
    matchStatsExisting = pd.read_csv(".\\MatchStatsProcessed.csv", sep=";", encoding='UTF-8')
    matchSquadsExisting = pd.read_csv(".\\MatchSquadsProcessed.csv", sep=";", encoding='UTF-8')
    matchShotsExisting = pd.read_csv(".\\MatchShotsProcessed.csv", sep=";", encoding='UTF-8')
    matchEventsExisting = pd.read_csv(".\\MatchEventsProcessed.csv", sep=";", encoding='UTF-8')
    allPlayerStatsExisting = pd.read_csv(".\\AllPlayerStatsProcessed.csv", sep=";", encoding='UTF-8')
    futureMatchesExisting = pd.read_csv(".\\FutureMatchesProcessed.csv", sep=";", encoding='UTF-8')
    
    #matchStatsExisting.drop(matchStatsExisting.index, inplace=True)
    #matchSquadsExisting.drop(matchSquadsExisting.index, inplace=True)
    #matchShotsExisting.drop(matchShotsExisting.index, inplace=True)
    #matchEventsExisting.drop(matchEventsExisting.index, inplace=True)
    #allPlayerStatsExisting.drop(allPlayerStatsExisting.index, inplace=True)
    #futureMatchesExisting.drop(futureMatchesExisting.index, inplace=True)

    matchStatsExisting = pd.concat([matchStatsExisting, matchStats])
    matchSquadsExisting = pd.concat([matchSquadsExisting, matchSquads])
    matchShotsExisting = pd.concat([matchShotsExisting, matchShots])
    matchEventsExisting = pd.concat([matchEventsExisting, matchEvents])
    allPlayerStatsExisting = pd.concat([allPlayerStatsExisting, allPlayerStats])
    futureMatchesExisting = pd.concat([futureMatchesExisting, futureMatches])
    
    matchStatsExisting.to_csv(".\\MatchStatsProcessed.csv", index=False, sep=";", encoding='UTF-8')
    matchSquadsExisting.to_csv(".\\MatchSquadsProcessed.csv", index=False, sep=";", encoding='UTF-8')
    matchShotsExisting.to_csv(".\\MatchShotsProcessed.csv", index=False, sep=";", encoding='UTF-8')
    matchEventsExisting.to_csv(".\\MatchEventsProcessed.csv", index=False, sep=";", encoding='UTF-8')
    allPlayerStatsExisting.to_csv(".\\AllPlayerStatsProcessed.csv", index=False, sep=";", encoding='UTF-8')
    futureMatchesExisting.to_csv(".\\FutureMatchesProcessed.csv", index=False, sep=";", encoding='UTF-8')
    
    
def processMatchStats(matchStats):
    # obrabianie MatchStats

    # usuniecie spacji z nazw kolumn
    matchStats.columns = [column.replace(' ', '') for column in matchStats.columns]
    
    # usuwanie nawiasu (referee) z jego imienia i nazwiska
    matchStats['referee'] = matchStats['referee'].str.rstrip(" (Referee)")
    
    # usuwanie nazwy druzyny z lineup
    matchStats['homeLineup'] = matchStats['homeLineup'].str.partition("(")[2].str.partition(")")[0]
    matchStats['awayLineup'] = matchStats['awayLineup'].str.partition("(")[2].str.partition(")")[0]
    
    
    # zamiana wartosci procentowych na liczbe i usuniecie znaku %
    # Funkcja lambda zamiany % na 0%
    replace = lambda cell: '0%' if isinstance(cell, str) and cell == '%' else cell
    
    for column in ('homePossession', 'awayPossession', 'homePassingAccuracy', 'awayPassingAccuracy', 'homeShotsonTarget', 'awayShotsonTarget', 'homeSaves', 'awaySaves'):
      matchStats[column] = matchStats[column].fillna('0%')
      matchStats[column] = matchStats[column].apply(replace)
      matchStats[column] = (matchStats[column].str.partition("%")[0]).astype(int) / 100
     
    return matchStats
    
def processPlayerStats(playerStats):
    # poprawianie players stats
    for column in ('aerials_won_pct', 'take_ons_tackled_pct', 'take_ons_won_pct', 'challenge_tackles_pct', 'passes_pct_long', 'passes_pct_medium', 'passes_pct_short', 'passes_pct'):
      playerStats[column] = playerStats[column].fillna(0)
    return playerStats


import pandas as pd

#matchStats = pd.read_csv(".\\MatchStats.csv", sep=";", encoding='UTF-8')
#matchSquads = pd.read_csv(".\\MatchSquads.csv", sep=";", encoding='UTF-8')
#matchShots = pd.read_csv(".\\MatchShots.csv", sep=";", encoding='UTF-8')
#matchEvents = pd.read_csv(".\\MatchEvents.csv", sep=";", encoding='UTF-8')
#allPlayerStats = pd.read_csv(".\\AllPlayerStats.csv", sep=";", encoding='UTF-8')
#futureMatches = pd.read_csv(".\\FutureMatches.csv", sep=";", encoding='UTF-8')


#repeatingRows(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches)
#checkMatchNumber(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches)

#matchStats = processMatchStats(matchStats)
#allPlayerStats = processPlayerStats(allPlayerStats)

#saveProcessedData(matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, futureMatches)




























