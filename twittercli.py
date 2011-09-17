#!/usr/bin/env python
"""
twittercli.py

Orignal script by Chad Black on 04/22/2011
http://parezcoydigo.wordpress.com/2011/04/23/twitter-from-the-command-line/

Authentication:
http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth

Argparse Code:
http://www.doughellmann.com/PyMOTW/argparse/

--Modified for GeekTool by Graeme Noble 2011-09-03
"""
import tweepy
import os
import webbrowser
import sys
import ConfigParser
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--count', action='store', dest='number',
                    help='Number of tweets/results to return.', type=int, default=30)
parser.add_argument('-a','--auth', '--oauth', action='store_true', default=False,
                    dest='oauth',
                    help='Creates configuration file with Authentication tokens.')
parser.add_argument('-t','--tweets', '--timeline', action='store_true', default=False,
                    dest='tweets',
                    help='Display\'s tweets your latest timeline.')
parser.add_argument('-d','--direct', '--directmessages', action='store_true', default=False,
                    dest='directmessages',
                    help='Display\'s your latest direct messages inbox')
parser.add_argument('-o','--directsent', '--directmessagessent', action='store_true', default=False,
                    dest='directmessagessent',
                    help='Display\'s your sent direct messages.')
parser.add_argument('-p','--publictweets', '--public', action='store_true', default=False,
                    dest='publictweets',
                    help='Display\'s the latest public tweets.')
parser.add_argument('-m','--mentions', action='store_true', default=False,
                    dest='mentions',
                    help='Display\'s your latest mentions.')
parser.add_argument('-s','--search', action='store', dest='searchterm',
                    help='Set a search term in quotes, results from twitter displayed.')
parser.add_argument('-rom','--retweetsofme', action='store_true', default=False,
                    dest='retweetsofme',
                    help='Displays your tweets that have been retweeted.')
parser.add_argument('-rbm','--retweetsbyme', action='store_true', default=False,
                    dest='retweetsbyme',
                    help='Displays tweets that your have retweeted.')
parser.add_argument('-rtm','--retweetstome', action='store_true', default=False,
                    dest='retweetstome',
                    help='Displays tweets retweeted by people you follow.')
parser.add_argument('-n','--newline', action='store_true', default=False,
                    dest='newline',
                    help='Display\'s tweets your latest timeline.')
parser.add_argument('-v','--version', action='version', version='%(prog)s 0.9')
parser.add_argument('-e','--example', action='store_true', default=False,
                    dest='example',
                    help='Display\'s an example GeekTool script path.')

results = parser.parse_args()
totalresults = results.number

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
keyfile = "authkeys.dat"

pathname = os.path.dirname(sys.argv[0]) 
python = os.environ['_'].split(os.pathsep)
pwd = os.environ['PWD'].split(os.pathsep)
AuthKeysDataFile = os.path.abspath(pathname) + "/" + keyfile

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
		while True:
			ok = raw_input(prompt)
			if ok in ('y', 'ye', 'yes'):
				return True

			if ok in ('n', 'no', 'nop', 'nope'):
				return False
			retries = retries - 1
			if retries < 0:
				exit()
			print complaint

def setupoauth():
	print "Auth data to will be saved to " + AuthKeysDataFile + " any existing data will be reset:"
	AreYouSure = ask_ok("Are You Sure?")
	if AreYouSure == False:
		exit()
	print "To authenticate to Twitter you need to create a Twitter web application"
	print "Once you have created a Twitter web application you need to provide your"
	print "Consumer_Key and Consumer_Secret to generate your Access token's"
	LoadTwitterApplicationsWebsite = ask_ok("Do you want to go to the Twitter website to create an applicaiton?")
	if LoadTwitterApplicationsWebsite == True:
		new = 2
		url = "http://twitter.com/oauth_clients"
		webbrowser.open(url,new=new)
	CONSUMER_KEY = raw_input('Please enter your Consumer Key: ').strip()
	CONSUMER_SECRET = raw_input('Please enter your Consumer Secret: ').strip()
	if CONSUMER_KEY == "" or CONSUMER_SECRET == "":
		print "No values entered"
		exit()
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth_url = auth.get_authorization_url()
	new = 2
	webbrowser.open(auth_url,new=new)
	print 'Please authorize: ' + auth_url
	verifier = raw_input('PIN: ').strip()
	auth.get_access_token(verifier)

	ACCESS_KEY = auth.access_token.key
	ACCESS_SECRET = auth.access_token.secret
	config = ConfigParser.RawConfigParser()

	config.add_section('Twitter Auth')
	config.set('Twitter Auth', 'CONSUMER_KEY', CONSUMER_KEY)
	config.set('Twitter Auth', 'CONSUMER_SECRET', CONSUMER_SECRET)
	config.set('Twitter Auth', 'ACCESS_KEY', ACCESS_KEY)
	config.set('Twitter Auth', 'ACCESS_SECRET', ACCESS_SECRET)

	with open(AuthKeysDataFile, 'wb') as configfilewrite:
		config.write(configfilewrite)
	
	print "Auth data saved to " + AuthKeysDataFile
	print "CONSUMER_KEY: "  + CONSUMER_KEY
	print "CONSUMER_SECRET: " + CONSUMER_SECRET
	print "ACCESS_KEY: " + ACCESS_KEY
	print "ACCESS_SECRET: " + ACCESS_SECRET
	results.example = True

