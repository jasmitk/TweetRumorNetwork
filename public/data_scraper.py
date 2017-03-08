#!/usr/bin/env python
# encoding: utf-8

import tweepy, datetime, csv, codecs, time

maxTweets = 100 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
since_time = "2016-09-01"
# until_time = "2017-03-07"

consumer_key = 'rnhNUcu1oLwQ9b6T0dMRtKg7S'
consumer_secret = 'Owho0Enr7hF54S6GylbKMrXuSie3IKpmXE2Rt9G5vzyK2dVFow'
access_key = '27848871-XEJ8TEasqpS0Bbgu2W2ScCPqzSwUTnNbmlWUKJLUG'
access_secret = '7pDKC87xNfHvjgnAabvd1Fqeb1aCCVAs61utr5j7iW014'

def getTracks():
	dotcoms = []
	with open('../data/input/sources.csv', 'rU') as f:
		f.readline()
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			dotcoms.append(row[0])
	print(dotcoms)
	print(len(dotcoms))
	return dotcoms

def writeToFile(data, fName):
	print("writing to file")
	with open(fName, 'a') as f:
		writer = csv.writer(f, dialect=csv.excel, lineterminator="\n")
		writer.writerows(data)
	return

def get_all_tweets(query, fName):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	oldest = -1L
	total_tweet_count = 0
	while total_tweet_count < maxTweets:
		try:
			if (oldest <= 0):
				new_tweets = api.search(q=query, count=tweetsPerQry, since=since_time)
			else:
				new_tweets = api.search(q=query, count=tweetsPerQry, max_id=oldest-1, since=since_time)
		except tweepy.TweepError:
			print("Rate limit exceeded. Pause for 15 mins starting from ",datetime.datetime.now())
			time.sleep(60 * 15 + 5)
			continue

		if len(new_tweets)<=0:
			print("Returning to main")
			return
		
		data = [(tweet.id, tweet.user.id, tweet.user.screen_name, tweet.created_at, tweet.text.encode("utf-8").replace('|', ' ').replace('\n', ' '), tweet.retweet_count) for tweet in new_tweets]
		writeToFile(data, fName)
		total_tweet_count += len(data)
		oldest = new_tweets[-1].id

if __name__ == '__main__':
	dotcoms = getTracks()
	for dotcom in dotcoms:
		searchQuery = 'url:' + dotcom  # this is what we're searching for
		fName = "../data/output/" + dotcom + ".csv" # We'll store the tweets in a text file.
		print(searchQuery, fName)
		get_all_tweets(searchQuery, fName)
		break
	print("Done")