''' Function: Get bio of twitter users followed by users in array reference_users'''

import tweepy
import os
import time
import threading 
import random

consumer_key = os.environ['TW_CKEY']
consumer_secret = os.environ['TW_CSECRET']

access_token = os.environ['TW_ATOKEN']
access_secret = os.environ['TW_ASECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

reference_users = ["sanchit_raina",
					"easyamol",
					"shiffman",
					"SalihSarikaya",
					"NationalistRavi"
					]

time_instance = time.time()

i = 0
t0 = time.time()

def save_data(data):
	with open("unlabled/bio_{}.txt".format(time_instance), "a") as f:
		f.write(data+"\n")
		f.close()

class MutliThreadBio(threading.Thread):
	def __init__(self, username):
		threading.Thread.__init__(self)
		self.username = username

	def run(self):
		while 1:
			try:
				user = api.get_user(self.username)
				if len(user.description) > 3:
					print("Saving Bio:", user.screen_name)
					fo.write(user.description + '\n')
					time.sleep(random.uniform(0.1, 0.9))
				break
			except Exception as e:
				print("Error: ", e)
				print("\n\nRetrying in 15 minutes")
				time.sleep(915)
				pass


while i < len(reference_users):
	ids = []
	print("Getting friends of: ", reference_users[i])

	try:
		for page in tweepy.Cursor(api.friends_ids, \
								screen_name=reference_users[i]).pages():
			print("-")
			ids.extend(page)
		print("Total friends:", len(ids))

		# ===== Sequential Code ======
		'''for e in ids:
		 	user = api.get_user(e)
		 	print("Saving Bio:", user.screen_name)
		 	if len(user.description) > 3:
		 		total_bio+=1
		 		save_data(user.description)
		'''
		fo = open("unlabled/multi_bio.txt", "a")
		for i in ids:
			t = MutliThreadBio(username = i)
			t.start()
		i+=1
	except Exception as e:
		print("Error: ", e)
		print("\n\nRetrying in 15 minutes")
		time.sleep(915)
		pass


print("Time Taken:", time.time()-t0)
	
