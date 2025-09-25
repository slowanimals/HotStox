import pandas as pd
from huggingface_hub import InferenceClient
# from dotenv import load_dotenv
from transformers import pipeline
import os
import scraper as sc
import streamlit as st

# load_dotenv("/Users/kaush/Documents/Hotstox/credentials.env")
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(api_key = hf_token)

clf = pipeline("text-classification", model="ProsusAI/finbert")
nsdq = sc.nsdq_tickers("nasdaq.csv")

#fetches any amount of posts from a specified sub
def df_fetch(sub, amount, filter):
    df = sc.fetch_submissions(sub, amount, filter)
    df = sc.post_extract_tickers(df, nsdq)
    df = df[df["p_mentioned"].astype(bool)]
    return df

#runs finbert analysis on dataframe's posts and merges results 
def fb_posts(df):
    res = {}
    for i, row in df.iterrows():
        text = row["content"]
        sub_id = row["submission_id"]
        result = clf(text, truncation=True)[0]
        res[sub_id] = {
            'fb_label' : result["label"],
            'fb_score' : result["score"]
        }
    
    finbert_df = pd.DataFrame(res).T
    finbert_df = finbert_df.reset_index().rename(columns={"index":"submission_id"})
    #ensure ids are same type and then merge
    finbert_df["submission_id"] = finbert_df["submission_id"].astype(str)
    df["submission_id"] = df["submission_id"].astype(str)
    merged = df.merge(finbert_df, how = 'right')
    return merged

#runs finbert analysis on dataframe's comments and merges results
def fb_cmts(df):
    cmt_scores = {}
    for i, row in df.iterrows():
        cmts_df = sc.fetch_top_comments(row["submission_id"])
        if cmts_df.empty:
            avg_compound = None
        else:
            #fibert result for each comment
            finbert_results = cmts_df["body"].apply(lambda x: clf(x, truncation=True)[0])
            #extract scores/labels
            scores = finbert_results.apply(lambda x: x["score"])
            labels = finbert_results.apply(lambda x: x["label"])
            #collapse
            avg_score = scores.mean()
            avg_label = labels.mode()[0]
        cmt_scores[row["submission_id"]] = {
            'c_label' : avg_label,
            'c_score' : avg_score
        }
    comment_scores_df = pd.DataFrame.from_dict(cmt_scores, orient = 'index')
    comment_scores_df = comment_scores_df.reset_index().rename(columns = {'index' : 'submission_id'})
    #ensure id is standardized
    comment_scores_df["submission_id"] = comment_scores_df["submission_id"].astype(str)
    merged = df.merge(comment_scores_df, on='submission_id', how='right')

    return merged

#reformates dataframe for sanity
def format(df):
    wanted_cols = [
    "submission_id",
    "title",
    "body",
    "p_mentioned",
    "fb_label",
    "fb_score",
    "c_label",
    "c_score"
]
    other_cols = [col for col in df.columns if col not in wanted_cols]
    merged = df[wanted_cols + other_cols]
    return merged

def run_sent(subreddit, amount, filter):
    df = df_fetch(subreddit, amount, filter)
    df = fb_posts(df)
    df = fb_cmts(df)
    df = format(df)
    return df


