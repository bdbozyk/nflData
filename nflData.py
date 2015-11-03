'''
This module takes gameIds from nfl.com and turns them into structure data
    sets of individual and team stats, as well as structure play by play
    data.
'''

import urllib
import json
import os
import csv

def dicter(rows,someDict,columns):
    if len(columns) == 0:
        columns = ['playerId']
    for index, row in enumerate(rows):
        if index == 0:
            header = row
            for column in row:
                if column not in columns:
                    columns.append(column)
        else:
            playerId = row[3]
            if playerId not in someDict:
                someDict[playerId] = {}

            for statIndex, stat in enumerate(row):
                if (header[statIndex]!='playerId') and (header[statIndex] not in someDict[playerId]):
                    someDict[playerId][header[statIndex]] = stat

    return someDict, columns


class game():
    '''This module takes gameIds from nfl.com and turns them into structure
    datasets of individual and team stats, as well as structured play by play
    data.'''

    def __init__(self, gameId):
        self.gameId = gameId

    def show(self):
        ''' Returns gameId.'''
        return self.gameId

    def jsonGetter(self):
        ''' Returns the json text that exists at nfl.com. The first time this
            is ran, jsonGetter will fetch from nfl.com and save a copy to
            disc. Every subsequent run will be pulled from the saved copy on
            disc.'''
        if 'json' not in os.listdir(os.getcwd()):
            os.mkdir('json')
            print('Making json directory...')
        if 'data' not in os.listdir(os.getcwd()):
            os.mkdir('data')
            print('Making data directory...')
        if '%s.json'%(self.show()) in os.listdir('%s/json/'%(os.getcwd())):
            f = open('%s/json/%s.json'%(os.getcwd(),self.show()),'r')
            text = f.read()
            f.close()
            print('Fetching data from disc...')
        else:
            text = urllib.urlopen('http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json'%(self.show(),self.show())).read()
            f = open('%s/json/%s.json'%(os.getcwd(),self.show()),'wb')
            f.write(text)
            f.close()
            print('Fetching data from nfl.com...')
        return json.loads(text)

    def teams(self):
        '''  Returns of tuple of (awayTeam, homeTeam).'''
        jsonText = self.jsonGetter()
        return jsonText[self.show()]['away']['abbr'], jsonText[self.show()]['home']['abbr']

    def passing(self):
        ''' Returns a list of lists of passing data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = []
        header = ['gameId','team','homeAway','playerId','player','passAtts','passCmps','passYds','passInts','passTds','pass2PtAtts','pass2PtCmps']
        rows.append(header)
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'passing'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['att'],          # passAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['cmp'],          # passCmps
                       jsonText[self.show()][team]['stats'][stat][playerId]['yds'],          # passYds
                       jsonText[self.show()][team]['stats'][stat][playerId]['ints'],         # passInts
                       jsonText[self.show()][team]['stats'][stat][playerId]['tds'],          # passTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['twopta'],       # pass2PtAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['twoptm']        # pass2PtCmps
                       ]
                rows.append(row)
        return rows


    def rushing(self):
        ''' Returns a list of lists of rushing data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','rushAtts','rushYds','rushTds','rushLng','rushLngTds','rush2PtAtts','rush2PtCmps']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'rushing'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['att'],          # rushAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['yds'],          # rushYds
                       jsonText[self.show()][team]['stats'][stat][playerId]['tds'],          # rushTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['lng'],          # rushLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['lngtd'],        # rushLngTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['twopta'],       # rush2PtAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['twoptm']        # rush2PtCmps
                       ]
                rows.append(row)
        return rows


    def receiving(self):
        ''' Returns a list of lists of receiving data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','recs','recYds','recTds','recLng','recLngTds','rec2PtAtts','rec2PtCmps']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'receiving'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['rec'],          # recs
                       jsonText[self.show()][team]['stats'][stat][playerId]['yds'],          # recYds
                       jsonText[self.show()][team]['stats'][stat][playerId]['tds'],          # recTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['lng'],          # recLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['lngtd'],        # recLngTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['twopta'],       # rec2PtAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['twoptm']        # rec2PtCmps
                       ]
                rows.append(row)
        return rows

    def punting(self):
        ''' Returns a list of lists of punting data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','punts','puntYds','puntLng','puntAvg']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'punting'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['pts'],          # punts
                       jsonText[self.show()][team]['stats'][stat][playerId]['yds'],          # puntYds
                       jsonText[self.show()][team]['stats'][stat][playerId]['lng'],          # puntLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['avg']           # puntAvg
                       ]
                rows.append(row)
        return rows

    def kicking(self):
        ''' Returns a list of lists of kicking data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','fgPts','fgAtts','fgCmps','fgLng','xpAtts','xpBlkd','xpCmps','xpMiss','xpPts']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'kicking'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['totpfg'],       # fgPts
                       jsonText[self.show()][team]['stats'][stat][playerId]['fga'],          # fgAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['fgm'],          # fgCmps
                       jsonText[self.show()][team]['stats'][stat][playerId]['fgyds'],        # fgLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['xpa'],          # xpAtts
                       jsonText[self.show()][team]['stats'][stat][playerId]['xpb'],          # xpBlkd
                       jsonText[self.show()][team]['stats'][stat][playerId]['xpmade'],       # xpCmps
                       jsonText[self.show()][team]['stats'][stat][playerId]['xpmissed'],     # xpMiss
                       jsonText[self.show()][team]['stats'][stat][playerId]['xptot']         # xpPts
                       ]
                rows.append(row)
        return rows

    def kickReturns(self):
        ''' Returns a list of lists of kick return data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','krs','krTds','krLngTd','krLng','krAvg']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'kickret'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['ret'],          # krs
                       jsonText[self.show()][team]['stats'][stat][playerId]['tds'],          # krTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['lngtd'],        # krLngTd
                       jsonText[self.show()][team]['stats'][stat][playerId]['lng'],          # krLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['avg']           # krAvg
                      ]
                rows.append(row)
        return rows

    def puntReturns(self):
        ''' Returns a list of lists of punt return data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','prs','prTds','prLngTd','prLng','prAvg']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'puntret'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(), # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['ret'],          # prs
                       jsonText[self.show()][team]['stats'][stat][playerId]['tds'],          # prTds
                       jsonText[self.show()][team]['stats'][stat][playerId]['lngtd'],        # prLngTd
                       jsonText[self.show()][team]['stats'][stat][playerId]['lng'],          # prLng
                       jsonText[self.show()][team]['stats'][stat][playerId]['avg']           # prAvg
                      ]
                rows.append(row)
        return rows

    def fumbles(self):
        ''' Returns a list of lists of fumble data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','fumLosts','fumRecs','fumTots','fumTotsRecs','fumYds']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'fumbles'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(),  # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['lost'],          # fumLost
                       jsonText[self.show()][team]['stats'][stat][playerId]['rcv'],           # fumRecs
                       jsonText[self.show()][team]['stats'][stat][playerId]['tot'],           # fumTots
                       jsonText[self.show()][team]['stats'][stat][playerId]['trcv'],          # fumTotsRecs
                       jsonText[self.show()][team]['stats'][stat][playerId]['yds']            # fumYds
                      ]
                rows.append(row)
        return rows

    def defense(self):
        ''' Returns a list of lists of defense data.'''
        jsonText = self.jsonGetter()
        awayTeam, homeTeam = self.teams()
        rows = [['gameId','team','homeAway','playerId','player','defAsts','defFumFrcd','defInts','defSacks','defTkls']]
        for team, teamName in [('away',awayTeam),('home',homeTeam)]:
            stat = 'defense'
            for playerId in jsonText[self.show()][team]['stats'][stat]:
                row = [self.show(),
                       teamName,
                       team.upper(),
                       playerId,
                       jsonText[self.show()][team]['stats'][stat][playerId]['name'].upper(),  # player
                       jsonText[self.show()][team]['stats'][stat][playerId]['ast'],           # defAsts
                       jsonText[self.show()][team]['stats'][stat][playerId]['ffum'],          # defFumFrcd
                       jsonText[self.show()][team]['stats'][stat][playerId]['int'],           # defInts
                       jsonText[self.show()][team]['stats'][stat][playerId]['sk'],            # defSacks
                       jsonText[self.show()][team]['stats'][stat][playerId]['tkl']            # defTkls
                      ]
                rows.append(row)
        return rows





    def allIndividualStats(self,write=True):
        ''' Returns a list of lists for all available individual players stats.
            By default, write is set to True, which will
            write the data to a csv in /data/individual. Set write=False to bypass
            this feature.'''
        if 'individual' not in os.listdir('%s/data/'%(os.getcwd())):
                os.mkdir('%s/data/individual/'%(os.getcwd()))
        dataDict = {}
        columns = []
        dataDict, columns = dicter(self.passing(),     dataDict, columns)
        dataDict, columns = dicter(self.receiving(),   dataDict, columns)
        dataDict, columns = dicter(self.rushing(),     dataDict, columns)
        dataDict, columns = dicter(self.puntReturns(), dataDict, columns)
        dataDict, columns = dicter(self.kickReturns(), dataDict, columns)
        dataDict, columns = dicter(self.punting(),     dataDict, columns)
        dataDict, columns = dicter(self.kicking(),     dataDict, columns)
        dataDict, columns = dicter(self.fumbles(),     dataDict, columns)
        dataDict, columns = dicter(self.defense(),     dataDict, columns)
        data = [columns]
        for playerId in dataDict:
            row = [playerId]
            for column in columns[1:]:
                if column in dataDict[playerId]:
                    row.append(dataDict[playerId][column])
                else:
                    row.append(0)
            data.append(row)

        with open('%s/data/individual/%s.csv'%(os.getcwd(),str(gameId)),'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        f.close()
        return data

def jsonGetter(gameId):
    ''' Given a gameId, this program will either open the json file
        from disk, or go out to nfl.com and retrieve it. It also checks
        your current working directory for a data directory and a json
        directory. If they don't exist, jsonGetter will create them.

        ex: jsonText = jsonGetter('2015102506')
        '''
    if 'json' not in os.listdir(os.getcwd()):
        os.mkdir('json')
    if 'data' not in os.listdir(os.getcwd()):
        os.mkdir('data')
    if '%s.json'%(gameId) in os.listdir('%s/json/'%(os.getcwd())):
        f = open('%s/json/%s.json'%(os.getcwd(),gameId),'r')
        text = f.read()
        f.close()
    else:
        text = urllib.urlopen('http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json'%(gameId,gameId)).read()
        f = open('%s/json/%s.json'%(os.getcwd(),gameId),'wb')
        f.write(text)
        f.close()
    return json.loads(text)

def teams(gameId):
    '''
    Given a gameId, teams will output a tuple of
    (awayTeam, homeTeam).

    ex:
    >>> awayTeam, homeTeam = teams('2015102506')
    >>> (u'MIN',u'DET')
    '''
    jsonText = jsonGetter(gameId)
    return jsonText[gameId]['away']['abbr'], jsonText[gameId]['home']['abbr']

def passing(gameId):
    ''' Takes a gameId and creates a list of lists with individual passing
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = []
    header = ['gameId','team','homeAway','playerId','player','passAtts','passCmps','passYds','passInts','passTds','pass2PtAtts','pass2PtCmps']
    rows.append(header)
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'passing'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['att'],          # passAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['cmp'],          # passCmps
                   jsonText[gameId][team]['stats'][stat][playerId]['yds'],          # passYds
                   jsonText[gameId][team]['stats'][stat][playerId]['ints'],         # passInts
                   jsonText[gameId][team]['stats'][stat][playerId]['tds'],          # passTds
                   jsonText[gameId][team]['stats'][stat][playerId]['twopta'],       # pass2PtAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['twoptm']        # pass2PtCmps
                   ]
            rows.append(row)
    return rows

def rushing(gameId):
    ''' Takes a gameId and creates a list of lists with individual rushing
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','rushAtts','rushYds','rushTds','rushLng','rushLngTds','rush2PtAtts','rush2PtCmps']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'rushing'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['att'],          # rushAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['yds'],          # rushYds
                   jsonText[gameId][team]['stats'][stat][playerId]['tds'],          # rushTds
                   jsonText[gameId][team]['stats'][stat][playerId]['lng'],          # rushLng
                   jsonText[gameId][team]['stats'][stat][playerId]['lngtd'],        # rushLngTds
                   jsonText[gameId][team]['stats'][stat][playerId]['twopta'],       # rush2PtAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['twoptm']        # rush2PtCmps
                   ]
            rows.append(row)
    return rows

