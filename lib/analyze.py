from alchemyapi import AlchemyAPI
from config import *
from sys import stdout



#Collection to hold meta data for time-slot analytics
meta_collection = []
#Setting up API for sentiment analysis
alchemyapi = AlchemyAPI()
#Counter for checking if API is still responsive
error_counter = 0
#Global holder for the previous output
prev_out = ''


#Function to perform sentiment analysis on a given chat message
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

#Function to update the meta collection
def update(index, sentiment, confidence):
    global error_counter

    if len(meta_collection) - 1 < index:
        meta_collection.append(META_EMPTY)

    if sentiment == 'positive':
        meta_collection[index]['pos'] += 1
        meta_collection[index]['posCon'] += confidence
        error_counter = 0

    elif sentiment == 'neutral':
        meta_collection[index]['neu'] += 1
        meta_collection[index]['neuCon'] += confidence
        error_counter = 0

    elif sentiment == 'negative':
        meta_collection[index]['neg'] += 1
        meta_collection[index]['negCon'] += confidence
        error_counter = 0

    else:
        meta_collection[index]['Error'] += 1
        error_counter += 1
        if error_counter == MAX_ERROR_COUNT:
            print('Recieved too many error messages from the API\nExiting program...')

def printMeta(index):
    global prev_out
    stdout.write('\r' + ' '*len(prev_out))
    stdout.flush()
    new_out = str(meta_collection[index])
    stdout.write("\r%s" % new_out)
    stdout.flush()
    prev_out = new_out
