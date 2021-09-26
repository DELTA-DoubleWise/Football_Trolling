import praw
import pandas as pd
import numpy as np
import requests
from praw.models import MoreComments
import datetime as dt
from psaw import PushshiftAPI
from tqdm import tqdm
import pickle
from utils import crawler_utils
from utils.crawler_utils import time_initialization, club_abbr, club_reddit_abbr

api = PushshiftAPI()

start_time, end_time = time_initialization()

for club_index in tqdm(range(len(club_abbr))):
    temp_list = []
    for i in tqdm(range(len(start_time))):
        temp_list.append(np.array(list(api.search_submissions(after=start_time[i], before=end_time[i],
                                                              subreddit=club_reddit_abbr[club_index],
                                                              filter=['url', 'author', 'title', 'subreddit', 'id',
                                                                      'num_comments', 'score', 'ups', 'upvote_ratio'])
                                       )))
    file = open(f'./data/{club_abbr[club_index]}.pickle', 'wb')
    pickle.dump(temp_list, file)
    file.close()
