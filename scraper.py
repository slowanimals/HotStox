import pandas as pd
import numpy as np
import praw
import time
from dotenv import load_dotenv
import os

load_dotenv("credentials.env")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

#initiate reddit bot
bot = praw.Reddit(username = USERNAME,
                  password = PASSWORD,
                  client_id = CLIENT_ID,
                  client_secret = CLIENT_SECRET,
                  user_agent = USER_AGENT
                  )

# INPUT: this function fetches a specified number of posts from a specified subreddit
# it is currently set up to find the top posts of the past 24 hours
# OUTPUT: a dictionary of the various attributes of each post
def fetch_submissions(subreddit, limit):
    subreddit = bot.subreddit(subreddit)
    posts = subreddit.top(limit = limit, time_filter = "day")
    data = []
    for p in posts:
        data.append({
            "subreddit" : str(p.subreddit),
            "submission id" : str(p.id),
            "author" : str(p.author) if p.author else None,
            "created_utc" : int(p.created_utc),
            "title" : str(p.title),
            "url" : str(p.url),
            "selftext" : str(p.selftext),
            "score" : int(p.score),
            "num_comments" : int(p.num_comments or 0),
            "is_self" : bool(p.is_self),
            "upvote_ratio" : float(p.upvote_ratio),
            "permalink" : f'https://www.reddit.com{p.permalink}'
        })
    return data
'''
t50_res = fetch_submissions("wallstreetbets", 50)
posts_df = pd.DataFrame(t50_res)
print(posts_df.head(20))
'''

# INPUT: a post's submission id
# this function fetches the top comments from a given post
# OUTPUT: a dictionary of all the retrieved comments and their respective attributes
def fetch_top_comments(submission_id):
    post = bot.submission(submission_id)
    post.comments.replace_more(limit = 0)
    cmts = []
    for c in post.comments:
        cmts.append({
            "submission id" : post.id,
            "comment id" : str(c.id),
            "author" : str(c.author) if c.author else None,
            "body" : str(c.body),
            "score" : int(c.score or 0),
            "permalink" : f'https://www.reddit.com{c.permalink}',
            "parent" : c.parent_id
        })
    return cmts
'''
cmts = fetch_top_comments("1ncqf7p")
cmts_df = pd.DataFrame(cmts)
print(cmts_df)
'''