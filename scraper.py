import pandas as pd
import praw
import time
# from dotenv import load_dotenv
import os
import regex as re

# load_dotenv("credentials.env")

bot = praw.Reddit(
    # username=st.secrets["REDDIT_USERNAME"],
    # password=st.secrets["REDDIT_PASSWORD"],
    client_id=st.secrets["REDDIT_CLIENTID"],
    client_secret=st.secrets["REDDIT_CLIENTSECRET"],
    user_agent=st.secrets["REDDIT_USER_AGENT"],
)

'''
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
'''

# INPUT: this function fetches a specified number of posts from a specified subreddit
# it is currently set up to find the top posts of the past 24 hours
# OUTPUT: a dataframe of the various attributes of each post
def fetch_submissions(subreddit, limit, filter):
    subreddit = bot.subreddit(subreddit)
    posts = subreddit.top(limit = limit, time_filter = filter)
    data = []
    for p in posts:
        data.append({
            "subreddit" : str(p.subreddit),
            "submission_id" : str(p.id),
            "author" : str(p.author) if p.author else None,
            "created_utc" : int(p.created_utc),
            "title" : str(p.title),
            "body" : str(p.selftext),
            "url" : str(p.url),
            "selftext" : str(p.selftext),
            "score" : int(p.score),
            "num_comments" : int(p.num_comments or 0),
            "is_self" : bool(p.is_self),
            "upvote_ratio" : float(p.upvote_ratio),
            "permalink" : f'https://www.reddit.com{p.permalink}'
        })
    posts_df = pd.DataFrame(data)
    return posts_df
'''
t50_res = fetch_submissions("wallstreetbets", 50)
posts_df = pd.DataFrame(t50_res)
print(posts_df.head(20))
'''

# INPUT: a post's submission id
# this function fetches the top comments from a given post
# OUTPUT: a dataframe of all the retrieved comments and their respective attributes
def fetch_top_comments(submission_id):
    post = bot.submission(submission_id)
    post.comments.replace_more(limit = 0)
    cmts = []
    for c in post.comments:
        cmts.append({
            "submission_id" : str(post.id),       
            "comment_id" : str(c.id),              
            "author" : str(c.author) if c.author else None,
            "body" : str(c.body) if c.body is not None else "",
            "score" : int(c.score or 0),
            "permalink" : f'https://www.reddit.com{c.permalink}',
            "parent" : c.parent_id
        })
    cmts_df = pd.DataFrame(cmts)

    if cmts_df.empty:
        return pd.DataFrame(columns=["submission_id","comment_id","body","score","created_utc","parent"])

    cmts_df["body"] = cmts_df["body"].fillna("")
    return cmts_df

'''
cmts = fetch_top_comments("1ncqf7p")
cmts_df = pd.DataFrame(cmts)
print(cmts_df)
'''
#compares post bodies to nsdq and then adds a col of mentioned tickers
def post_extract_tickers(df, nsdq):
    df_copy = df.copy()
    stoplist = {"AI", "USA", "US", "YOLO", "GAINZ", "HODL", "IT", "CEO", "GDP", "UK"}
    pattern = re.compile(r'\$?[A-Z]{2,5}\b')
    df_copy["content"] = df_copy["title"].fillna("") + " " + df_copy["body"].fillna("")
    df_copy["p_mentioned"] = df_copy["content"].apply(lambda text: pattern.findall(text))
    df_copy["p_mentioned"] = df_copy["p_mentioned"].apply(lambda tickers: [t.lstrip("$") for t in tickers])
    df_copy["p_mentioned"] = df_copy["p_mentioned"].apply(lambda tickers: list(set(t for t in tickers)))
    df_copy["p_mentioned"] = df_copy["p_mentioned"].apply(lambda tickers: [t for t in tickers if t not in stoplist])
    df_copy["p_mentioned"] = df_copy["p_mentioned"].apply(lambda tickers: [t for t in tickers if t in nsdq])
    return df_copy

def cmts_extract_tickers(id, nsdq):
    df = fetch_top_comments(id)
    stoplist = {"USA", "US", "YOLO", "GAINZ", "HODL", "IT", "CEO", "GDP"}
    pattern = re.compile(r'\$?[A-Z]{2,5}\b')
    df["c_mentioned"] = df["body"].apply(lambda text: pattern.findall(text))
    df["c_mentioned"] = df["c_mentioned"].apply(lambda tickers: [t.lstrip("$") for t in tickers])
    df["c_mentioned"] = df["c_mentioned"].apply(lambda tickers: list(set(t for t in tickers)))
    df["c_mentioned"] = df["c_mentioned"].apply(lambda tickers: [t for t in tickers if t not in stoplist])
    df["c_mentioned"] = df["c_mentioned"].apply(lambda tickers: [t for t in tickers if t in nsdq])
    return df

def get_cmt_tickers(id, nsdq):
    df = cmts_extract_tickers(id, nsdq)
    all_tickers = [ticker for sublist in df["c_mentioned"] for ticker in sublist]
    return list(set(all_tickers))

#simplified way to clean nasdaq csv, returns a list of tickers
def nsdq_tickers(csv):
    raw_nsdq_df = pd.read_csv(csv)
    cleaned_nsdq = raw_nsdq_df["Symbol"].str.replace(r'[\^.-].*$', "")
    nsdq = set(cleaned_nsdq)
    return nsdq


#get tickers from NASDAQ
# raw_nsdq_df = pd.read_csv("nasdaq.csv")
# cleaned_nsdq = raw_nsdq_df["Symbol"].str.replace(r'[\^.-].*$', "")  # removes ^.- and anything after, anchored at end by $
# nsdq = set(cleaned_nsdq)


# nsdq = nsdq_tickers("nasdaq.csv")
# print(nsdq)

#get dataframe of subreddit to analyze
# posts = fetch_submissions("wallstreetbets", 100)  # top posts of the day
# print(posts.info())

# extracted = post_extract_tickers(posts, nsdq)
# print(extracted.head())
# cmts_extracted = cmts_extract_tickers(extracted["submission_id"][2], nsdq)
# print(cmts_extracted.head)

# cmts = fetch_top_comments("1ndwms0")
# print(cmts)
