import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, access_token, access_token_secret = loadkeys(twitter_auth_filename)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary
    """
    tweets_response = api.user_timeline(screen_name=name, count=100)
    tweets = []
    sent_analyzer_obj = SentimentIntensityAnalyzer()

    for t in tweets_response:
        tweet_info = dict()
        tweet_info['id'] = t.id
        tweet_info['created'] = t.created_at.date()
        tweet_info['retweeted'] = t.retweet_count
        tweet_info['text'] = t.text
        tweet_info['score'] = sent_analyzer_obj.polarity_scores(t.text)['compound']
        tweet_info['hashtags'] = [hashtag_dict['text'] for hashtag_dict in t.entities['hashtags']]
        # May need to experiment with different types of urls
        tweet_info['urls'] = [url_dict['expanded_url'] for url_dict in t.entities['urls']]
        tweet_info['mentions'] = [mention_dict['screen_name'] for mention_dict in t.entities['user_mentions']]
        tweets.append(tweet_info)

    return {'user': name, 'count': len(tweets_response), 'tweets': tweets}


        
    


def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get the list of User objects back from friends();
    get a maximum of 100 results. Pull the appropriate values from
    the User objects and put them into a dictionary for each friend.
    """
    friends_response = api.get_friends(screen_name=name, count=100)

    friends = []
    
    for f in friends_response:
        friends_dict = dict()
        friends_dict['name'] = f.name
        friends_dict['screen_name'] = f.screen_name
        friends_dict['followers'] = f.followers_count
        friends_dict['created'] = f.created_at.date()
        friends_dict['image'] = f.profile_image_url
        friends.append(friends_dict)
    
    return sorted(friends, reverse=True, key=lambda x: x['followers'])



if __name__ == '__main__':
    keys_filepath = "/Users/charu/USF/data_acquisition/secret_keys_do_not_deploy/twiter_combined.csv"
    api = authenticate(keys_filepath)
    profile = fetch_tweets(api, 'the_antlr_guy')
    # following = fetch_following(api, 'Charudatta_M')
    print(profile['user'], profile['count'])
    for tweet in profile['tweets']:
        print('_'*30)
        for k, v in tweet.items():
            print(k, ':', v)
    # for f in following:
    #     for k, v in f.items():
    #         print(k, ':', v)
