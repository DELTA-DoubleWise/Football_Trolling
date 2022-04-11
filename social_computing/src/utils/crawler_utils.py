import praw
import pandas as pd
import numpy as np
import requests
from praw.models import MoreComments
import datetime as dt
from psaw import PushshiftAPI
from tqdm import tqdm
import pickle
import dill
from datetime import datetime,timedelta
import tqdm.notebook as tq

TIMEOUT_AFTER_COMMENT_IN_SECS = .350

club_reddit_abbr = ['ACMilan', 'atletico', 'Barca', 'borussiadortmund', 'chelseafc', 'fcbayern', 'FCInterMilan',
                    'Gunners',
                    'Juve', 'LiverpoolFC', 'MCFC', 'psg', 'realmadrid', 'reddevils', 'roma', 'coys']

premier_other_reddit_abbr = ['lcfc', 'Hammers','LeedsUnited', 'Everton','avfc','NUFC','WWFC','crystalpalace',
                       'SaintsFC','BrightonHoveAlbion','Burnley','fulhamfc','WBAfootball','SheffieldUnited']

premier_reddit_abbr = ['lcfc', 'Hammers','LeedsUnited', 'Everton','avfc','NUFC','WWFC','crystalpalace',
                       'SaintsFC','BrightonHoveAlbion','Burnley','fulhamfc','WBAfootball','SheffieldUnited',
                       'chelseafc','Gunners','LiverpoolFC','MCFC','reddevils','coys']

premier_team_full_name = ['Leicester City','West Ham United', 'Leeds United', 'Everton', 'Aston Villa', 'Newcastle United','Wolverhampton Wanderers',
                          'Crystal Palace','Southampton','Brighton','Burnley','Fulham','West Bromwich Albion','Sheffield United',
                          'Chelsea','Arsenal','Liverpool','Manchester City','Manchester United','Tottenham Spurs']

TOT_abbr = ['coys','PremierLeague','soccer','football','ThreeLions']
all_abbr = ['lcfc', 'Hammers','LeedsUnited', 'Everton','avfc','NUFC','WWFC','crystalpalace',
                       'SaintsFC','BrightonHoveAlbion','Burnley','fulhamfc','WBAfootball','SheffieldUnited',
                       'chelseafc','Gunners','LiverpoolFC','MCFC','reddevils','coys','PremierLeague','soccer','football','ThreeLions']

club_abbr = ['MIL', 'AMD', 'BAR', 'DOR', 'CHE', 'MUN', 'INT', 'ARS',
             'JUV', 'LIV', 'MNC', 'PSG', 'RMD', 'MNU', 'ROM', 'TOT']

premier_other_abbr = ['LEI','WHU','LEE','EVE','AST','NEW','WOL','PAL',
                    'SOT','BHA','BUR','FUL','WBA','SHW']

premier_abbr = ['LEI','WHU','LEE','EVE','AST','NEW','WOL','PAL',
                      'SOT','BHA','BUR','FUL','WBA','SHW','CHE','ARS',
                      'LIV', 'MNC','MNU','TOT']

target_player = ['Kane', 'Sterling', 'Walker', 'Stones', 'Pickford', 'Lingard']
target_player_1 = ['Kane','Sterling','Stones']
player_club = ['coys','MCFC','MCFC']

player_group1 = ['Sterling','Bruyne','Stones','Mahrez', 'Kane', 'Rashford', 'Lingard']

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
    return headers


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

def time_generation_year(y):
    start_time_list = []
    end_time_list = []
    end_day_lunar = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    end_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for year in range(2021-y,2022):
        if year==2016 or year==2020:
            for m in range(12):
                start_time_list.append(int(dt.datetime(year, m+1, 1).timestamp()))
                end_time_list.append(int(dt.datetime(year, m+1, end_day_lunar[m]).timestamp()))
        else:
            for m in range(12):
                start_time_list.append(int(dt.datetime(year, m + 1, 1).timestamp()))
                end_time_list.append(int(dt.datetime(year, m + 1, end_day[m]).timestamp()))

    return start_time_list,end_time_list