def readconfigfile():
	config = ConfigParser.RawConfigParser()
	config.read(AuthKeysDataFile)
	global CONSUMER_KEY
	global CONSUMER_SECRET
	global ACCESS_KEY
	global ACCESS_SECRET
	try :
		CONSUMER_KEY = config.get('Twitter Auth','CONSUMER_KEY')
		CONSUMER_SECRET = config.get('Twitter Auth','CONSUMER_SECRET')
		ACCESS_KEY = config.get('Twitter Auth','ACCESS_KEY')
		ACCESS_SECRET = config.get('Twitter Auth','ACCESS_SECRET')
	except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) :
		print "error reading config file"
	
if results.oauth == True:
	setupoauth()

if CONSUMER_KEY == "" or CONSUMER_SECRET == "" or ACCESS_KEY == "" or ACCESS_SECRET == "":
	ConfigFile = os.path.isfile(AuthKeysDataFile)


if ConfigFile == True:
	readconfigfile()
	

if CONSUMER_KEY == "" or CONSUMER_SECRET == "" or ACCESS_KEY == "" or ACCESS_SECRET == "":
	print "You are missing Twitter OAuth details try running OAuth."
	DoYouWantToSetupAuth = ask_ok("Do you want to run OAuth setup?")
	if DoYouWantToSetupAuth == False:
		exit()
	setupoauth()
	readconfigfile()


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def determine_max_username(padding,type,sorting):
	length = 0
	pad = 0
	size = 0
	bold = "\033[1m"
	reset = "\033[0;0m"
	
	for result in type:
	
		if sorting == "timeline":
			size = len(result.user.screen_name)
		if sorting == "retweet":
			size = len(result.user.screen_name + str(result.retweet_count))
		if sorting == "search":
			size = len(result.from_user)
		if sorting == "direct" or sorting == "directsent":
			size = len(result.sender_screen_name)
		if size > length:
			length = size

	pad = length + padding

	for result in type:
		if sorting == "timeline":
			print "{0}{1:{width}}{2}".format(bold,result.user.screen_name+":",reset, width=pad) + result.text.encode("utf-8")
			if results.newline == True:
				print 
		if sorting == "retweet":
			print "{0}{1:{width}}{2}".format(bold,result.user.screen_name + "(" + str(result.retweet_count) + "):",reset, width=pad) + result.text.encode("utf-8")
			if results.newline == True:
				print
		if sorting == "search":
			print "{0}{1:{width}}{2}".format(bold,result.from_user+":",reset, width=pad) + result.text.encode("utf-8")
			if results.newline == True:
				print
		if sorting == 'direct':
			print "{0}{1:{width}}{2}".format(bold,result.sender_screen_name+":",reset, width=pad) + result.text.encode("utf-8")
			if results.newline == True:
				print
		if sorting == "directsent":
			print "{0}{1:{width}}{2}".format(bold,result.sender_screen_name+":",reset, width=pad) + "@" + result.recipient_screen_name + " " + result.text.encode("utf-8")
			if results.newline == True:
				print

def returntweets(tweettype):
	global tweetstream
	try :
		if tweettype == "home_timeline":
			tweetstream = api.home_timeline(count=totalresults)
		if tweettype == "mentions":
			tweetstream = api.mentions(count=totalresults)
		if tweettype == "retweets_of_me":
			tweetstream = api.retweets_of_me(count=totalresults)
		if tweettype == "retweeted_to_me":
			tweetstream = api.retweeted_to_me(count=totalresults)
		if tweettype == "retweeted_by_me":
			tweetstream = api.retweeted_by_me(count=totalresults)
		if tweettype == "search":
			tweetstream = api.search(q=searchterm,rpp=totalresults)
		if tweettype == "public_timeline":
			tweetstream = api.public_timeline()
		if tweettype == "direct_messages":
			tweetstream = api.direct_messages(count=totalresults)
		if tweettype == "direct_messages_sent":
			tweetstream = api.sent_direct_messages(count=totalresults)
			
		
	except (tweepy.error.TweepError) :
		print "Unable to connect to Twitter API"
		exit()

	if tweettype == "home_timeline" or tweettype == "mentions" or tweettype == "public_timeline":
		determine_max_username(2,tweetstream,"timeline")
	if tweettype == "retweets_of_me" or tweettype == "retweeted_to_me" or tweettype == "retweeted_by_me":
		determine_max_username(4,tweetstream,"retweet")
	if tweettype == "search":
		determine_max_username(2,tweetstream,"search")
	if tweettype == "direct_messages":
		determine_max_username(2,tweetstream,"direct")
	if tweettype == "direct_messages_sent":
		determine_max_username(2,tweetstream,"directsent")
	
	
	
if results.tweets == True:
	returntweets("home_timeline")
if results.mentions == True:
	returntweets("mentions")
if results.publictweets == True:
	returntweets("public_timeline")
if results.retweetsofme == True:
	returntweets("retweets_of_me")
if results.retweetstome == True:
	returntweets("retweeted_to_me")
if results.retweetsbyme == True:
	returntweets("retweeted_by_me")
if results.directmessages == True:
	returntweets("direct_messages")
if results.directmessagessent == True:
	returntweets("direct_messages_sent")	
	
if results.searchterm:
	global searchterm
	searchterm = results.searchterm
	returntweets("search")

if results.example:
	python = str(python)
	python = python[:-2]
	python = python[2:]
	pwd = str(pwd)
	pwd = pwd[:-2]
	pwd = pwd[2:]	
	print python + " " + pwd + "/" + sys.argv[0] + " -t -c30"

if len(sys.argv) == 1:
	returntweets("home_timeline")