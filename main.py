import socket
import requests
import re
from time import sleep,time
from lib.config import *
from lib.analyze import *


#Setting up connection with Twitch
s = socket.socket()
try:
    s.connect((HOST, PORT))
except socket.gaierror:
    print 'Error connecting to Twitch\nExiting program...'
    quit()
s.send("PASS {}\r\n".format(AUTHORIZATION).encode("utf-8"))
s.send("NICK {}\r\n".format(NICKNAME).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHANNEL).encode("utf-8"))

#Setting up start time for use in time-slot analytics
start_time = time()

with open('data/sentiment-log_'+CHANNEL+'_'+str(int(start_time))+'.csv','a') as output:
    output.write('username,message,sentiment,confidence\n')
    while True:
        #Getting response (and response time)
        response = s.recv(1024).decode("utf-8")
        message_time = time()

        #Sending Twitch a pong message if a ping message arrives to maintain connection
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

        #If not a ping, check into the contents of the message
        else:
            #Splitting data into username and message content
            username = (re.search(r"\w+", response).group(0)).encode('utf8')
            message = (CHAT_MSG.sub("", response)[:-2]).encode('utf8')

            #Analyze and output if not a Twitch API message
            if not 'tmi.twitch.tv' in message:
                #Analysis occurs here
                sent,confidence = sentiment(message)

                #Output
                #print [username, message, sent, confidence]
                output.write(username+','+message+','+sent+','+confidence+'\n')

                #Updating meta data
                index = int((message_time - start_time)/ANALYSIS_TIME_FRAME)
                update(index, sent, float(confidence))
                printMeta(index)

        #Added refresh rate to limit hitting Twitch
        sleep(REFRESH_RATE)