def receiving(gameId):
    ''' Takes a gameId and creates a list of lists with individual receiving
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','recs','recYds','recTds','recLng','recLngTds','rec2PtAtts','rec2PtCmps']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'receiving'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['rec'],          # recs
                   jsonText[gameId][team]['stats'][stat][playerId]['yds'],          # recYds
                   jsonText[gameId][team]['stats'][stat][playerId]['tds'],          # recTds
                   jsonText[gameId][team]['stats'][stat][playerId]['lng'],          # recLng
                   jsonText[gameId][team]['stats'][stat][playerId]['lngtd'],        # recLngTds
                   jsonText[gameId][team]['stats'][stat][playerId]['twopta'],       # rec2PtAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['twoptm']        # rec2PtCmps
                   ]
            rows.append(row)
    return rows

def punting(gameId):
    ''' Takes a gameId and creates a list of lists with individual punting
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','punts','puntYds','puntLng','puntAvg']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'punting'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['pts'],          # punts
                   jsonText[gameId][team]['stats'][stat][playerId]['yds'],          # puntYds
                   jsonText[gameId][team]['stats'][stat][playerId]['lng'],          # puntLng
                   jsonText[gameId][team]['stats'][stat][playerId]['avg']           # puntAvg
                   ]
            rows.append(row)
    return rows

