#!/usr/bin/env python

"""
twittercli.py

Orignal script by Chad Black on 04/22/2011
	http://parezcoydigo.wordpress.com/2011/04/23/twitter-from-the-command-line/

OAuth Authentication :
	http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth

Argparse Code:
	http://www.doughellmann.com/PyMOTW/argparse/

--Modified for GeekTool by Graeme Noble 2011-09-03
"""

# Import modules, tweepy should be the only package not preinstalled on system. 

import tweepy
import os
import webbrowser
import sys
import ConfigParser
import argparse

# Parse command line arguments using argparse. Descriptions added here will be displayed using -h

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
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-e','--example', action='store_true', default=False,
                    dest='example',
                    help='Display\'s an example GeekTool script path.')

# Argparse results saved, number of tweet results set.

results = parser.parse_args()
totalresults = results.number

# Declare OAuth varibles.
# if you do not want to use a config file you can manually add your OAuth detail here.

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
keyfile = "authkeys.dat"

# Determine python2.7 and script location.

pathname = os.path.dirname(sys.argv[0]) 
python = os.environ['_'].split(os.pathsep)
pwd = os.environ['PWD'].split(os.pathsep)
AuthKeysDataFile = os.path.abspath(pathname) + "/" + keyfile

# Prompting code used in OAuth setup wizard.
# Pretty simple returns True or Faluse based on user's answer.

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
			
# OAuth setup wizard code.

def setupoauth():

	# Warn the user that this could override existing config file.
	
	print "Auth data to will be saved to " + AuthKeysDataFile + " any existing data will be reset:"
	AreYouSure = ask_ok("Are You Sure?")
	if AreYouSure == False:
		exit()
	print "To authenticate to Twitter you need to create a Twitter web application"
	print "Once you have created a Twitter web application you need to provide your"
	print "Consumer_Key and Consumer_Secret to generate your Access token's"
	
	# Ask the user if they want to go to the Twitter website.
	
	LoadTwitterApplicationsWebsite = ask_ok("Do you want to go to the Twitter website to create an applicaiton?")
	if LoadTwitterApplicationsWebsite == True:
		new = 2		# This should open browser in a new window/tab.
		url = "http://twitter.com/oauth_clients"
		webbrowser.open(url,new=new)
		
	# Ask the user for there OAuth app details.
	
	CONSUMER_KEY = raw_input('Please enter your Consumer Key: ').strip()
	CONSUMER_SECRET = raw_input('Please enter your Consumer Secret: ').strip()
	
	# If they don't enter anything stop the setup wizard.
	
	if CONSUMER_KEY == "" or CONSUMER_SECRET == "":
		print "No values entered"
		exit()
	
	# Use the details entered with Tweepy to get an authorization url.
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth_url = auth.get_authorization_url()
	
	# Assume the user needs the URL launched and launch it. :/
	
	new = 2
	webbrowser.open(auth_url,new=new)
	print 'Please authorize: ' + auth_url # URL printed just in case.
	
	# Prompt user for the PIN then verify it.
	
	verifier = raw_input('PIN: ').strip()
	auth.get_access_token(verifier)
	
	# Set access values returned from Tweepy authorization.
	
	ACCESS_KEY = auth.access_token.key
	ACCESS_SECRET = auth.access_token.secret
	
	# Attempt to save values to config file.
	
	config = ConfigParser.RawConfigParser()

	config.add_section('Twitter Auth')
	config.set('Twitter Auth', 'CONSUMER_KEY', CONSUMER_KEY)
	config.set('Twitter Auth', 'CONSUMER_SECRET', CONSUMER_SECRET)
	config.set('Twitter Auth', 'ACCESS_KEY', ACCESS_KEY)
	config.set('Twitter Auth', 'ACCESS_SECRET', ACCESS_SECRET)

	with open(AuthKeysDataFile, 'wb') as configfilewrite:
		config.write(configfilewrite)
	
	# Print the results in the terminal so the user knows what has happened.
	
	print "Auth data saved to " + AuthKeysDataFile
	print "CONSUMER_KEY: "  + CONSUMER_KEY
	print "CONSUMER_SECRET: " + CONSUMER_SECRET
	print "ACCESS_KEY: " + ACCESS_KEY
	print "ACCESS_SECRET: " + ACCESS_SECRET
	
	# Set example to True, so an example GeekTool line will be printed compatible on user's system.
	
	results.example = True

