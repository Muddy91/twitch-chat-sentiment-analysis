import socket
import re
import requests
from time import sleep
from lib.alchemyapi import AlchemyAPI
from lib.config import *

def sentiment(message):
    response = alchemyapi.sentiment("text", message)
    try:
        sentim = str(response["docSentiment"]["type"])
        try:
            score = str(response["docSentiment"]["score"])
        except KeyError:
            score = '0'
    except KeyError:
        sentim = "Error"
        score = '0'

    return sentim,score

alchemyapi = AlchemyAPI()

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(AUTHORIZATION).encode("utf-8"))
s.send("NICK {}\r\n".format(NICKNAME).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHANNEL).encode("utf-8"))

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

with open('out.csv','a') as output:
    output.write('username,message,sentiment,confidence\n')
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = (re.search(r"\w+", response).group(0)).encode('utf8')
            message = (CHAT_MSG.sub("", response)[:-2]).encode('utf8')
            if not 'tmi.twitch.tv' in message:
                results = sentiment(message)
                print [username, message, results[0], results[1]]
                output.write(username+','+message+','+results[0]+','+results[1]+'\n')
        sleep(REFRESH_RATE)