def kicking(gameId):
    ''' Takes a gameId and creates a list of lists with individual kicking
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','fgPts','fgAtts','fgCmps','fgLng','xpAtts','xpBlkd','xpCmps','xpMiss','xpPts']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'kicking'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['totpfg'],       # fgPts
                   jsonText[gameId][team]['stats'][stat][playerId]['fga'],          # fgAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['fgm'],          # fgCmps
                   jsonText[gameId][team]['stats'][stat][playerId]['fgyds'],        # fgLng
                   jsonText[gameId][team]['stats'][stat][playerId]['xpa'],          # xpAtts
                   jsonText[gameId][team]['stats'][stat][playerId]['xpb'],          # xpBlkd
                   jsonText[gameId][team]['stats'][stat][playerId]['xpmade'],       # xpCmps
                   jsonText[gameId][team]['stats'][stat][playerId]['xpmissed'],     # xpMiss
                   jsonText[gameId][team]['stats'][stat][playerId]['xptot']         # xpPts
                   ]
            rows.append(row)
    return rows

def kickReturns(gameId):
    ''' Takes a gameId and creates a list of lists with individual kick returns
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','krs','krTds','krLngTd','krLng','krAvg']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'kickret'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['ret'],          # krs
                   jsonText[gameId][team]['stats'][stat][playerId]['tds'],          # krTds
                   jsonText[gameId][team]['stats'][stat][playerId]['lngtd'],        # krLngTd
                   jsonText[gameId][team]['stats'][stat][playerId]['lng'],          # krLng
                   jsonText[gameId][team]['stats'][stat][playerId]['avg']           # krAvg
                  ]
            rows.append(row)
    return rows

