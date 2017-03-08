#!/usr/bin/env python
# encoding: utf-8

import tweepy
import time
import csv
from datetime import date
import datetime

f = open('tweets.csv', 'a')
writer = csv.writer(f)

# #Twitter API credentials
# consumer_key = "SGS9ZMk1h0CvkfVJ6uvFZiZfv"
# consumer_secret = "BEcNaMbQbaG7oDoZKT2yztyYa0haJwlqmz8SYr0O5CBa3zIhIf"
# access_key = "212920273-pjmAKzWw23rkLinFFNfJE9A96uE4F2qB3wr1vr7n"
# access_secret = "wBsz1Ze4xOAtNTWelk0NJcyI2GRnEK77qcWNwK1A4jyvy"

# consumer_key = "WkmU1ZOLH64dV5HZDaKUL9QDc"
# consumer_secret = "uDJVYICdbZ7JTsCEwB6JI8ms8tkWdJsKiMLIdZnvJLWVf3c1HB"
# access_key = "833549298725961728-5Fvngkzt92PLyV1dpGeqNiN0FQ9vfFB"
# access_secret = "Jstd8N24MxiaSVqDXl6aayPWtVBTBLPWTNb1pQYyyWiqd"

# consumer_key = "eiDhOCZRSDY95IzZKmZVAcK20"
# consumer_secret = "wQHu7sPvQHGfMlTDI4r3v37afB4jK3eBDHPhvXmkMjGCMsiMG0"
# access_key = "472754640-yfnNdQ3ywnkWJYNCbM7zonfgsmx3gQkVNOtAkneD"
# access_secret = "Abfbua0ShkFtUtp2WRiaezZI7ouZEzgQmgZuAJBBAVXNO"

consumer_key = 'rnhNUcu1oLwQ9b6T0dMRtKg7S'
consumer_secret = 'Owho0Enr7hF54S6GylbKMrXuSie3IKpmXE2Rt9G5vzyK2dVFow'
access_key = '27848871-XEJ8TEasqpS0Bbgu2W2ScCPqzSwUTnNbmlWUKJLUG'
access_secret = '7pDKC87xNfHvjgnAabvd1Fqeb1aCCVAs61utr5j7iW014'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Setting date bound and number bound
date_from = datetime.date(2017, 3, 4)
date_to = datetime.date(2017, 3, 6)

num_bound = 1000000

total_tweet_count = 0

def get_all_tweets(query):
	loopCond = True
	tweets = []
	
	new_tweets = api.search(q=query)

	for tweet in new_tweets:
		if tweet.created_at.date() <= date_to and tweet.created_at.date() >= date_from:
			tweets.append(tweet)

	if tweets:
		oldest = tweets[-1].id - 1
	else:
		oldest = new_tweets[-1].id - 1

	while len(new_tweets) > 0 and loopCond:
		if len(tweets) > num_bound:
			break
		try:
			new_tweets = api.search(q=query,max_id=oldest)
		except tweepy.TweepError:
			print("Rate limit exceeded. Pause for 15 mins starting from",datetime.datetime.now())
			time.sleep(60*15)
		except StopIteration:
			break

		if len(new_tweets)<=0:
			print("No more result")
			loopCond = False
			break

		write_list = []
		for tweet in new_tweets:
			if tweet.created_at.date() <= date_to and tweet.created_at.date() >= date_from:
				tweets.append(tweet)

				originality = ''
				if hasattr(tweet, 'retweeted_status'):
					originality = tweet.retweeted_status._json['user']['id']
				else:
					originality = 'original'

				# Date, Tweet ID, Tweet, User ID, Original tweet's user ID, List of Retweeters' ID

				write_list = [tweet.created_at.date(), tweet.id, tweet.text, tweet._json['user']['id'], originality]
				writer.writerow(write_list)
				print("Tweet appended")

		
		#save most recent tweets
		if write_list:
			oldest = tweets[-1].id - 1
		else:
			oldest = new_tweets[-1].id - 1
			print("Tweets Appended")

def get_retweets(tweet):
	print("------------------------------------------------")
	rt_list = api.retweets(tweet.id)
	if hasattr(tweet, 'retweeted_status'):
		print("Tweet:",tweet.text, "ID:", tweet.id)
		print("This tweet is a retweet. The original tweet is", tweet.retweeted_status.text)
		if rt_list:
			print("And this tweet is retweeted by")
			for rt in rt_list:
				print(rt.text)
	elif rt_list:
		print("Tweet:",tweet.text)
		print("This tweet is an original tweet and retweeted by")
		for rt in rt_list:
			print(rt._json.get('user').get('screen_name'))
	else:
		print("Tweet:",tweet.text)
		print("This tweet is an original tweet without retweets.")
	print("------------------------------------------------")


def main():
	query = input("Put Query: ")
	get_all_tweets(query)
	# tweet_list = get_all_tweets(query)
	# print("First item:",tweet_list[0].created_at.date())
	# print("Last item:",tweet_list[-1].created_at.date())

	# for tweet in tweet_list:
	# 	try:
	# 		get_retweets(tweet)
	# 	except tweepy.TweepError:
	# 		print("Rate limit exceeded. Pause for 15 mins.")
	# 		time.sleep(60*15)
	# 		continue
	# 	except StopIteration:
	# 		break
	print("Done")

if __name__ == '__main__':
	main()