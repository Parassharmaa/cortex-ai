import json 
import requests
from textblob import TextBlob
from instafetch import Instafetch
import os
import time

dir_path = os.path.join("..", "_data", "insta_captions")

file_name = "insta_{}.txt".format(int(time.time()))

if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
    print("Directory Created")

def is_english(t):
    t = t.replace("#", "")
    chk = TextBlob(t)
    if chk.detect_language() == 'en':
        return True
    return False

def fetch_hashtags(tag):
    I  = Instafetch()
    print("Fetching data...")
    I.explore(tag, pages=1)
    all_posts = I.posts
    captions = []
    print("Data fetch complete: [{}]".format(tag))
    for i in all_posts['data']:
        c = i['caption']
        if is_english(c):
            captions.append(c+"\n")
    for cp in captions:        
        try:
            with open(os.path.join(dir_path, file_name), "a") as f:
                f.write(cp)
        except Exception as e:
            print("Error", e)
            pass
    print("Saved Caption for #",tag)
 
if __name__ == "__main__":
    hashtags = ["cool", "tech", "hello"]
    for h in hashtags:       
        fetch_hashtags(h)
