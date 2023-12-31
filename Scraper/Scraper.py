def collectMatch(URL, league, season, matchweek):
    import requests
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    import time
    import re
    
    pd.options.display.max_columns = None
    
    page = requests.get(URL)
    requestTime = time.time()
    soup = BeautifulSoup(page.content, 'html.parser')
    
    matchStats = pd.DataFrame(columns=['league', 'season', 'matchweek'])
    
    matchStats.at[0, 'league'] = league
    matchStats.at[0, 'season'] = season
    matchStats.at[0, 'matchweek'] = matchweek

    teams = soup.select('div[class="scorebox"] strong a')
    matchStats.at[0, 'homeTeam'] = teams[0].text
    matchStats.at[0, 'awayTeam'] = teams[1].text
    
    result = soup.select('div[class="score"]')
    matchStats.at[0, 'homeGoals'] = result[0].text
    matchStats.at[0, 'awayGoals'] = result[1].text
    
    date = soup.select('span[class="venuetime"]')
    matchStats.at[0, 'date'] = date[0]['data-venue-date']
    matchStats.at[0, 'hour'] = date[0]['data-venue-time']

    referees = soup.select('div[class="scorebox_meta"] div small span')
    matchStats.at[0, 'referee'] = referees[0].text

    lineups = soup.select('div[class="lineup"] tr th[colspan="2"]')
    matchStats.at[0, 'homeLineup'] = lineups[0].text
    matchStats.at[0, 'awayLineup'] = lineups[2].text

    stats = soup.select('div[id="team_stats"] table tr')
    for i in range(1, len(stats) - 2, 2):
        matchStats.at[0, 'home' + stats[i].text] = stats[i+1].select('div strong')[0].text
        matchStats.at[0, 'away' + stats[i].text] = stats[i+1].select('div strong')[1].text

    
    extraStats = soup.select('div[id="team_stats_extra"] div div')
    for i in range(int((len(extraStats)) / 3)):
        if (i % 5) != 0:
            if(extraStats[i*3].text != matchStats.at[0, 'homeTeam']):
                matchStats.at[0, 'home' + extraStats[i*3 + 1].text] = extraStats[i*3].text
                matchStats.at[0, 'away' + extraStats[i*3 + 1].text] = extraStats[i*3 + 2].text
                
                
    # team squads
    teamSquads = soup.select('div[class="lineup"]')
    homeSquad = teamSquads[0]
    awaySquad = teamSquads[1]
    
    matchSquads = []
    
    homePlayers = homeSquad.select('tr a')
    for i in range(len(homePlayers)):
        if i < 11:
            matchSquads.append([matchStats.at[0, 'homeTeam'], matchStats.at[0, 'awayTeam'], homePlayers[i].text, 'firstSquad'])
        else:
            matchSquads.append([matchStats.at[0, 'homeTeam'], matchStats.at[0, 'awayTeam'], homePlayers[i].text, 'bench'])
            
    awayPlayers = awaySquad.select('tr a')
    for i in range(len(awayPlayers)):
        if i < 11:
            matchSquads.append([matchStats.at[0, 'homeTeam'], matchStats.at[0, 'awayTeam'], awayPlayers[i].text, 'firstSquad'])
        else:
            matchSquads.append([matchStats.at[0, 'homeTeam'], matchStats.at[0, 'awayTeam'], awayPlayers[i].text, 'bench'])
            

    
    matchSquadsDF = pd.DataFrame(matchSquads, columns=['homeTeam', 'awayTeam', 'player', 'status'])
    matchSquadsDF[['league', 'season', 'matchweek', 'date']] = [
     league, season, matchweek, 
     matchStats.at[0, 'date']]


    # match shots
    matchShots = soup.select('table[id="shots_all"] tbody tr')
    allMatchShots = pd.DataFrame()
    
    for i, shot in enumerate(matchShots):
        minuteShot = shot.select('th')
        if minuteShot[0].text != '':
            allMatchShots.at[i, 'league'] = league
            allMatchShots.at[i, 'season'] = season
            allMatchShots.at[i, 'matchweek'] = matchweek
            allMatchShots.at[i, 'date'] = matchStats.at[0, 'date']
            allMatchShots.at[i, 'minute'] = minuteShot[0].text
            
            detailsShot = shot.select('td')
            for detail in detailsShot:
                allMatchShots.at[i, detail['data-stat']] = detail.text
                
                
    allMatchShots[['league', 'season', 'matchweek', 'date', 'homeTeam', 'awayTeam']] = [
     league, season, matchweek, 
     matchStats.at[0, 'date'], 
     matchStats.at[0, 'homeTeam'], 
     matchStats.at[0, 'awayTeam']]
    allMatchShots.reset_index(inplace=True, drop=True)
                

    # match events
    matchEvents = soup.select('div[id="events_wrap"]')
    matchHomeEvents = matchEvents[0].select('div[class="event a"]')
    matchAwayEvents = matchEvents[0].select('div[class="event b"]')
    
    matchEventsDF = pd.DataFrame(columns=['minute', 'team', 'eventType', 'playerOne', 'playerTwo'])
    
    for event in matchHomeEvents:
        i = len(matchEventsDF)
        eventStats = event.select('div')
        minute = eventStats[0].text
        minute = minute.split('&')[0]
        
        matchEventsDF.at[i, 'minute'] = minute.strip()
        matchEventsDF.at[i, 'team'] = matchStats.at[0, 'homeTeam']
        
        eventType = eventStats[1].select('div')
        eventType = eventType[0]['class'][1]
    
        if eventType in ['substitute_in', 'goal']:

            matchEventsDF.at[i, 'eventType'] = eventType
            
            playerOne = eventStats[1].select('div a')[0].text
            matchEventsDF.at[i, 'playerOne'] = playerOne
            
            if(len(eventStats[1].select('div a')) > 1):
                playerTwo = eventStats[1].select('div a')[1].text
                matchEventsDF.at[i, 'playerTwo'] = playerTwo
            
        elif eventType in ['red_card', 'yellow_card']:
            matchEventsDF.at[i, 'eventType'] = eventType
            
            playerOne = eventStats[1].select('div a')[0].text
            matchEventsDF.at[i, 'playerOne'] = playerOne
            
            
            
    for event in matchAwayEvents:
        i = len(matchEventsDF)
        eventStats = event.select('div')
        minute = eventStats[0].text
        minute = minute.split('&')[0]
        
        matchEventsDF.at[i, 'minute'] = minute.strip()
        matchEventsDF.at[i, 'team'] = matchStats.at[0, 'awayTeam']
        
        eventType = eventStats[1].select('div')
        eventType = eventType[0]['class'][1]
    
        if eventType in ['substitute_in', 'goal']:

            matchEventsDF.at[i, 'eventType'] = eventType
            
            playerOne = eventStats[1].select('div a')[0].text
            matchEventsDF.at[i, 'playerOne'] = playerOne
            
            if(len(eventStats[1].select('div a')) > 1):
                playerTwo = eventStats[1].select('div a')[1].text
                matchEventsDF.at[i, 'playerTwo'] = playerTwo
            
        elif eventType in ['red_card', 'yellow_card']:
            matchEventsDF.at[i, 'eventType'] = eventType
            
            playerOne = eventStats[1].select('div a')[0].text
            matchEventsDF.at[i, 'playerOne'] = playerOne
            
    matchEventsDF[['league', 'season', 'matchweek', 'date', 'homeTeam', 'awayTeam']] = [
     league, season, matchweek, 
     matchStats.at[0, 'date'], 
     matchStats.at[0, 'homeTeam'], 
     matchStats.at[0, 'awayTeam']]
    
    # player stats summary
    
    allPlayerStatsSummary = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="summary"] table[id$="summary"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsSummary.at[i, item['data-stat']] = item.text


    offset = len(allPlayerStatsSummary)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsSummary.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsSummary.reset_index(inplace=True, drop=True)
    
    
    # player stats passing
    
    allPlayerStatsPassing = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="passing"] table[id$="passing"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsPassing.at[i, item['data-stat']] = item.text
            
    offset = len(allPlayerStatsPassing)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsPassing.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsPassing.reset_index(inplace=True, drop=True)
    
    # player stats passing types
    
    allPlayerStatsPassingTypes = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="passing_types"] table[id$="passing_types"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsPassingTypes.at[i, item['data-stat']] = item.text
            
    offset = len(allPlayerStatsPassingTypes)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsPassingTypes.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsPassingTypes.reset_index(inplace=True, drop=True)
    
    # player stats defense
    
    allPlayerStatsDefence = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="defense"] table[id$="defense"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsDefence.at[i, item['data-stat']] = item.text
            
    offset = len(allPlayerStatsDefence)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsDefence.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsDefence.reset_index(inplace=True, drop=True)
    
    # player stats possession
    
    allPlayerStatsPossesion = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="possession"] table[id$="possession"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsPossesion.at[i, item['data-stat']] = item.text
            
    offset = len(allPlayerStatsPossesion)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsPossesion.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsPossesion.reset_index(inplace=True, drop=True)
    
    # player stats misc
    
    allPlayerStatsMisc = pd.DataFrame()
    
    allPlayers = soup.select('div[id^="switcher_player_stats"] div[id$="misc"] table[id$="misc"]')
    allPLayers = allPlayers[0].select('tbody tr tr tr')
    allPLayers = allPlayers[0].select('tr')
    allPlayersHome = allPlayers[0].select('tr')
    allPlayersAway = allPlayers[1].select('tr')

    for i in range(2, len(allPlayersHome)-1):
        for item in allPlayersHome[i]:
            allPlayerStatsMisc.at[i, item['data-stat']] = item.text
            
    offset = len(allPlayerStatsMisc)

    for i in range(2, len(allPlayersAway) -1):
        for item in allPlayersAway[i]:
            allPlayerStatsMisc.at[i + offset, item['data-stat']] = item.text

    allPlayerStatsMisc.reset_index(inplace=True, drop=True)
    
    allPlayerStatsSummary.set_index('player', inplace=True)
    allPlayerStatsPassing.set_index('player', inplace=True)
    allPlayerStatsPassingTypes.set_index('player', inplace=True)
    allPlayerStatsDefence.set_index('player', inplace=True)
    allPlayerStatsPossesion.set_index('player', inplace=True)
    allPlayerStatsMisc.set_index('player', inplace=True)
    
    allPlayerAllStats = allPlayerStatsSummary
    
    for col in allPlayerStatsPassing.columns:
        if col not in allPlayerAllStats.columns:
            allPlayerAllStats = allPlayerAllStats.join(allPlayerStatsPassing[col])
            
    for col in allPlayerStatsPassingTypes.columns:
        if col not in allPlayerAllStats.columns:
            allPlayerAllStats = allPlayerAllStats.join(allPlayerStatsPassingTypes[col])
            
    for col in allPlayerStatsDefence.columns:
        if col not in allPlayerAllStats.columns:
            allPlayerAllStats = allPlayerAllStats.join(allPlayerStatsDefence[col])
            
    for col in allPlayerStatsPossesion.columns:
        if col not in allPlayerAllStats.columns:
            allPlayerAllStats = allPlayerAllStats.join(allPlayerStatsPossesion[col])
            
    for col in allPlayerStatsMisc.columns:
        if col not in allPlayerAllStats.columns:
            allPlayerAllStats = allPlayerAllStats.join(allPlayerStatsMisc[col])
    
    allPlayerAllStats = allPlayerAllStats.copy()
    allPlayerAllStats.reset_index(inplace=True)

    return matchStats, matchSquadsDF, allMatchShots, matchEventsDF, allPlayerAllStats, requestTime

    
def collectLeagueResults(URL, league, season, startPoint):
    import requests
    import time
    from bs4 import BeautifulSoup
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    matches = soup.select('div[id="content"] tbody tr')
    matchList = []
    matchStatList = []
    
    for i in range(len(matches)):
        matchWeek = matches[i].select('th')[0].text
        matchURL = matches[i].select('td[data-stat="score"]')
        if(matchURL[0].find('a')):
            matchList.append((matchWeek, matchURL[0].a['href']))


    requestsTimes = []


    for i, (matchweek, URL) in enumerate(matchList):
        if i >= startPoint:
            startTime = time.time()
            completeURL = 'https://fbref.com' + URL
            
            print("Match: ", i, "Matchweek: ", matchweek, " URL: ", URL)
            
            if len(requestsTimes) == 20:
                if time.time() - requestsTimes[0] < 60:
                    time.sleep(60 - (time.time() - requestsTimes[0]))
                    requestsTimes.pop(0)
                else:
                    requestsTimes.pop(0)
            
            matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, requestTime = collectMatch(completeURL, 
                                                                                                         league, season, matchweek)
            
            # zapis zebranych danych do csv
            
            matchStatsExisting = pd.read_csv(".\\MatchStats.csv", sep=";", encoding='UTF-8')
            matchSquadsExisting = pd.read_csv(".\\MatchSquads.csv", sep=";", encoding='UTF-8')
            matchShotsExisting = pd.read_csv(".\\MatchShots.csv", sep=";", encoding='UTF-8')
            matchEventsExisting = pd.read_csv(".\\MatchEvents.csv", sep=";", encoding='UTF-8')
            allPlayerStatsExisting = pd.read_csv(".\\AllPlayerStats.csv", sep=";", encoding='UTF-8')
            
            matchStatsExisting = pd.concat([matchStatsExisting, matchStats])
            matchSquadsExisting = pd.concat([matchSquadsExisting, matchSquads])
            matchShotsExisting = pd.concat([matchShotsExisting, matchShots])
            matchEventsExisting = pd.concat([matchEventsExisting, matchEvents])
            allPlayerStatsExisting = pd.concat([allPlayerStatsExisting, allPlayerStats])
            
            matchStatsExisting.to_csv(".\\MatchStats.csv", index=False, sep=";", encoding='UTF-8')
            matchSquadsExisting.to_csv(".\\MatchSquads.csv", index=False, sep=";", encoding='UTF-8')
            matchShotsExisting.to_csv(".\\MatchShots.csv", index=False, sep=";", encoding='UTF-8')
            matchEventsExisting.to_csv(".\\MatchEvents.csv", index=False, sep=";", encoding='UTF-8')
            allPlayerStatsExisting.to_csv(".\\AllPlayerStats.csv", index=False, sep=";", encoding='UTF-8')
    
            requestsTimes.append(requestTime)
            matchStatList.append(matchStats)
            
            endTime = time.time()
            print(endTime - startTime)

    return matchStatList


def collectLeagueResultsPastBundesliga(URL, league, season):
    import requests
    import time
    from bs4 import BeautifulSoup
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    matches = soup.select('div[id="content"] tbody tr')
    matchList = []
    matchStatList = []
    
    for i in range(len(matches)):
        matchWeek = matches[i].select('td')
        matchWeek = matchWeek[0].text
        #print(matchWeek)
        matchURL = matches[i].select('td[data-stat="score"]')
        if(matchURL[0].find('a')):
            matchList.append((matchWeek, matchURL[0].a['href']))


    requestsTimes = []

    for matchweek, URL in matchList:
        startTime = time.time()
        completeURL = 'https://fbref.com' + URL
        
        print("Matchweek: ", matchweek, " URL: ", URL)
        
        if len(requestsTimes) == 20:
            if time.time() - requestsTimes[0] < 60:
                time.sleep(60 - (time.time() - requestsTimes[0]))
                requestsTimes.pop(0)
            else:
                requestsTimes.pop(0)
        
        
        matchStats, requestTime = collectMatch(completeURL, league, season, matchweek)
        
        
        requestsTimes.append(requestTime)
        matchStatList.append(matchStats)
        
        endTime = time.time()
        print(endTime - startTime)

    return matchStatList
    



import pandas as pd
import time

URL = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
data = collectLeagueResults(URL, 'PremierLeague', '23_24', 165)



#URL = 'https://fbref.com/en/matches/3a6836b4/Burnley-Manchester-City-August-11-2023-Premier-League'
#matchStats, matchSquads, matchShots, matchEvents, allPlayerStats, rt = collectMatch(URL, "PremierLeague", "23_24", 1)



#matchStats.to_csv(".\\MatchStats.csv", index=False, sep=";", encoding='UTF-8')
#matchSquads.to_csv(".\\MatchSquads.csv", index=False, sep=";", encoding='UTF-8')
#matchShots.to_csv(".\\MatchShots.csv", index=False, sep=";", encoding='UTF-8')
#matchEvents.to_csv(".\\MatchEvents.csv", index=False, sep=";", encoding='UTF-8')
#allPlayerStats.to_csv(".\\AllPlayerStats.csv", index=False, sep=";", encoding='UTF-8')









