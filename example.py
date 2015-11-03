import os
# change the working directory to the one containing the nflData repository
os.chdir('/home/brett/nflData/')

import nflData as nfl
gameId = '2015102506'


# Method 1: Call an instance of a game, and use its methods to get data
g = nfl.game(gameId)
# Each of the following returns a list of lists of the data
g.teams()
g.passing()
g.rushing()
g.receiving()
g.puntReturns()
g.kickReturns()
g.punting()
g.kicking()
g.fumbles()
g.defense()
# This returns and writes a flat file of indiviual data
g.allIndividualStats()

# Read it into a pandas DataFrame
import pandas as pd
theData = g.allIndividualStats()
header = theData.pop(0)
df = pd.DataFrame(theData,columns=header)
print df.head()


# Method 2: Call individual functions, given the gameId
nfl.teams(gameId)
nfl.passing(gameId)
# ...
nfl.allIndividualStats(gameId)
# etc.

# Note: As soon as you call any function using a gameId, a copy of the
#       json file will be writen to a json directory in your working
#       directory.
# Note: Any time you call allIndividualStats, a csv file containing the
#       structured data will be writen to your data directory in your
#       current working directory. (That is, unless you specify write=False in
#       the function.)