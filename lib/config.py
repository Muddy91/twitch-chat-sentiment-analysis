import re


#Twitch setup
HOST = "irc.twitch.tv"	#Twitch API host IP
PORT = 6667		#Twitch API host port
NICKNAME = "sentiment_bot"	#Twitch username
AUTHORIZATION = "oauth:rmd0q99k20szlghys0cgsf9r6thl02"	#Twitch auth token from http://www.twitchapps.com/tmi/
CHANNEL = "#officialhhi"	#Twitch channel to read chat from

#Analytics variables
REFRESH_RATE = 0	#Time in seconds that the process will sleep to check for another message
ANALYSIS_TIME_FRAME = 60	#Time in seconds that the program will perform meta-data analysis
MAX_ERROR_COUNT = 10	#Maximum amount of errors the API can send in a row before exiting the program
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")	#Reg expression for filtering out chat messages
META_EMPTY = {'pos': 0, 'neg' : 0, 'neu' : 0, 'posCon' : 0, 'negCon' : 0, 'neuCon' : 0, 'Error' : 0}	#Empty dictionary for keeping track of live meta data