def list_flatten(target):
    return [item for sublist in target for item in sublist]


def transform_df(filename):
    with open(filename, 'rb') as file:
        posts = dill.load(file)
    posts = list_flatten(posts)
    posts_info = [post[-1] for post in posts]
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
            'upvote_ratio': post['upvote_ratio'],
            'self_text': post['selftext'] if 'selftext' in post else ''

        }, ignore_index=True)
    return df

def parse_dates(df):
    dates = df['created_utc'].astype(int)
    real_dates = []
    for date in dates:
        real_dates.append(datetime.fromtimestamp(date)-timedelta(hours=8))
    df['time'] = real_dates
    df['time_str'] = df['time'].astype("str")
    return df

def praw_init():
    return praw.Reddit(client_id='bCnE1U61Wqixgs2wy28POg', client_secret='vEY7k3_j7o3PZZvP-tEt6DnhWr1x5A',
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')

def extract_comments_by_praw(reddit, filename, columns):
    comments = pd.DataFrame(columns = columns)
    #reddit = praw_init()
    data = pd.read_csv(filename)
    data_comments_50 = data.loc[data['num_comments']>=50]
    if data_comments_50.shape[0]>=100:
        for i in tqdm(range(len(data_comments_50))):
            uid = data_comments_50.iloc[i]['id']
            subreddit = data_comments_50.iloc[i]['subreddit']
            time = data_comments_50.iloc[i]['time']
            title = data_comments_50.iloc[i]['title']
            submission = reddit.submission(id=uid)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comments = comments.append({'comments': comment.body, 'post_id': uid, 'subreddit': subreddit,
                                            'time': time, 'title': title},
                                           ignore_index=True)

                #if TIMEOUT_AFTER_COMMENT_IN_SECS > 0:
                    #time.sleep(TIMEOUT_AFTER_COMMENT_IN_SECS)
            '''
            for top_level_comment in tqdm(submission.comments):
                if isinstance(top_level_comment, MoreComments):
                    for cid in top_level_comment.children:
                        comments = comments.append({'comments': reddit.comment(cid).body, 'post_id': uid, 'subreddit': subreddit,
                                                    'time': time, 'title': title},
                                                   ignore_index=True)
                else:
                    comments = comments.append({'comments': top_level_comment.body, 'post_id': uid, 'subreddit': subreddit,
                                                'time': time, 'title': title},
                                               ignore_index=True)
            '''

    return comments

def extract_comments_by_psaw(filename, columns):
    api = PushshiftAPI()
    comments = pd.DataFrame(columns=columns)
    data = pd.read_csv(filename)
    data_comments_50 = data.loc[data['num_comments'] >= 50]
    if data_comments_50.shape[0] >= 100:
        for i in tqdm(range(len(data_comments_50))):
            uid = data_comments_50.iloc[i]['id']
            subreddit = data_comments_50.iloc[i]['subreddit']
            time = data_comments_50.iloc[i]['date']
            title = data_comments_50.iloc[i]['title']
            comment_ids = api._get_submission_comment_ids(uid)
            for cid in tqdm(comment_ids):
                gen = api.search_comments(ids=cid)
                comment = next(gen).body
                comments = comments.append(
                            {'comments': comment, 'post_id': uid, 'subreddit': subreddit,
                             'time': time, 'title': title},
                            ignore_index=True)
    return comments


def extract_comments_by_api(filename,columns):
    comments = pd.DataFrame(columns=columns)
    headers = api_initialization()
    posts = pd.read_csv(filename)
    posts_comments = posts.loc[posts['num_comments'] >= 50]
    subreddit = posts['subreddit'][0]
    if posts_comments.shape[0] >= 100:
        iter = 0
        for uid in tq.tqdm(posts_comments['id']):
            if iter%200 == 0:
                headers = api_initialization()
            iter += 1
            try:
                url = f"https://oauth.reddit.com/r/{subreddit}/comments/{uid}/"
                res = requests.get(url, headers=headers)
                comment_list = res.json()[1]
                comments = get_comment(comment_list,comments,uid)
            except Exception as e:
                comments.to_csv(f'../data/comments/temp{iter}.csv',index=False)
                pass
            continue
    return comments


def extract_gameday_comments(filename,matchfilename,columns):
    comments = pd.DataFrame(columns=columns)
    headers = api_initialization()
    posts = pd.read_csv(filename)
    posts['datetime'] = pd.to_datetime(posts.time)
    match = pd.read_csv(matchfilename)
    posts_comments = pd.DataFrame()
    for i in range(match.shape[0]):
        time = datetime.fromisoformat(match['time'][i])
        time_48h = time+timedelta(hours=48)
        post_temp = posts[posts.datetime>=time]
        posts_temp = post_temp[post_temp.datetime<=time_48h]
        posts_comments = pd.concat([posts_comments,posts_temp])

    subreddit = posts['subreddit'][0]
    iter = 0
    for uid in tq.tqdm(posts_comments['id']):
        if iter%200 == 0:
            headers = api_initialization()
        iter += 1
        try:
            url = f"https://oauth.reddit.com/r/{subreddit}/comments/{uid}/"
            res = requests.get(url, headers=headers)
            comment_list = res.json()[1]
            comments = get_comment(comment_list,comments,uid)
        except Exception as e:
            comments.to_csv(f'../data/comments/temp{iter}.csv',index=False)
            pass
        continue
    return comments

def get_comment(comment_list,df,post_id):
    comment_list = comment_list['data']['children']
    for comment in comment_list:
        c_text, c_id, c_post, c_subreddit, c_time, c_author, c_ups = None, None, None, None, None, None, None
        c_post = post_id
        if 'body' in comment['data']:
            c_text = comment['data']['body']
        if 'id' in comment['data']:
            c_id = comment['data']['id']
        if 'subreddit' in comment['data']:
            c_subreddit = comment['data']['subreddit']
        if 'created_utc' in comment['data']:
            c_time = datetime.fromtimestamp(int(comment['data']['created_utc']))
        if 'author' in comment['data']:
            c_author = comment['data']['author']
        if 'ups' in comment['data']:
            c_ups = comment['data']['ups']
        df = df.append(
            {'text': c_text, 'id': c_id, 'post_id': c_post, 'subreddit': c_subreddit,
             'time': c_time, 'author': c_author, 'ups': c_ups},
            ignore_index=True)
        if 'replies' in comment['data'] and comment['data']['replies'] != '':
            df = get_comment(comment['data']['replies'],df,post_id)
    return df

def get_gameday_comments(subreddit,matchfilename):
    match = pd.read_csv(matchfilename)
    r = praw.Reddit(client_id='bCnE1U61Wqixgs2wy28POg', client_secret='vEY7k3_j7o3PZZvP-tEt6DnhWr1x5A',
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')
    api = PushshiftAPI(r)
    start_time = []
    end_time = []
    for i in range(match.shape[0]):
        time = datetime.fromisoformat(match['date'][i])
        start_time.append(time)
        time_3day = time + timedelta(days=3)
        end_time.append(time_3day)

    df = pd.DataFrame()
    for i in tq.tqdm(range(len(start_time))):
        gen = api.search_comments(before=end_time[i], after=start_time[i], subreddit=subreddit,
                                  filter=['author', 'body', 'subreddit', 'id', 'ups', 'created_utc'])
        results_df = pd.DataFrame({'subreddit': row.subreddit, 'id': row.id, 'time': datetime.fromtimestamp(int(row.created_utc)),
                                   'author': row.author, 'ups': row.ups, 'body': row.body} for row in gen)
        df = pd.concat([df, results_df])
    return df