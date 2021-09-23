import praw
import pandas as pd
import numpy as np
import requests
from praw.models import MoreComments
import datetime as dt
from psaw import PushshiftAPI
from tqdm import tqdm
from utils import crawler_utils
from utils.crawler_utils import time_initialization

api = PushshiftAPI()

club_reddit_abbr = ['ACMilan', 'atletico', 'Barca', 'borussiadortmund', 'chelseafc', 'fcbayern', 'FCInterMilan', 'Gunners',
             'Juve', 'LiverpoolFC', 'MCFC', 'psg', 'realmadrid', 'reddevils', 'roma', 'Tottenham']

club_abbr = ['MIL', 'AMD', 'BAR', 'DOR', 'CHE', 'MUN', 'INT', 'ARS',
             'JUV', 'LIV', 'MNC', 'PSG', 'RMD', 'MNU', 'ROM', 'TOT']

MIL_list = []
AMD_list = []
BAR_list = []
DOR_list = []
CHE_list = []
MUN_list = []
INT_list = []
ARS_list = []
JUV_list = []
LIV_list = []
MNC_list = []
PSG_list = []
RMD_list = []
MNU_list = []
ROM_list = []
TOT_list = []
all_list = [MIL_list, AMD_list, BAR_list, DOR_list, CHE_list, MUN_list, INT_list, ARS_list,
            JUV_list, LIV_list, MNC_list, PSG_list, RMD_list, MNU_list, ROM_list, TOT_list]

start_time, end_time = time_initialization()

for club_index in tqdm(range(len(all_list))):
    for i in tqdm(range(len(start_time))):
        all_list[club_index].append(list(api.search_submissions(after=start_time[i], before=end_time[i],
                                                                subreddit=club_reddit_abbr[club_index],
                                                                filter=['url', 'author', 'title', 'subreddit', 'id',
                                                                        'num_comments', 'score', 'ups', 'upvote_ratio'])
                                         ))
    temp_list = np.array(all_list[club_index])
    np.save(f'{club_abbr[club_index]}.npy', temp_list)
