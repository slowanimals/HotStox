
import sentiment as sent
import pandas as pd

def rank(df):
    exploded = df.copy().explode("p_mentioned")
    exploded["fb_score"] = exploded["fb_score"].astype(float)
    exploded["p_mentioned"] = exploded["p_mentioned"].astype(str)

    #ensure all cols are numeric values
    exploded["fb_score"] = pd.to_numeric(exploded['fb_score'],errors='coerce')
    exploded['c_score'] = pd.to_numeric(exploded['c_score'],errors='coerce')
    exploded['upvote_ratio'] = pd.to_numeric(exploded['upvote_ratio'],errors='coerce')
    exploded['score'] = pd.to_numeric(exploded['score'],errors='coerce')

    #aggregate dataframe
    aggregate = exploded.groupby('p_mentioned').agg(
    mentions = ('p_mentioned','size'),
    post_sent = ('fb_score','mean'),
    cmt_sent = ('c_score','mean'),
    upvote_ratio = ('upvote_ratio','mean'),
    upvotes = ('score','mean')
    ).reset_index().sort_values(
    ['mentions','post_sent','cmt_sent','upvote_ratio','upvotes'], 
    ascending=[False,False,False,False,False])

    #normalize aggregated values
    aggregate['mentions'] = aggregate['mentions'] / aggregate['mentions'].max()
    aggregate['upvotes'] = aggregate['upvotes'] / aggregate['upvotes'].max()

    #weight all the values and come up with a final score
    rank = aggregate.copy()
    rank['score_final'] = (
        0.75 * rank['mentions'] +
        0.85 * rank['post_sent'] +
        0.8 * rank['cmt_sent'] +
        0.4 * rank['upvote_ratio'] +
        0.6 * rank['upvotes']
    )

    #finally rank by the scores given
    rank = rank.reset_index().sort_values('score_final', ascending = False)
    return rank


def run_ranker(subreddit, amount, filter):
    df = sent.run_sent(subreddit,amount,filter)
    ranked_df = rank(df)
    return ranked_df

