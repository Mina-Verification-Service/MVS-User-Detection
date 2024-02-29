
import tweepy
from utils import TWEET_FIELDS, EXPANSIONS, \
    setup_logging, log_response_errors, setup_twitter_client


client = setup_twitter_client()
logger = setup_logging


def fetch_user_tweet(user_id,
                     start_timestamp,
                     end_timestamp,
                     per_user_tweet_count_limit=None):
    """Makes a request to twitter API for tweets in a date range.

    Args:
        user_id (int): id for user to fetch tweets from
        start_datetime (pd.Timestamp): date range starting timestamp
        end_datetime (pd.Timestamp): date range ending timestamp
        per_user_tweet_count_limit (int): number of tweets to limit request
            if you want all tweets in the date range, set to None (default)

    Returns:
        tweet_list (list of pd.Series): the tweets returned from the API
            each tweet is stored as a Series with only the relevant fields needed for graph making

    Notes:
        https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_all_tweets
    """

    max_results = per_user_tweet_count_limit if\
        per_user_tweet_count_limit is not None else 500  # current twitter request max
    get_users_tweets_kwargs = {"max_results": max_results,
                               "start_time": start_timestamp,
                               "end_time": end_timestamp,
                               "tweet_fields": TWEET_FIELDS,
                               "expansions": EXPANSIONS}
    # want all tweets in date range, use tweepy result Paginator
    if per_user_tweet_count_limit is None:
        responses = tweepy.Paginator(client.search_all_tweets,
                                     "from:" + str(user_id), **get_users_tweets_kwargs)
    # only want per_user_tweet_count_limit tweets in this date range
    else:
        responses = [client.search_all_tweets(
            "from:" + str(user_id), **get_users_tweets_kwargs)]

    for response in responses:
        if response.data is not None:
            return response.data
        else:
            log_response_errors(logger, response.errors)
