'''
Created on Feb 16, 2017

@author: lbozarth
'''
import tweepy

class FakeNewsStreamer(tweepy.StreamListener):
        
    def on_status(self, status):
        print(status)
        return

    def on_exception(self, exception):
        print(exception)
        return tweepy.StreamListener.on_exception(self, exception)
    
    def on_error(self, status_code):
        print(status_code)
        return tweepy.StreamListener.on_error(self, status_code)

        