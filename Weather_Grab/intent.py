#!/usr/bin/env python

from __future__ import print_function
from alchemyapi import AlchemyAPI
from weather import Weather
import json
import sys

class Intent:
    def __init__(self):

        ##### Input file, can either be modified manually or with another program.
        fo = open("answer.txt", "r")
        text = open("answer.txt").read().splitlines()
        index = len(text) - 1

        ##### Because I was working with a file that was updated very frequently, 
        ##### I grab the most recent expression in the file.
        text = text[index]
        fo.close()

        #### API instance creation
        alchemyapi = AlchemyAPI()
        print(text)
        print('')

        isCity = False
        isWeather = False
        wasIn = False

        #### If there is no city name in our input, program asks for a city name until you specify one.
        #### NOTICE: enter the city name between quotation marks. e.g. "Paris"
        while (not isCity) or (not isWeather):

            ##### This is not the best solution ever, will update when I come up with a new one :P
            if wasIn:
                test = input("WHERE?")
                print(test)
                text = text + " " + test

            # JSON result which has the intents we're looking for.
            response = alchemyapi.combined('text', text)
            # Uncomment the line below for the JSON result.
            #print(json.dumps(response, indent=4))

            ##### If the sentence is not related with weather, an exception is thrown
            if response['taxonomy']:
                for x in response['taxonomy']:
                    if "weather" in x['label']:
                        isWeather = True
                        break

            # A temporary solution for simple cases.
            if "FORECAST" in text:
                isWeather = True
            elif "SUNNY" in text:
                isWeather = True
            elif "RAINY" in text:
                isWeather = True

            ##### Distinguishing between cities and countries in order to prevent troubles
            if response['entities']:
                for x in response['entities']:
                    if "City" in x['type']:
                        isCity = True
                        break
            wasIn = True

            ##### Variables below are passed to weather.py for further usage.
            try:
                if isCity:
                    self.city = response['entities'][0]['text'] #city name
            except:
                self.city = ""

            try:
                self.total_days = response['entities'][1]['text']
            except:
                self.total_days = "TODAY"
        pass

    def start(self):
        wth = Weather()
        return wth.get_forecast(self.city, self.total_days)
