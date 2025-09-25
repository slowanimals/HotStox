# HotStox

HotStox is a sentiment-analysis model that finds, ranks, and visualizes trending stock tickers across various Reddit investment communities 

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

## Scraper:
- Uses **PRAW** to scrape any subreddit with adjustable parameters for the subreddit, amount of posts desired, filter to sort the posts by
- **Designed to scalable**, so the scraper can be used for more general purposes, and only is targetting stock tickers from helper functions that I created

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
- Diplays each ticker in order of ranking alongside a visual chart of data from yfinance
- Additionally, each ticker is given a color for its sentiment:
  - 🟢 = positive
  - 🟡 = neutral
  - 🔴 = negative

https://hotstox.streamlit.app/
