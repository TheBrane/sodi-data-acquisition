""" Code to do a basic Reddit pull using the hottest topics on a subreddit.  Simple bot to track posts
Aisha Pectyo, 8/8/2017"""

#---Import Libraries---#
import praw
from sklearn.datasets import fetch_20newsgroups

#---Credentials---#
#Credentials hidden.  Need to use your personal credentials
reddit = praw.Reddit(client_id='', client_secret='',user_agent='', username = '', password = '')
print(reddit.user.me()) #make sure your credentials work

#---Loop through subreddit---#
titles = [] #placeholder for posts' titles
urls = [] #placeholder for urls
for submission in reddit.subreddit('science').hot(limit=1000):
    titles.append(submission.title)
    urls.append(submission.url)
    
#---Create bot---#
"""All you need to do is make use of the stream object to indefinitely iterate over new submissions to a subreddit."""
subreddit = reddit.subreddit('science')
sub= subreddit.stream.submission()

#---Run loop to get info from bot---#
titles_bot = []
urls_bot = []
for submission in sub:
  titles_bot.append(submission.title)
        
#---Save to CSV file----#
