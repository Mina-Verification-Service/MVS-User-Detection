import tweepy
from os import getenv
from dotenv import load_dotenv
import logging

load_dotenv()


# twitter API endpoint documentation and parameters
# https://developer.twitter.com/en/docs/twitter-api/fields
TWEET_FIELDS = ["referenced_tweets", "in_reply_to_user_id", "entities"]
# https://developer.twitter.com/en/docs/twitter-api/expansions
EXPANSIONS = ["referenced_tweets.id.author_id"]


def setup_logging(log_fname):
    """Set up logging for model
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s.%(msecs)06f %(message)s',
                                  datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_fname)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def log_response_errors(logger, errors):
    """Write any request error to the log file
    """

    if len(errors) > 0:
        for i, error in enumerate(errors):
            title = error["title"]
            detail = error["detail"]
            debug_msg = f"Error #{i} {title}: {detail}"
            logger.debug(debug_msg)


def handleEnv(key):
    value = getenv(key)
    if (value != None):
        return value
    raise Exception("set env file with key '{}' value".format(key))


def setup_twitter_client():
    """Loads bearer token for Twitter API from file and uses it to authenticaate with Twitter.

    Returns: tweepy client.Client: Tweepy client used for accessing Twitter API
    """

    client = tweepy.Client(bearer_token=handleEnv(
        "BEARER_TOKEN"), return_type=tweepy.Response, wait_on_rate_limit=True)

    return client