def puntReturns(gameId):
    ''' Takes a gameId and creates a list of lists with individual kick returns
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','prs','prTds','prLngTd','prLng','prAvg']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'puntret'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(), # player
                   jsonText[gameId][team]['stats'][stat][playerId]['ret'],          # prs
                   jsonText[gameId][team]['stats'][stat][playerId]['tds'],          # prTds
                   jsonText[gameId][team]['stats'][stat][playerId]['lngtd'],        # prLngTd
                   jsonText[gameId][team]['stats'][stat][playerId]['lng'],          # prLng
                   jsonText[gameId][team]['stats'][stat][playerId]['avg']           # prAvg
                  ]
            rows.append(row)
    return rows

def fumbles(gameId):
    ''' Takes a gameId and creates a list of lists with individual fumble
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','fumLosts','fumRecs','fumTots','fumTotsRecs','fumYds']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'fumbles'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(),  # player
                   jsonText[gameId][team]['stats'][stat][playerId]['lost'],          # fumLost
                   jsonText[gameId][team]['stats'][stat][playerId]['rcv'],           # fumRecs
                   jsonText[gameId][team]['stats'][stat][playerId]['tot'],           # fumTots
                   jsonText[gameId][team]['stats'][stat][playerId]['trcv'],          # fumTotsRecs
                   jsonText[gameId][team]['stats'][stat][playerId]['yds']            # fumYds
                  ]
            rows.append(row)
    return rows

