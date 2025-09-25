# HotStox

##### Link: https://hotstox.streamlit.app/

#### Have you ever felt FOMO from failing to cash in on a hype stock? If that's the case, I present to you a solution ;)
#### HotStox is a sentiment-analysis model that finds, ranks, and visualizes trending stock tickers across various Reddit investment communities so that you can catch the next big trend before any headlines do

<img width="648" height="473" alt="Screenshot 2025-09-25 at 9 50 12 AM" src="https://github.com/user-attachments/assets/1db52c46-2cc8-477e-a7bf-7c3b7ad78c7c" />

## Tech Used:
- Python
- FinBERT (via Hugging Face)
- Streamlit
- Pandas
- yfinance
- Regex

## Overview:
This application utilizes a: 
- Reddit scraper
- Financial sentiment analysis model (NLP)
- Ranking algorithm created and tuned by me
- Streamlit dashboard for visualization

## Scraper:
- Uses **PRAW** to scrape any subreddit with adjustable parameters for the subreddit, amount of posts desired, filter to sort the posts by
- **Designed to scalable** so that the scraper can be used for more general purposes
  - It is only is targetting stock tickers from helper functions that I created

## Sentiment Analysis
- Uses FinBERT by ProsusAI to process the scraped data
- Returns a pandas dataframe that provides vital information about the sentiment of a post's body as well as the average sentiment of its corresponding comments

## Ranker
- Combines data from the scraper and sentiment model
- Evaluates a clear final score for each ticker, and then ranks the them by their respective scores
- Ranking based on (in order of emphasis):
  - Average FinBERT score of the body of posts for each ticker
  - Average FinBERT score of comments for each ticker
  - Amount of mentions each  ticker has
  - Upvote Ratio
  - Upvotes

## Dashboard
- Based on the ranker's results, a dataframe is fed into a Streamlit interface for visualization
- It diplays each ticker in order of ranking alongside a visual chart of data from yfinance
- Additionally, each ticker is given a color for its sentiment:
  - 🟢 = positive
  - 🟡 = neutral
  - 🔴 = negative
## Optimizations
- **yfinance caching**: Stock data is cached for about 10 minutes to reduce API calls and avoid rate limits
- **Sentiment/Ranking caching**: Since the pipeline takes nearly a minute or more to process, results are cached for about 15 minutes

## Lessons Learned
- This is the first programming project that I've completed end-to-end, and it was an absolute joy to see it come to life
- It taught me:
  - How to build ML pipelines
  - How to create Python dependencies
  - How to debug and structure a project across multiple files
  - How to integrate multiple API's and work around their rate limits
  - How to create a clean UI
  - And that programming is **so much** fun!
