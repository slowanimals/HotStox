![hotstoxlogo](https://github.com/user-attachments/assets/2023706c-9c5f-4eb8-af54-a849af733d69)

HotStox is a sentiment-analysis model that finds, ranks, and visualizes trending stock tickers across various investment communities in Reddit, with the current options being r/wallstreetbets, r/investing, and r/stocks (more will be added in the future).

<img width="973" height="710" alt="Screenshot 2025-09-25 at 9 19 33 AM" src="https://github.com/user-attachments/assets/1a5e48ca-5745-4b73-924f-428d0ca813fe" />

## How It's Made:
**Tech Used**: Python, FinBERT (Hugging Face Inference), Streamlit, Pandas, yfinance, Regex
This application utilizes a scraper, financial sentiment analysis model via natural language processing, and a ranking algorithm created and tuned by me. \n
The scraper uses PRAW to scrape any subreddit with adjustable parameters for the subreddit, amount of posts desired, the filter to sort the posts by. Because its scalability, the scraper can be used for more general purposes, and only is targetting stock tickers from helper functions that I created. \n
The sentiment analysis model uses FinBERT by ProsusAI to process the scraped data. It returns a pandas dataframe that provides vital information about the sentiment of a post's body as well as the average sentiment of its corresponding comments. \n
The ranker takes in data from the scraper and sentiment model to evaluate a clear final score for each ticker, and then ranks the them by their respective scores. I've designed the ranking system to place an emphasis on the average sentiment score for the posts, and comments, as well as the amount of mentions each respective ticker has. \n
Based on the ranker's results, a dataframe is fed into a Streamlit interface for visualization. The interface displays each ticker in order of ranking and also uses data from yfinance to create a visual chart of the past month of each stock's performance. Additionally, each ticker is given a color for its sentiment, green meaning positive, yellow meaning neutral, and red meaning negative.

https://hotstox.streamlit.app/
