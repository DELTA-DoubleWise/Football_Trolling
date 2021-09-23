import praw
import pandas as pd
import requests
from praw.models import MoreComments
import datetime as dt
from psaw import PushshiftAPI
from tqdm import tqdm


# reddit api initialization
def api_initialization():
    auth = requests.auth.HTTPBasicAuth('bCnE1U61Wqixgs2wy28POg','vEY7k3_j7o3PZZvP-tEt6DnhWr1x5A')

    data = {'grant_type': 'password',
        'username': 'Delta_Wang11',
        'password': 'delta113420'
        }

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

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




