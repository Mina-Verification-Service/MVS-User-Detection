from typing import Dict, List
import joblib
import numpy as np
from feature_extractor import FeatureExtractor


class Classifier(FeatureExtractor):

    def __init__(self, usernames: List[str], max_tweets: int=5):
        super().__init__(usernames, max_tweets)

        self.features = None
        self.model = None

    def _prepare_df(self):
        features = []
        for username in self.usernames:
            row = [
                self.users_infos[username].screen_name_length,
                self.users_infos[username].description_length,
                self.users_infos[username].account_longevity,
                self.users_infos[username].following_count,
                self.users_infos[username].followers_count,
                self.users_infos[username].following_to_followers,
                self.users_infos[username].tweet_count,
                self.users_infos[username].tweets_count_per_day,
                self.users_infos[username].links_ratio,
                self.users_infos[username].unique_links_ratio,
                self.users_infos[username].mention_ratio,
                self.users_infos[username].unique_mention_ratio,
                self.users_infos[username].compression_ratio,
                self.users_infos[username].similarity
            ]

            features.append(row)
        
        self.features = np.array(features)
        

    def _load_model(self) -> None:
        self.model = joblib.load('model/model.joblib')

    
    def predict(self) -> Dict:
        self._prepare_df()
        self._load_model()
        
        prediction = self.model.predict(self.features)

        result = dict()
        for username, p in zip(self.usernames, prediction):
            if p == 1:
                result[username] = 'bot'
            else:
                result[username] = 'human'

        return result