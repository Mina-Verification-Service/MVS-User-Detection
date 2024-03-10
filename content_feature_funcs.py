import re
import os
import zipfile

def count_urls(tweets):
    total = len(tweets)
    unique =[]
    for val in tweets:
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', val['text'])
        unique += urls
    count = len(unique)
    unique_count = len(set(unique))
    return count/total, unique_count/total


def count_mentions(tweets):
    total = len(tweets)
    unique =[]
    for val in tweets:
        mentions = re.findall(r'@(?:[a-zA-Z]|[0-9]|[_+])+',val['text'])
        unique += mentions
    count = len(unique)
    unique_count = len(set(unique))
    return count/total, unique_count/total


def count_similarity(nlp, tweets):
    tweets = [t['text'] for t in tweets]
    num = len(tweets)
    if num == 1:
        return 1
    else:
        for i in range(num):
            tweets[i] = nlp(tweets[i])
        
        similarity = 0
        for i in range(num):
            ti = tweets[i]
            for j in range(i+1, num):
                similarity += ti.similarity(tweets[j])

        pairs = num*(num-1)/2
        avg = similarity / pairs
        return avg
    
def zip_ratio(tweets):
    filepath = "./temp_tweets.txt"
    zip_filepath = './temp_tweets.txt.zip'
    with open(filepath, "w") as f:
        for val in tweets:
            f.write(val['text']+'\n')
    unzip_size = os.path.getsize(filepath)
    
    if not os.path.exists(filepath):
        print('File not exist')
    else:
        zips = zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED)
        zips.write(filepath)
        
    zip_size = os.path.getsize(zip_filepath)
    return unzip_size/zip_size







