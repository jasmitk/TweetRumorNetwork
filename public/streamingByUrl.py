'''
Created on Feb 16, 2017

@author: lbozarth
'''
import csv, tweepy
from FakeNewsStreamer import FakeNewsStreamer

#Twitter API credentials
consumer_key = "SGS9ZMk1h0CvkfVJ6uvFZiZfv"
consumer_secret = "BEcNaMbQbaG7oDoZKT2yztyYa0haJwlqmz8SYr0O5CBa3zIhIf"
access_key = "212920273-pjmAKzWw23rkLinFFNfJE9A96uE4F2qB3wr1vr7n"
access_secret = "wBsz1Ze4xOAtNTWelk0NJcyI2GRnEK77qcWNwK1A4jyvy"

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

def streaming(tracks):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    fnStreamer = FakeNewsStreamer()
    fnStream = tweepy.Stream(auth=api.auth, listener=fnStreamer)
    fnStream.filter(track=tracks)
    return

if __name__ == '__main__':
    tracks = getTracks()
#     tracks = list(set(tracks))
#     tracks = tracks[:200]
#     print(len(tracks))
    streaming(tracks)
    pass