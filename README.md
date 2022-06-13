# Covid-19 Web Scraper With Voice Detection

A simple voice recognition application that gives the user various amount of information about COVID-19 in respect to what they request verbally.
The purpose of this program is to give a user updates about COVID-19 cases, both in general and country specific. Using python's speech recognition, a user can verbally ask the program for specific data regarding the COVID-19 cases. To ensure updated information of cases, a third party application, ParseHub, scrapes the following website: https://www.worldometers.info/coronavirus/ to obtain the updated relevant information.

Example usage of program:
	Asking the program any of these will deliver a response accordingly both through audio output and in the terminal:
		-"How many total cases are there?"
		-"How many total deaths are there?"
		-"How many total recovered people are there?"
		-"How many total cases in Japan?"
		-"How many deaths in Korea?"
		-"How many active cases in the USA?"
		-"How many critical cases are there in China?"

The program is designed to give relevant information to the user as long as their command contains any of the following:
	-total cases
	-total deaths
	-total recovered
	-total cases + (a country)
	-deaths + (a country)
	-active cases + (a country)
	-critical cases + (a country)

Additionally, the user can continually ask questions until they say "stop", which will end the program. When the user wants to update the current information, all they need to do is say "update", and the program will automatically start updating the information.

# References
Tech With Tim (https://www.youtube.com/c/TechWithTim)
