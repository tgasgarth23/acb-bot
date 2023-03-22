# all the import statements
import os
import sys
from time import gmtime, strftime
from bs4 import BeautifulSoup
import requests
import random
from flask import Flask, request
from pathlib import Path
from datetime import datetime
import pytz
import textwrap
import openai


# global variables to be used by the app later.
app = Flask(__name__)
location_coords = {'x': '42.372400734', 'y': '-72.516410713'}
location_name = "Amherst"

@app.route('/', methods=['POST'])
def webhook():
    # get the message from the POST request
    data = request.get_json()

    # parse the data that we got from the POST request

    msg = parse_message(data)
    if type(msg).__name__ == 'list':
        for i in msg:
            send_message(i)
    else:
    
    # send the message that we just got from parsing the input
        send_message(msg)

    # return the correct code
    return "ok", 200


def parse_message(data):
    '''
    This is where you are going to branch for any commands that you add.
    This could really be re-worked but this is what got brobot to where he is today
    '''
    # get the actual text from the message that was sent in the chat
    receivedMessage = data['text'].split('\n')
    print(f"RECEIVED MESSAGE:{receivedMessage}")
    print(f"EDITED MESSAGE:{receivedMessage[0].lower().strip()}")
    # branch to the correct function according to the text that we got
    if receivedMessage[0].lower().strip() == '!weather':
        msg = getWeather()
    elif receivedMessage[0].lower().strip() == '!hello':
        msg = "Hey {}!".format(data['name'])
    elif receivedMessage[0].lower().strip() == '!quote':
        msg = getQuote()
    elif receivedMessage[0].lower().strip() == '!fun':
        msg = getFun()
    elif receivedMessage[0].lower().strip() == '!news':
        msg = getNews()
    elif receivedMessage[0].lower().strip() == '!breakfast':
        msg = getMeal('Breakfast')
    elif receivedMessage[0].lower().strip() == '!lunch':
        msg = getMeal('Lunch')
    elif receivedMessage[0].lower().strip() == '!dinner':
        msg = getMeal('Dinner')
    elif receivedMessage[0].lower().strip() == '!latenight':
        msg = getMeal('Late-Night')
    elif receivedMessage[0].lower().strip() == '!gng':
        msg = getGNG()
    elif receivedMessage[0].lower().strip() == '!ligma':
        msg = getLigma()
    elif receivedMessage[0].lower().strip() == '!communism':
        msg = getCommunism()
    elif '!chat' in receivedMessage[0].lower().strip():
        msg = aiBot(receivedMessage)
    elif receivedMessage[0].lower().strip() == '!help':
        msg = getHelp()
    elif receivedMessage[0].lower().strip() == '!loop':
        msg = getLoop() 
    return msg


def aiBot(input):
    
    input = input[0]
    input = input[6:]
    # print(f"Input:\t{input} \n")
    api_key = os.getenv('API')
    openai.organization = 'org-9JJxC5Dd7efT1PTXawq62Hl9'
    openai.api_key = api_key
    response = openai.Completion.create(
    model = 'text-davinci-003',
    prompt = input,
    max_tokens = 4020
    )
    # print(response)
    response = response.get('choices')[0].get('text')
    response = response.strip()
    arr = []
    while len(response) > 0:
        if len(response) > 1000:
            arr.append(response[:1000])
            response = response[1000:]
        else:
            arr.append(response)
            response = ''
    return arr


def getHelp():
    msg = '''
BrotherBot v1.13.0 Commands:

"!Weather" - Get the current and future weather for Amherst College

"!Hello" - Just to say hi

"!Quote" - To hear a quote

"!Fun" - To get the weekend's schedule

"!Breakfast/Lunch/Dinner/LateNight" - Get the Valentine Dining Hall meals for the specified meal

"!gng" - Get the Grab and Go Menu for the day

"!News" - Get the latest Mammo news letter

"!Communism" - Learn about the economic theory of Communism

"!Chat 'Your input'" - Chat with an ai bot

"!Loop" - Who has loop responsibility today

"!Help" - To get BroBot commands
    '''
    return msg

def send_message(msg):
    ''' This message literally just sends (the parameter) to the groupchat'''

    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': os.getenv('GROUPME_BOT_ID'),
        'text': msg,
        }

    requests.post(url, json=data)

def getWeather():
    '''
    Scrape the weather API to see what the weather is like in Amherst.
    You can probably generalize the location if you wanted, but it would be more work to get
    any other place except amherst.
    
    NOTE: There are hardcoded variables at the top of this file that get this to work.
    '''

    # request the data
    r = requests.get('https://api.weather.gov/points/' + location_coords['x'] + ',' + location_coords['y'] + '/forecast')
    weather_response = r.json()

    # parse out the current weather from the API response
    current_weather = weather_response['properties']['periods'][0]['detailedForecast']
    weather_time = weather_response['properties']['periods'][0]['name']

    # parse out the future weather from the API response
    future_weather = weather_response['properties']['periods'][1]['detailedForecast']
    future_weather_time = weather_response['properties']['periods'][1]['name']

    # This is the final message
    msg = "The " + weather_time + " forecast in " + location_name + ": " + current_weather + "\n\n"
    msg += "The " + future_weather_time + " forecast in " + location_name + ": " + future_weather

    return msg


def getMeal(meal):
    '''
    This is the function to get the current meal. If they change the meal website, this will be broken.
    '''
    url = 'https://amherst.nutrislice.com/menu/valentine-hall/'
    mealurl = url + meal + '/print-menu/month/' + datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d')
    return mealurl

def getGNG():
    '''
    This is the function to get the current meal. If they change the meal website, this will be broken.
    '''
    msg = 'Not working' 
    return msg

def getQuote():

    '''
    This is the function to get an AP quote
    '''
    quotes = ["All baseball players are at least 25% Gay", "LIMOAAANNNNN", "Starting to think that ACB deserves the hate!", "LeAdErShIp OpPoRtUnItY"]
    msg = random.choice(quotes)
    return msg

def getFun():

    '''
    This is the function to get the upcoming weekend schedule'
    '''
    
    print("Fun function called")
    
    msg = 'Ask Newbie'

    return msg

def getNews():
    msg = 'Shut up Dove'
    return msg

def getLigma():
    msg = 'ligma balls bitch @Robin'
    return msg

def getCommunism():
    msg = 'https://en.wikipedia.org/wiki/Red_Terror\n' \
          'https://en.wikipedia.org/wiki/Soviet_famine_of_1930%E2%80%931933\n' \
          'https://en.wikipedia.org/wiki/Great_Purge\n' \
          'https://en.wikipedia.org/wiki/Soviet_war_crimes\n' \
          'https://en.wikipedia.org/wiki/Great_Chinese_Famine\n' \
          'https://en.wikipedia.org/wiki/1989_Tiananmen_Square_protests_and_massacre'
    return msg

def getLoop():
    msg = 'Naav has loops responsibility today'
    return msg