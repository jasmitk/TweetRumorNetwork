'''
Created on Feb 16, 2017

@author: lbozarth
'''
import tweepy, csv, datetime

class FakeNewsStreamer(tweepy.StreamListener):
    
    def on_status(self, status):
        urlString = "none"
        for url in status.entities["urls"]:
            urlString = url['expanded_url']
            break
        data = [status.id, status.user.id, status.user.screen_name, urlString, status.created_at, status.text.encode("utf-8").replace('|', ' ').replace('\n', ' '), status.retweet_count]
        dString = datetime.datetime.today().strftime('%Y-%m-%d')
        fName = '../data/output/' + dString + '.csv'
        with open(fName, 'a') as f:
            writer = csv.writer(f, dialect=csv.excel, lineterminator="\n")
            writer.writerow(data)
        return

    def on_exception(self, exception):
        print(exception)
        return tweepy.StreamListener.on_exception(self, exception)
    
    def on_error(self, status_code):
        print(status_code)
        return tweepy.StreamListener.on_error(self, status_code)

        