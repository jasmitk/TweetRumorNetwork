#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import time
from datetime import date

#Twitter API credentials
consumer_key = "SGS9ZMk1h0CvkfVJ6uvFZiZfv"
consumer_secret = "BEcNaMbQbaG7oDoZKT2yztyYa0haJwlqmz8SYr0O5CBa3zIhIf"
access_key = "212920273-pjmAKzWw23rkLinFFNfJE9A96uE4F2qB3wr1vr7n"
access_secret = "wBsz1Ze4xOAtNTWelk0NJcyI2GRnEK77qcWNwK1A4jyvy"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

date_bound = date(2017, 1, 28)
num_bound = 15

def get_all_tweets(query):
	loopCond = True
	tweets = []
	
	new_tweets = api.search(q=query)

	if new_tweets[-1].created_at.date() < date_bound:
		for tweet in new_tweets:
			if tweet.created_at.date() < date_bound:
				new_tweets.remove(tweet)
		loopCond = False

	tweets.extend(new_tweets)
	print(len(new_tweets),"Appended")

	oldest = tweets[-1].id - 1
	#while
	while len(new_tweets) > 0 and loopCond:
		if len(tweets) > num_bound:
			break
		try:
			new_tweets = api.search(q=query,since_id=oldest)
		except tweepy.TweepError:
			print("Rate limit exceeded. Pause for 15 mins.")
			time.sleep(60*15)
			continue
		except StopIteration:
			break

		if new_tweets[-1].created_at.date() < date_bound:
			for tweet in new_tweets:
				if tweet.created_at.date() < date_bound:
					new_tweets.remove(tweet)
			tweets.extend(new_tweets)
			loopCond = False
			break
		
		#save most recent tweets
		tweets.extend(new_tweets)
		print(len(new_tweets),"Appended")
		
		#update the id of the oldest tweet less one
		oldest = tweets[-1].id - 1

	return tweets

def get_retweets(tweet):
	print("------------------------------------------------")
	rt_list = api.retweets(tweet.id)
	if hasattr(tweet, 'retweeted_status'):
		print("Tweet:",tweet.text)
		print("This tweet is a retweet. The original tweet is", tweet.retweeted_status.text)
	elif rt_list:
		print("Tweet:",tweet.text)
		print("This tweet is an original tweet and retweeted by")
		for rt in rt_list:
			print(rt.text)
	else:
		print("Tweet:",tweet.text)
		print("This tweet is an original tweet without retweets.")
	print("------------------------------------------------")


def main():	
	query = input("Put Query: ")
	tweet_list = get_all_tweets(query)
	#get_retweets(tweet_list[0])

	for tweet in tweet_list:
		get_retweets(tweet)
	#print(tweet_list[0])
	print("Done")

if __name__ == '__main__':
	main()