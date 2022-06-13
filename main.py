import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import requests
import time

projectToken = "tL-KCDn-UBBj"
runToken = "tES-WUC4nh6S"
apiKey = "tY5NFz4vMrpK"


class covidData:
    def __init__(self, apiKey, projectToken):
        self.projectToken = projectToken
        self.apiKey = apiKey
        self.params = {"api_key": self.apiKey}
        self.serverData = self.retrieveData()

    def retrieveData(self):
        serverRequest = requests.get(f'https://www.parsehub.com/api/v2/projects/{projectToken}/last_ready_run/data', params=self.params) #contains the updated version of cases
        serverData = json.loads(serverRequest.text)
        return serverData

    def totalCases(self):
        cases = self.serverData['total']
        for info in cases:
            if "Coronavirus Cases:" == info['name']:
                return info['amount']
    
    def totalDeaths(self):
        deaths = self.serverData['total']
        for info in deaths:
            if "Deaths:" == info['name']:
                return info['amount']

    def totalRecovered(self):
        recovered = self.serverData['total']
        for info in recovered:
            if "Recovered:" == info['name']:
                return info['amount']

    def countrySpecific(self, region):
        countryInfo = self.serverData["countries"]
        for info in countryInfo:
            if region.lower() == info['name'].lower():
                return info

    def countryList(self):
        all_countries = []
        for country in self.serverData["countries"]:
            all_countries.append(country['name'].lower())
        return all_countries

    def get_updated_data(self):
        serverRequest = requests.post(f'https://www.parsehub.com/api/v2/projects/{projectToken}/run', params=self.params)

        def poll():
            time.sleep(0.1)
            previous_data = self.serverData
            while True:
                new_data = self.retrieveData()
                if new_data != previous_data:
                    self.serverData = new_data
                    print("Data has been updated.")
                    break
                time.sleep(5)



        new_thread = threading.Thread(target=poll) 
        new_thread.start()


def talk_to_user(text):
    tts = pyttsx3.init()
    tts.say(text)
    tts.runAndWait()

def retrive_voice():
    record = sr.Recognizer()
    with sr.Microphone() as audio:
        sound = record.listen(audio) #records the audio
        heard = "" #stores what is recorded from the audio

        try:
            heard = record.recognize_google(sound) #converts audio into a string of what is said
        except Exception as error:
            print("Exception: ", str(error)) #if something goes wrong, print an exception
    return heard.lower()

def main():
    print("Program Started")
    covid_data = covidData(apiKey, projectToken)
    stop_word = "end program"
    update_word = "update program"
    country_list = covid_data.countryList()
    regex_patterns = {
        re.compile("[\w\s]+ total [\w\s]+ cases"):covid_data.totalCases,
        re.compile("[\w\s]+ total cases"):covid_data.totalCases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"):covid_data.totalDeaths,
        re.compile("[\w\s]+ total deaths"):covid_data.totalDeaths,
        re.compile("[\w\s]+ total [\w\s]+ recovered"):covid_data.totalRecovered,
        re.compile("[\w\s]+ total recovered"):covid_data.totalRecovered
    }

    country_regex = {
        re.compile("[\w\s]+ total cases [\w\s]+"):lambda country: covid_data.countrySpecific(country)['totalCases'],
        re.compile("[\w\s]+ deaths [\w\s]+"):lambda country: covid_data.countrySpecific(country)['totalDeaths'],
        re.compile("[\w\s]+ recovered [\w\s]+"):lambda country: covid_data.countrySpecific(country)['totalRecovered'],
        re.compile("[\w\s]+ active cases [\w\s]+"):lambda country: covid_data.countrySpecific(country)['activeCases'],
        re.compile("[\w\s]+ critical cases [\w\s]+"):lambda country: covid_data.countrySpecific(country)['seriousCritical']
    }


    isCountry = False
    while True:
        print("Listening...")
        heard = retrive_voice()
        print(heard)
        found_func = None
        isCountry = False

        for pattern, function in country_regex.items():
            if pattern.match(heard.replace('.','')):
                words = set(heard.split(" ")) #splits what is heard into a set (ex. "Hello There" becomes {"Hello", "There"})
                for country in country_list:
                    if country in words:
                        found_func = function(country)
                        isCountry = True
                        break

        for pattern, function in regex_patterns.items():
            if pattern.match(heard) and isCountry == False:
                found_func = function()
                break

        if heard == update_word:
            found_func = "Data is being updated. Please wait a moment."
            covid_data.get_updated_data()

        if found_func:
            print(found_func)
            talk_to_user(found_func)

        if heard.find(stop_word) != -1:
            print("Program Shutting Down")
            break
        
main()