# Reading config file code

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

# If -a is set force OAuth setup wizard.

if results.oauth == True:
	setupoauth()

# If any OAuth values are missing (not defined in script) start attempting to read config file.

if CONSUMER_KEY == "" or CONSUMER_SECRET == "" or ACCESS_KEY == "" or ACCESS_SECRET == "":
	ConfigFile = os.path.isfile(AuthKeysDataFile)

# If the config file exists, read it.

if ConfigFile == True:
	readconfigfile()

# If no config file exists and no OAuth details are defined, assume user is running for the first
# time with no -a switch so prompt and ask them if they want to run the OAuth setup wizard.
#
# Once OAuth setup wizard has finished try to read the created config file. 

if CONSUMER_KEY == "" or CONSUMER_SECRET == "" or ACCESS_KEY == "" or ACCESS_SECRET == "":
	print "You are missing Twitter OAuth details try running OAuth."
	DoYouWantToSetupAuth = ask_ok("Do you want to run OAuth setup?")
	if DoYouWantToSetupAuth == False:
		exit()
	setupoauth()
	readconfigfile()

# At this point, OAuth varibles should be set so setup API authentication using Tweepy. 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Define some more functions.

# This function finds the longest username returned in the Twitter results, this then becomes the
# column width for username fields (plus a few extra characters for padding).
#
# Printing the output is slightly different for timeline results vs retweets etc.

def determine_max_username(padding,type,sorting):

	# Default values reset/set.

	length = 0
	pad = 0
	size = 0
	bold = "\033[1m"
	reset = "\033[0;0m"
	
	for result in type:
		
		# For every result try to find the longest Twitter username.
		#
		# Because the Twitter username is sometimes in different places based on Twitter API type,
		# size of Twitter username is checked based on the type of Twitter API used.
		
		if sorting == "timeline":
			size = len(result.user.screen_name)
		if sorting == "retweet":
			size = len(result.user.screen_name + str(result.retweet_count))
		if sorting == "search":
			size = len(result.from_user)
		if sorting == "direct" or sorting == "directsent":
			size = len(result.sender_screen_name)
			
		# If the current Twitter username is longer than the last, set length to that value.
		
		if size > length:
			length = size
	
	# Once we have checked all the results padding is added.
	
	pad = length + padding
	
	# Print the results, slightly different output based Twitter API type.
	#
	# I'm going to look a new/better way of printing line spacing if required. :/

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

# Determines which Twitter api to use. Then sends the output to the determine_max_username function
# for printing output.

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
	
	# So connect to the API but if it fails tell the user. We also end the script if this is true.
	
	except (tweepy.error.TweepError) :
		print "Unable to connect to Twitter API"
		exit()

	# We should have results from the Twitter API, set the padding length based on API type/output.

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
	
# If an command line option is specified execute it. 
	
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

# Search is a tiny bit different because it has a search query.

if results.searchterm:
	global searchterm
	searchterm = results.searchterm
	returntweets("search")

# Added a -e option to print out a full command line example because python2.7 might be located in
# different places on different systems.

if results.example:
	
	# This was quick code that I added, we should do some better error checking. :/
	
	python = str(python)
	python = python[:-2]
	python = python[2:]
	pwd = str(pwd)
	pwd = pwd[:-2]
	pwd = pwd[2:]
	
	print python + " " + pwd + "/" + sys.argv[0] + " -t -c30"

# If no options are set but OAuth varibles exist just bring up the user's home timeline.

if len(sys.argv) == 1:
	returntweets("home_timeline")