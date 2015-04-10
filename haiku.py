# twitter client
import tweepy

import nltk
import urllib3
import database
from nltk.corpus import cmudict

# digit detection
import curses
from curses.ascii import isdigit

 
ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS
 
def is_english(text):
	"""Return True if text is probably English, False if text is probably not English
	"""
	text = text.lower()
	words = set(nltk.wordpunct_tokenize(text))
	return len(words & ENGLISH_STOPWORDS) > len(words & NON_ENGLISH_STOPWORDS)

def insert_haiku(start):
	end=start+1000
	db=database.haikuTweetDB("tweets.db")
	db.execute("Select id, text, screen_name, created_at, source from tweetCollection where id between "+str(start)+" and "+str(end)+";")
	tweets=db.cur.fetchall()
	if tweets==None:
		return False
	for tweet in tweets:
		
		id, text, screen_name, created_at, source = tweet
		
		if is_haiku(text):
			#db.execute("Insert Into haikuCollection Names(id, text, screen_name, created_at, source) Values (?, ?, ?, ?, ?);", [id, text, screen_name, created_at, source])
			print screen_name+": "+text

	return True

def is_haiku(text):
	import re
	text_orig = text
	text = text.lower()
	if filter(str.isdigit, str(text)):
		return False
	words = nltk.wordpunct_tokenize(re.sub('[^a-zA-Z_ ]', '',text))
	syl_count = 0
	word_count = 0
	haiku_line_count = 0
	lines = []
	d = cmudict.dict()
	for word in words:
	   try:
		syl_count += [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
		if haiku_line_count == 0:
			if syl_count == 5:
				lines.append(word)
				haiku_line_count += 1
		elif haiku_line_count == 1:
			if syl_count == 12:
				lines.append(word)
				haiku_line_count += 1
		else:
			if syl_count == 17:
				lines.append(word)
				haiku_line_count += 1
	   except KeyError:
		print "Oops"
		return False
	if syl_count == 17:
		try:
			final_lines = []
			str_tmp = ""
			counter = 0
			for word in text_orig.split():
				str_tmp += str(word) + " "
				if lines[counter].lower() in str(word).lower():
					final_lines.append(str_tmp.strip())
					counter += 1
					str_tmp = ""
			if len(str_tmp) > 0:
				final_lines.append(str_tmp.strip())
				return final_lines
		except Exception as e:
			print e
			return False
	else:
		print("Not a Haiku: "+text)
		return False
        
"""
				haiku_result = is_haiku(status.text)
				if haiku_result is not False:
					database.haikuTweetDB.insertTweet(status.text, status.author.screen_name, status.created_at, status.source)
					print "FOUND HAIKU: %snby %s at %s from %snn" % (status.text,
                                                           status.author.screen_name,
                                                           status.created_at,
                                                           status.source,)
"""


class StreamWatcherListener(tweepy.StreamListener):
	db = database.haikuTweetDB("tweets.db")
	def on_status(self, status):
		try:
			if is_english(status.text):
				print("Adding Tweet...")
				id = self.db.insertTweet(str(status.text), str(status.author.screen_name), str(status.created_at), str(status.source))
				print(status.text +" with db ID: "+str(id))
		except Exception as e:
			print(e)
			pass
	def on_error(self, status_code):
		print "An error has occurred! Status code = %s" % status_code
		return True  # keep the dream alive

def streamAndCollectTweets():
	# establish stream
	consumer_key = "aPmWghTglbAsmUaI5Q25GBwpG"
	consumer_secret = "8C2snnOpOqK1OcY7n1XiOZtjhJ7GhvhK29nuVzm0CPOgNX6pp7"
	auth1 = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
	access_token = "14849033-3BJYxmAfd0jsI0WR1Zu0MyNKJPqmmYbOy8eidjcnj"
	access_token_secret = "iTz2dN1EWmgiXyG6pnZt6Puw20NCmozSscW4uDA9KewbE"
	auth1.set_access_token(access_token, access_token_secret)
	print "Establishing stream"
	
	"""
	haiku_test = "Learn to Write haiku there are rules for syllables ham radio rest"
	if is_haiku(haiku_test) is not False and len(is_haiku(haiku_test)) == 3:
		print "Haiku detection is (probably) working properly"
	else:
		print "Haiku detection (probably) broken :("
	"""
	stream = tweepy.Stream(auth1, StreamWatcherListener(), timeout=None, retry_count=2)
	stream.sample()
	
if __name__ == '__main__':
	run=True
	curr=0
	while run:
		run=insert_haiku(curr)
		curr+=1000
	"""
	while True:
		try:
			#streamAndCollectTweets()
			#call method that queries the tweetCollection table,
			#checks to see if result is a haiku,
			#if so, insert into haikuCollection table		
		except KeyboardInterrupt:
			print "Later gator!"
			break
		except:
			print "Exception. trying again..."
			continue
	"""
