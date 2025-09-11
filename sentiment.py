import scraper as sc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk

df = sc.fetch_submissions("wallstreetbets", 10)
print(df.head())