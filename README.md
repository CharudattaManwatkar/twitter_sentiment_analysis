# Twitter Sentiment Analysis

This is a small project I made using 'tweepy', which is a python wrapper around Twitter API.

You Can enter a twitter handle and the program will get you:
* A sentiment score for each of the last 100 tweets by that handle
* List of the twitter accounts followed by the handle.

![](home.png?)

## Sentiment Analysis
I used VaderSentiment to do the sentiment analysis. It gives a single score (-1 for negative to +1 for positive) for the overall sentiment of that tweet.Positive sentiment tweets are coloerd in green while negative sentiment tweets are colored in red. I also provide the median sentiment score for the last 100 tweets.

![](sentiments.png?)

## Following List
We get a list of other twitter accounts being followed by the handle of our choice. We can also see their profile picture, their follower count, and their account creation date.

![](followers.png?)


