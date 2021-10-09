import praw
import pandas as pd
import numpy as np
import requests
from praw.models import MoreComments
import datetime as dt
from psaw import PushshiftAPI
from tqdm import tqdm
import pickle
from datetime import datetime

club_reddit_abbr = ['ACMilan', 'atletico', 'Barca', 'borussiadortmund', 'chelseafc', 'fcbayern', 'FCInterMilan',
                    'Gunners',
                    'Juve', 'LiverpoolFC', 'MCFC', 'psg', 'realmadrid', 'reddevils', 'roma', 'Tottenham']

club_abbr = ['MIL', 'AMD', 'BAR', 'DOR', 'CHE', 'MUN', 'INT', 'ARS',
             'JUV', 'LIV', 'MNC', 'PSG', 'RMD', 'MNU', 'ROM', 'TOT']


# reddit api initialization
def api_initialization():
    auth = requests.auth.HTTPBasicAuth('bCnE1U61Wqixgs2wy28POg', 'vEY7k3_j7o3PZZvP-tEt6DnhWr1x5A')

    data = {'grant_type': 'password',
            'username': 'Delta_Wang11',
            'password': 'delta113420'
            }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


def time_initialization():
    start_time_list = []
    end_time_list = []
    year = [2020, 2020, 2020, 2020, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021]
    month = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
    end_day = [30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31]

    for i in range(12):
        start_time_list.append(int(dt.datetime(year[i], month[i], 1).timestamp()))
        end_time_list.append(int(dt.datetime(year[i], month[i], end_day[i]).timestamp()))

    return start_time_list, end_time_list


def list_flatten(target):
    return [item for sublist in target for item in sublist]


def transform_df(filename):
    with open(filename, 'rb') as file:
        posts = pickle.load(file)
    posts = list_flatten(posts)
    posts = np.array(posts)
    posts_info = posts[:, 10]
    df = pd.DataFrame()
    for post in posts_info:
        df = df.append({
            'author': post['author'],
            'id': post['id'],
            'created_utc': post['created_utc'],
            'subreddit': post['subreddit'],
            'url': post['url'],
            'title': post['title'],
            'num_comments': post['num_comments'],
            'score': post['score'],
            'upvote_ratio': post['upvote_ratio']
        }, ignore_index=True)
    return df

def parse_dates(df):
    dates = df['created_utc'].astype(int)
    real_dates = []
    for date in dates:
        real_dates.append(datetime.fromtimestamp(date))
    df['date'] = real_dates
    return df

def praw_init():
    return praw.Reddit(client_id='bCnE1U61Wqixgs2wy28POg', client_secret='vEY7k3_j7o3PZZvP-tEt6DnhWr1x5A',
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')

def extract_comments(filename, columns):
    comments = pd.DataFrame(columns = columns)
    reddit = praw_init()
    data = pd.read_csv(filename)
    data_comments_50 = data.loc[data['num_comments']>=50]
    if data_comments_50.shape[0]>=100:
        for i in range(len(data_comments_50)):
            uid = data_comments_50.iloc[i]['id']
            subreddit = data_comments_50.iloc[i]['subreddit']
            time = data_comments_50.iloc[i]['date']
            title = data_comments_50.iloc[i]['title']
            submission = reddit.submission(id=uid)
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    for cid in top_level_comment.children:
                        comments = comments.append({'comments': reddit.comment(cid).body, 'post_id': uid, 'subreddit': subreddit,
                                                    'time': time, 'title': title},
                                                   ignore_index=True)
                else:
                    comments = comments.append({'comments': top_level_comment.body, 'post_id': uid, 'subreddit': subreddit,
                                                'time': time, 'title': title},
                                               ignore_index=True)
    return comments



