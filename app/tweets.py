from __future__ import print_function
import tweepy
import numpy as np
import configurations
import pandas as pd
import time
import sys
from textblob import TextBlob
import googlemaps

def limit_handled(cursor):

    while True:
        try:
        	yield cursor.next()

        except tweepy.RateLimitError:
            time.sleep(60*15)
            continue

        except StopIteration:
        	break

def make_maps(tweetsDataframe):
	doughnut = []
	sentiment_map = []
	sources_plot = []
	sentiment_pie = []
	retweet_table = []
	doughnut.append(["Language","Tweets"])
	lang_count = tweetsDataframe["language"].value_counts()
	lang_count= lang_count.to_dict()
	for key,value in lang_count.iteritems():
		temp = [key,value]
		doughnut.append(temp)
	sentiment_pie.append(["Sentiment","Tweets"])
	sentiment_count = tweetsDataframe["sentiments_group"].value_counts()
	sentiment_count= sentiment_count.to_dict()
	for key,value in sentiment_count.iteritems():
		temp = [key,value]
		sentiment_pie.append(temp)

	sources_plot.append(["Twitter Client","Users"])
	source_count = tweetsDataframe["source"].value_counts()[:5][::-1]
	source_count= source_count.to_dict()
	for key,value in source_count.iteritems():
		temp = [key,value]
		sources_plot.append(temp)

	for i in range(0,len(tweetsDataframe)):

		temp= []
		latitude = tweetsDataframe['latitude'][i]
		longitude = tweetsDataframe['longitude'][i]
		language = tweetsDataframe["translate"][i]
		language = language.encode('utf-8')
		sentiment = tweetsDataframe['sentiments'][i]
		if latitude == "":
			continue
		else:

			temp = [latitude,longitude,language,sentiment,"tooltip"]
			sentiment_map.append(temp)

	retweet_table.append(["Tweet Text","ReTweets"])
	df = tweetsDataframe[['translate','retweet_count']].drop_duplicates().sort_values(['retweet_count'],ascending=False)[:10]
	for key,value in zip(df['translate'],df['retweet_count']):
		temp = [key,value]
		retweet_table.append(temp)
	

	return (doughnut,sentiment_map,sources_plot,sentiment_pie,retweet_table)


def QueryTwitter(search_string):

	key = configurations.consumer_key
	secret = configurations.consumer_secret
	access_token = configurations.access_token
	access_secret = configurations.access_secret
	auth = tweepy.OAuthHandler(consumer_key=key,consumer_secret=secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	tweet_list = []
	for tweet in limit_handled(tweepy.Cursor(api.search,q=search_string).items(50)):
		tweet_list.append(tweet)
	tweet_Data = filter_tweets(tweet_list)
	(doughnut,sentiment_map,sources_plot,sentiment_pie,retweet_table) = make_maps(tweet_Data)
	return (doughnut,sentiment_map,sources_plot,sentiment_pie,retweet_table)

def filter_tweets(tweets):


	id_list = [tweet.id for tweet in tweets]
	tweet_Data = pd.DataFrame(id_list,columns=['id'])
	tweet_Data["text"] = [tweet.text for tweet in tweets]
	tweet_Data["retweet_count"]= [tweet.retweet_count for tweet in tweets]

	Sentiments_list = []
	Sentiments_group = []
	Subjectivity_list = []
	Subjectivity_group = []
	tweet_text_list = []
	tweet_location_list = []
	tweet_language = []
	tweet_latitude = []
	tweet_longitude =[]
	tweet_country = []
	tweet_source = []
	tweet_translation= []

	for tweet in tweets:
		raw_tweet_text = tweet.text
		message = TextBlob(unicode(tweet.text))
		location = tweet.author.location
		source = tweet.source
		source = source.encode('utf-8')
		tweet_source.append(source)
		if len(location) !=0:
			(latitude,longitude,country) = geocode_location(location)
			tweet_latitude.append(latitude)
			tweet_longitude.append(longitude)
			tweet_country.append(country)

		else:
			tweet_latitude.append("")
			tweet_longitude.append("")
			tweet_country.append("")

		lang = message.detect_language()
		tweet_language.append(str(lang))
		try:
			if str(lang) != "en":
				message = message.translate(to="en") 
		except:
			pass
		message = str(message)
		new_message = ""
		for letter in range(0,len(message)):
			current_read =message[letter]
			if ord(current_read) > 126:
				continue
			else:
				new_message =new_message+current_read

		message = new_message 
		tweet_translation.append(message[:120])
		message = TextBlob(message)

		sentiment = message.sentiment.polarity
		if (sentiment > 0):
			#postive
			Sentiments_group.append('positive')
		elif (sentiment < 0):
			#Negative
			Sentiments_group.append('negative')
		else:
			Sentiments_group.append('neutral')



		subjectivity = message.sentiment.subjectivity
		if (subjectivity > 0.4):
			
			Subjectivity_group.append('subjective')
		else:
			Subjectivity_group.append('objective')

		Sentiments_list.append(sentiment)
		Subjectivity_list.append(subjectivity)
		tweet_text_list.append(raw_tweet_text)
		tweet_location_list.append(location)


	tweet_Data["sentiments"] = Sentiments_list
	tweet_Data["sentiments_group"] = Sentiments_group

	tweet_Data["subjectivity"]= Subjectivity_list
	tweet_Data["subjectivity_group"] = Subjectivity_group

	tweet_Data["location"] = tweet_location_list
	tweet_Data["text"] = tweet_text_list

	tweet_Data["language"] = tweet_language
	tweet_Data["latitude"] = tweet_latitude
	tweet_Data["longitude"]= tweet_longitude
	tweet_Data["country"] = tweet_country
	tweet_Data["source"] = tweet_source
	tweet_Data["translate"] = tweet_translation

	return tweet_Data

def geocode_location(loc):
	
	gmaps_api = configurations.google_maps_key
	gm = googlemaps.Client(key=gmaps_api)
	location_result = gm.geocode(loc)
	if len(location_result) > 0:
		latitude = location_result[0]['geometry']['location']['lat']
		longitude= location_result[0]['geometry']['location']['lng']
		country =location_result[0]['formatted_address'].split(",")
		country = country[len(country)-1]		
		return (latitude,longitude,country)

	else:
		return ("","","")

	return
