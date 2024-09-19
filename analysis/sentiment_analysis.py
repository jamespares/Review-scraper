# File: sentiment_analysis.py

import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load your data
reviews = pd.read_csv('reviews.csv')  # Ensure this CSV is obtained legally

# Define a function to get sentiment polarity
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply the function to your dataset
reviews['Sentiment'] = reviews['ReviewText'].apply(get_sentiment)

# Plot the sentiment distribution
plt.hist(reviews['Sentiment'], bins=20)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Frequency')
plt.show()