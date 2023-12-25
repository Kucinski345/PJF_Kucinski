def collectMatch(URL, league, season, matchweek):
    import requests
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    pd.options.display.max_columns = None
    
    page = requests.get(URL)
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
    
    
    return matchStats

    
def collectLeagueResults(URL, league, season):
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

    for matchweek, URL in matchList:
        startTime = time.time()
        completeURL = 'https://fbref.com' + URL
        
        print("Matchweek: ", matchweek, " URL: ", URL)
        matchStats = collectMatch(completeURL, league, season, matchweek)
        matchStatList.append(matchStats)
        
        endTime = time.time()
        print(endTime - startTime)
        while(endTime - startTime < 3.01):
            endTime = time.time()

    return matchStatList

    
import pandas as pd

URL = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
data = collectLeagueResults(URL, 'PremierLeague', '23_24')

data = pd.concat(data)
data.reset_index()
data.to_csv(".\\PL_23_24_MatchStats.csv", index=False, sep=";", encoding='UTF-8')









