from typing import Dict, List
import os
import requests
from dotenv import load_dotenv

load_dotenv('twitter.env')

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

class UserInfo:

    def __init__(self,
                 username: str,
                 user_id: str,
                 screen_name: str,
                 description: str,
                 created_at: str,
                 following_count: int,
                 followers_count: int,
                 tweet_count: int):
        
        self.username: str = username,
        self.user_id: str = user_id
        self.screen_name: str = screen_name
        self.description: str = description
        self.created_at: str = created_at
        self.following_count: int = following_count
        self.followers_count: int = followers_count
        self.tweet_count: int = tweet_count
        self.tweets: List[Dict[str, str]] = None
        self.screen_name_length: int = None
        self.description_length: int = None
        self.account_longevity: int = None
        self.following_to_followers: float = None
        self.tweets_count_per_day: float = None
        self.links_ratio: float = None
        self.unique_links_ratio: float = None
        self.mention_ratio: float = None
        self.unique_mention_ratio: float = None
        self.compression_ratio: float = None
        self.similarity: float = None


class TwitterAPI:
    
    def __init__(self, usernames: List[str], max_tweets: int=5) -> None:

        self.usernames: List[str] = usernames
        self.users_infos: Dict[str, UserInfo] = dict()
        self._make_api_call(max_tweets)

    def _get_users_info(self) -> None:
        payload = {
            "user.fields": "id,description,created_at,public_metrics"
        }

        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        
        for username in self.usernames:
            try:
                response = requests.get(
                    url=f'https://api.twitter.com/2/users/by/username/{username}',
                    headers=headers,
                    params=payload
                )

                response_json = response.json()['data']

                user_info = UserInfo(
                    username=username,
                    user_id=response_json["id"],
                    screen_name=response_json["name"],
                    description=response_json["description"],
                    created_at=response_json["created_at"],
                    following_count=response_json["public_metrics"]["following_count"],
                    followers_count=response_json["public_metrics"]["followers_count"],
                    tweet_count=response_json["public_metrics"]["tweet_count"]
                )

                self.users_infos[username] = user_info

            except Exception:
                self.users_infos[username] = None


    def _get_users_tweets(self, max_tweets: int) -> None:
        payload = {
            "max_results": max_tweets
        }

        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

        for username in self.usernames:
            try:
                user_id = self.users_infos[username].user_id

                response = requests.get(
                    url=f'https://api.twitter.com/2/users/{user_id}/tweets',
                    headers=headers,
                    params=payload
                )

                response_json = response.json()['data']

                tweets = [{"id": t["id"], "text": t["text"]} for t in response_json]

                self.users_infos[username].tweets = tweets

            except Exception as oops:
                print(oops)
                self.users_infos[username].tweets = None


    def _make_api_call(self, max_tweets: int=5) -> None:
        self._get_users_info()
        self._get_users_tweets(max_tweets)