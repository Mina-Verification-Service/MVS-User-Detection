import re
import datetime
import calendar
import sys

def get_user_id(user):
    return user['id']


def get_longevity(created_at):
    year, month, other_time = created_at.split('-')
    day = other_time.split('T')[0]
    year, month, day = int(year), int(month), int(day)
    create_time = datetime.datetime(year, month, day)
    collect_time = datetime.datetime(2020, 10, 1)
    longevity = (collect_time - create_time).days
    
    return longevity


def get_screen_name_length(user):
    screen_name = user['name']
    if screen_name is None:
        return 0
    else:
        return len(screen_name)


def get_description_length(user):
    des = user['description']
    if des is None:
        return 0
    else:
        return len(des)


def get_following(user):
    following_count = user['public_metrics']['following_count']
    if following_count is None:
        return 0
    else:
        return int(following_count)


def get_followers(user):
    followers_count = user['public_metrics']['followers_count']
    if followers_count is None:
        return 0
    else:
        return int(followers_count)


def get_following_to_followers(user_info):
    followers_count = user_info.followers_count
    following_count = user_info.following_count
    if followers_count is None or following_count is None:
        return 0.0
    if int(followers_count) == 0:
        return 0.0        
    else:
        return int(following_count) / int(followers_count)


def get_tweets(user):
    tweets = user['public_metrics']['tweet_count']
    if tweets is None:
        return 0
    else:
        return int(tweets)


def get_tweets_per_day(user_info):
    tweet_count = user_info.tweet_count
    num_days = get_longevity(user_info.created_at)
    if num_days == 0:
        return tweet_count
    return tweet_count / num_days