def defense(gameId):
    ''' Takes a gameId and creates a list of lists with individual defense
        statistics for that game.'''
    jsonText = jsonGetter(gameId)
    awayTeam, homeTeam = teams(gameId)
    rows = [['gameId','team','homeAway','playerId','player','defAsts','defFumFrcd','defInts','defSacks','defTkls']]
    for team, teamName in [('away',awayTeam),('home',homeTeam)]:
        stat = 'defense'
        for playerId in jsonText[gameId][team]['stats'][stat]:
            row = [gameId,
                   teamName,
                   team.upper(),
                   playerId,
                   jsonText[gameId][team]['stats'][stat][playerId]['name'].upper(),  # player
                   jsonText[gameId][team]['stats'][stat][playerId]['ast'],           # defAsts
                   jsonText[gameId][team]['stats'][stat][playerId]['ffum'],          # defFumFrcd
                   jsonText[gameId][team]['stats'][stat][playerId]['int'],           # defInts
                   jsonText[gameId][team]['stats'][stat][playerId]['sk'],            # defSacks
                   jsonText[gameId][team]['stats'][stat][playerId]['tkl']            # defTkls
                  ]
            rows.append(row)
    return rows



def dicter(rows,someDict,columns):
    if len(columns) == 0:
        columns = ['playerId']
    for index, row in enumerate(rows):
        if index == 0:
            header = row
            for column in row:
                if column not in columns:
                    columns.append(column)
        else:
            playerId = row[3]
            if playerId not in someDict:
                someDict[playerId] = {}

            for statIndex, stat in enumerate(row):
                if (header[statIndex]!='playerId') and (header[statIndex] not in someDict[playerId]):
                    someDict[playerId][header[statIndex]] = stat

    return someDict, columns

def allIndividualStats(gameId,write=True):
    '''Takes a gameId and returns a list of lists consisting of all individual
       player stats for that game. By default, write is set to True, which will
       write the data to a csv in /data/individual. Set write=False to bypass
       this feature.'''
    if 'individual' not in os.listdir('%s/data/'%(os.getcwd())):
            os.mkdir('%s/data/individual/'%(os.getcwd()))
    dataDict = {}
    columns = []
    dataDict, columns = dicter(passing(gameId),     dataDict, columns)
    dataDict, columns = dicter(receiving(gameId),   dataDict, columns)
    dataDict, columns = dicter(rushing(gameId),     dataDict, columns)
    dataDict, columns = dicter(puntReturns(gameId), dataDict, columns)
    dataDict, columns = dicter(kickReturns(gameId), dataDict, columns)
    dataDict, columns = dicter(punting(gameId),     dataDict, columns)
    dataDict, columns = dicter(kicking(gameId),     dataDict, columns)
    dataDict, columns = dicter(fumbles(gameId),     dataDict, columns)
    dataDict, columns = dicter(defense(gameId),     dataDict, columns)
    data = [columns]
    for playerId in dataDict:
        row = [playerId]
        for column in columns[1:]:
            if column in dataDict[playerId]:
                row.append(dataDict[playerId][column])
            else:
                row.append(0)
        data.append(row)

    with open('%s/data/individual/%s.csv'%(os.getcwd(),str(gameId)),'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    f.close()
    return data














