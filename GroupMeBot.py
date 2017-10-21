import requests,json, random, math
import csv
import random


###############GROUPME KEYS/DETAILS######################
###########REPLACE WITH YOUR OWN CREDENTIALS#############
accesstoken = ''
botid = ''
botidjarvis = ''
groupid = ''
farmersgroupid = ''
getfunction = '/groups/' + groupid + '/messages'
postfunction = '/bots/post?bot_id=' + botid + '&text='
url = 'https://api.groupme.com/v3'
#########################################################
#########################################################

def commands():
	requests.post(url + postfunction \
	+ 'Commands:' \
	+ '\n\n/8ball (Yes or No Question)' \
	+ '\n/weather' \
	+ '\n/news' \
	+ '\n/tv (TV Show Name)')

def eightBall():
	responses = ['Yes', 'Of Course!', 'No', "Of Course Not!"]
	requests.post(url + postfunction + random.choice(responses))

def weather():
	apikey = '' #REPLACE WITH APIKEY
	latitude = '29.7604'
	longitude = '-95.3698'
	units = 'us'
	darkSkyURL = 'https://api.darksky.net/forecast/' + apikey + '/' + latitude + ',' + longitude + '?units=' + units
	get_weather = requests.get(darkSkyURL)
	load_weather = json.loads(get_weather.text)
	#Get Specific Data
	summary = (load_weather['currently']['summary'])
	temp = (load_weather['currently']['temperature'])
	requests.post(url + postfunction + 'Currently it is ' + summary.lower() + ' with a temperature of ' + str(int(math.ceil(temp))) + ' degrees in Houston.')

def news():
	x = 0
	articleArr = []
	articleDescription = []
	apikey = '' #REPLACE WITH APIKEY
	newsURL = 'https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=' + apikey
	get_news = requests.get(newsURL)
	load_news = json.loads(get_news.text)
	#Get Specific Data
	while x<10:
		label = x + 1
		title = (load_news['articles'][x]['title'])
		description = (load_news['articles'][x]['description'])
		articleArr.append(title)
		articleDescription.append(description)
		x = x + 1

	requests.post(url + postfunction \
	+ '1. ' + articleArr[0] \
	+ '\n\n2. ' + articleArr[1] \
	+ '\n\n3. ' + articleArr[2] \
	+ '\n\n4. ' + articleArr[3] \
	+ '\n\n5. ' + articleArr[4] \
	+ '\n\n6. ' + articleArr[5] \
	+ '\n\n7. ' + articleArr[6] \
	+ '\n\n8. ' + articleArr[7] \
	+ '\n\n9. ' + articleArr[8] \
	+ '\n\n10. ' + articleArr[9])

def tvshows(last_message):
	try:
		tvShow = last_message.split(' ', 1)
		tvShow = tvShow[1]
		tvShow = tvShow.title()
		tvShowLink = tvShow.replace(' ', '%20')
		###SEARCH FOR SHOW ID###
		searchURL = 'http://api.tvmaze.com/search/shows?q=' + tvShowLink
		get_search = requests.get(searchURL)
		load_search = json.loads(get_search.text)
		tvrageID = (load_search[0]['show']['externals']['tvrage'])

		###SEARCH FOR SHOW AIR DATES###
		showLookupURL = 'http://api.tvmaze.com/lookup/shows?tvrage=' + str(tvrageID)
		get_show = requests.get(showLookupURL)
		load_show = json.loads(get_show.text)
	except:
		pass

	try:
		##PREVIOUS EPISODE DETAILS###
		prevepURL = (load_show['_links']['previousepisode']['href'])
		get_prevepDetails = requests.get(prevepURL)
		load_prevepDetails = json.loads(get_prevepDetails.text)
		prevAirDate = (load_prevepDetails['airdate'])
		prevMessage = ' was last aired on ' + str(prevAirDate)
	except:
		prevMessage = ' has not aired yet'
		pass

	try:
		###NEXT EPISODE DETAILS###
		nextepURL = (load_show['_links']['nextepisode']['href'])
		get_nextepDetails = requests.get(str(nextepURL))
		load_nextepDetails = json.loads(get_nextepDetails.text)
		nextAirDate = (load_nextepDetails['airdate'])
		nextMessage = ' and will next air on ' + str(nextAirDate) + '.'
	except:
		nextMessage = ' and the show has now ended or a release date has not been announced.'
		pass
	requests.post(url + postfunction + tvShow + prevMessage + nextMessage)

def throwback():
	random_lines = random.choice(open('farmersmessages.csv').readlines())
	requests.post(url + postfunction + random_lines)


def main():
	get_messages = requests.get(url + getfunction + '?token=' + accesstoken)
	load_messages = json.loads(get_messages.text)
	last_message = (load_messages['response']['messages'][0]['text']).lower()
	if last_message.startswith('/commands'):
		commands()
	if last_message.startswith('/8ball'):
		eightBall()
	if last_message.startswith('/weather'):
		weather()
	if last_message.startswith('/news'):
		news()
	if last_message.startswith('/tv'):
		tvshows(last_message)
	if last_message.startswith('/tb'):
		throwback()



run = True
while run:
	try:
		main()
	except:
		main()
