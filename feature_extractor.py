from typing import Dict, List
import spacy
from fetcher import TwitterAPI
import user_feature_funcs as uff
import content_feature_funcs as cff

nlp = spacy.load('en_core_web_lg', disable=['parser', 'ner'])


class FeatureExtractor(TwitterAPI):

    def __init__(self, usernames: List[str], max_tweets: int):
        super().__init__(usernames, max_tweets)
        
        self.user_vectors = None
        self.df = None
        self._get_user_feature_vector()


    def _get_user_feature_vector(self) -> None:
        for username in self.usernames:

            # self.users_infos[username].id=self.users_infos[username].user_id,
            self.users_infos[username].screen_name_length = len(self.users_infos[username].screen_name)
            self.users_infos[username].description_length = len(self.users_infos[username].description)
            self.users_infos[username].account_longevity = uff.get_longevity(self.users_infos[username].created_at)
            # self.users_infos[username].following_count = self.users_infos[username].following_count
            # self.users_infos[username].followers_count = self.users_infos[username].followers_count
            self.users_infos[username].following_to_followers = uff.get_following_to_followers(self.users_infos[username])
            # self.users_infos[username].tweet_count = self.users_infos[username].tweet_count
            self.users_infos[username].tweets_count_per_day = uff.get_tweets_per_day(self.users_infos[username])

            ##################

            links = cff.count_urls(self.users_infos[username].tweets)
            mentions = cff.count_mentions(self.users_infos[username].tweets)

            # "id":'u',
            self.users_infos[username].links_ratio = links[0]
            self.users_infos[username].unique_links_ratio = links[1]
            self.users_infos[username].mention_ratio = mentions[0]
            self.users_infos[username].unique_mention_ratio = mentions[1]
            self.users_infos[username].compression_ratio = cff.zip_ratio(self.users_infos[username].tweets)
            self.users_infos[username].similarity = cff.count_similarity(nlp,self.users_infos[username].tweets)