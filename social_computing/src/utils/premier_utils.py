import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import sklearn.preprocessing as preprocessing

def get_premier_info():
    premier_abbr = ['LEI', 'WHU', 'LEE', 'EVE', 'AST', 'NEW', 'WOL', 'PAL',
                    'SOT', 'BHA', 'BUR', 'FUL', 'WBA', 'SHW', 'CHE', 'ARS',
                    'LIV', 'MNC', 'MNU', 'TOT']

    premier_reddit_abbr = ['lcfc', 'Hammers', 'LeedsUnited', 'Everton', 'avfc', 'NewcastleUnited', 'WWFC',
                           'crystalpalace',
                           'SaintsFC', 'BrightonHoveAlbion', 'Burnley', 'fulhamfc', 'WBAfootball', 'SheffieldUnited',
                           'chelseafc', 'Gunners', 'LiverpoolFC', 'MCFC', 'reddevils', 'coys']

    premier_full_name = ['Leicester City','West Ham United','Leeds United','Everton','Aston Villa',
                         'Newcastle','Wolverhampton','Crystal Palace','Southampton','Brighton and Hove Albion',
                         'Burnley','Fulham','West Bromwich Albion','Sheffield United','Chelsea',
                         'Arsenal','Liverpool','Manchester City','Manchester United','Tottenham Hotspur']

    big_six_full_name = ['Chelsea','Arsenal','Liverpool','Manchester City','Manchester United','Tottenham Hotspur']

    is_big_six = [False,False,False,False,False,
                  False,False,False,False,False,
                  False,False,False,False,True,
                  True,True,True,True,True]

    end_season_rank = [5,6,9,10,11,
                       12,13,14,15,16,
                       17,18,19,20,4,
                       8,3,1,2,7]

    is_top_six = []
    is_last_six = []
    for i in range(20):
        is_top_six.append(end_season_rank[i]<=6)
        is_last_six.append(end_season_rank[i]>=15)

    return premier_abbr, premier_reddit_abbr, premier_full_name, big_six_full_name, is_big_six, end_season_rank, is_top_six, is_last_six

def create_table():
    premier_abbr, premier_reddit_abbr, premier_full_name, big_six_full_name, is_big_six, end_season_rank, is_top_six, is_last_six = get_premier_info()
    match_all = pd.read_csv('../../data/FiveThirtyEight/premier_match_2020.csv')
    time_all = pd.read_csv('../../data/utils/game_time.csv')
    df_all = pd.DataFrame()
    for team in range(20):
        df = pd.DataFrame()
        posts = pd.read_csv(f'../../data/posts/csvs/{premier_abbr[team]}.csv')
        name = premier_full_name[team]
        filter = (match_all['team1'] == name) | (match_all['team2'] == name)
        match = match_all.loc[filter]
        match = match.reset_index()

        filter = (time_all['team1'] == name) | (time_all['team2'] == name)
        time = time_all.loc[filter]
        time = time.reset_index()

        df['id'] = np.arange(1, 39, 1)

        df['date'] = match['date']
        df['time'] = match['date']+'T'+time['time']

        #if is_big_six[team]:
        #    df['is_big_six_true'] = np.ones(38)
        #    df['is_big_six_false'] = np.zeros(38)
        #else:
        #    df['is_big_six_false'] = np.ones(38)
        #    df['is_big_six_true'] = np.zeros(38)

        df['team'] = 38*[name]

        if is_big_six[team]:
            df['is_big_six'] = np.ones(38)
        else:
            df['is_big_six'] = np.zeros(38)

        df['end_season_rank'] = end_season_rank[team]*np.ones(38)

        df['top_team'] = df['end_season_rank']<=5
        df.loc[(df.top_team == True), 'top_team'] = 1
        df.loc[(df.top_team == False), 'top_team'] = 0

        df['bottom_team'] = df['end_season_rank'] >=16
        df.loc[(df.bottom_team == True), 'bottom_team'] = 1
        df.loc[(df.bottom_team == False), 'bottom_team'] = 0

        df.loc[(match.team1 == name), 'opponent'] = match['team2']
        df.loc[(match.team2 == name), 'opponent'] = match['team1']
        df['match_between_big_six'] = (df['is_big_six']>0) & (df['opponent'].isin(big_six_full_name))

        df.loc[(df.match_between_big_six == True), 'match_between_big_six'] = 1
        df.loc[(df.match_between_big_six == False), 'match_between_big_six'] = 0

        #df.loc[(df.match_between_big_six == True), 'match_between_big_six_false'] = 0
        #df.loc[(df.match_between_big_six == False), 'match_between_big_six_false'] = 1

        df.loc[(match.team1 == name), 'my_SPI'] = match['spi1']
        df.loc[(match.team2 == name), 'my_SPI'] = match['spi2']
        df.loc[(match.team2 == name), 'opponent_SPI'] = match['spi1']
        df.loc[(match.team1 == name), 'opponent_SPI'] = match['spi2']
        df['SPI_difference'] = abs(df['my_SPI'] - df['opponent_SPI'])

        df.loc[(match.team1 == name), 'win_prob'] = match['prob1']
        df.loc[(match.team2 == name), 'win_prob'] = match['prob2']
        df.loc[(match.team1 == name), 'my_importance'] = match['importance1']
        df.loc[(match.team2 == name), 'my_importance'] = match['importance2']


        df.loc[(match.team1 == name), 'my_goal'] = match['score1']
        df.loc[(match.team2 == name), 'my_goal'] = match['score2']
        df.loc[(match.team2 == name), 'opponent_goal'] = match['score1']
        df.loc[(match.team1 == name), 'opponent_goal'] = match['score2']
        df['is_win'] = df['my_goal'] > df['opponent_goal']
        df.loc[(df.is_win == True), 'is_win'] = 1
        df.loc[(df.is_win == False), 'is_win'] = 0
        df['is_tie'] = df['my_goal'] == df['opponent_goal']
        df.loc[(df.is_tie == True), 'is_tie'] = 1
        df.loc[(df.is_tie == False), 'is_tie'] = 0
        df['is_loss'] = df['my_goal'] < df['opponent_goal']
        df.loc[(df.is_loss == True), 'is_loss'] = 1
        df.loc[(df.is_loss == False), 'is_loss'] = 0
        df['is_win_tie'] = df['is_loss']==0
        df.loc[(df.is_win_tie == True), 'is_win_tie'] = 1
        df.loc[(df.is_win_tie == False), 'is_win_tie'] = 0
        df['top_team_not_win'] = (df['top_team']) & (df['is_win']==0)
        df.loc[(df.top_team_not_win == True), 'top_team_not_win'] = 1
        df.loc[(df.top_team_not_win == False), 'top_team_not_win'] = 0
        df['top_team_win'] = (df['top_team']) & (df['is_win'] == 1)
        df.loc[(df.top_team_win == True), 'top_team_win'] = 1
        df.loc[(df.top_team_win == False), 'top_team_win'] = 0

        df['bottom_team_win'] = (df['bottom_team']) & (df['is_win'] == 1)
        df.loc[(df.bottom_team_win == True), 'bottom_team_win'] = 1
        df.loc[(df.bottom_team_win == False), 'bottom_team_win'] = 0
        df['bottom_team_not_win'] = (df['bottom_team']) & (df['is_win'] == 0)
        df.loc[(df.bottom_team_not_win == True), 'bottom_team_not_win'] = 1
        df.loc[(df.bottom_team_not_win == False), 'bottom_team_not_win'] = 0




        '''
        posts["date"] = pd.to_datetime(posts['time'], format="%Y-%m-%d")
        posts["date"] = posts["date"].dt.date
        count_by_date = pd.DataFrame(posts['date'].groupby(posts['date']).count())
        count_by_date = count_by_date.rename(columns={"date": "count"})
        count_by_date['date'] = count_by_date.index
        count_by_date['date_str'] = count_by_date['date'].astype("str")
        count_by_date = count_by_date.reset_index(drop=True)

        comments_by_date = pd.DataFrame(posts['num_comments'].groupby(posts['date']).sum())
        comments_by_date['date'] = comments_by_date.index
        comments_by_date['date_str'] = comments_by_date['date'].astype("str")
        comments_by_date = comments_by_date.reset_index(drop=True)

        
        df['posts_count'] = np.zeros(38)
        for i in range(df.shape[0]):
            day = datetime.strptime(df['date'][i], '%Y-%m-%d')
            day_2 = (day + timedelta(days=1)).strftime('%Y-%m-%d')
            if df['date'][i] in list(count_by_date['date_str']):
                index = count_by_date[count_by_date['date_str'] == df['date'][i]].index[0]
                df['posts_count'][i] = count_by_date.iloc[index][0] + count_by_date.iloc[index + 1][0]
            elif day_2 in list(count_by_date['date_str']):
                index = count_by_date[count_by_date['date_str'] == day_2].index[0]
                df['posts_count'][i] = count_by_date.iloc[index][0] + count_by_date.iloc[index + 1][0]

        df['comments_count'] = np.zeros(38)
        for i in range(df.shape[0]):
            day = datetime.strptime(df['date'][i], '%Y-%m-%d')
            day_2 = (day + timedelta(days=1)).strftime('%Y-%m-%d')
            if df['date'][i] in list(comments_by_date['date_str']):
                index = comments_by_date[comments_by_date['date_str'] == df['date'][i]].index[0]
                df['comments_count'][i] = comments_by_date.iloc[index]['num_comments'] + \
                                          comments_by_date.iloc[index + 1]['num_comments']
            elif day_2 in list(comments_by_date['date_str']):
                index = comments_by_date[comments_by_date['date_str'] == day_2].index[0]
                df['comments_count'][i] = comments_by_date.iloc[index]['num_comments'] + \
                                          comments_by_date.iloc[index + 1]['num_comments']
        '''



        df.to_csv(f"../../data/match/{premier_abbr[team]}_match.csv",index=False)

        df_all = pd.concat([df_all,df])
    df_all.to_csv("../../data/analysis/match_regression_analysis.csv",index=False)
    return df_all

def match_troll_analysis(hour):
    premier_abbr,_,_,_,_,_,_,_ = get_premier_info()
    df = pd.DataFrame()
    big_six_df = pd.DataFrame()
    top_team_df = pd.DataFrame()
    bottom_team_df = pd.DataFrame()
    for team in premier_abbr:
        match = pd.read_csv(f'../../data/match/{team}_match.csv')
        comments = pd.read_csv(f'../../data/comments/gameday/labeled/{team}_gameday_comments_labeled.csv')
        comments['datetime'] = pd.to_datetime(comments.time)
        comments_count_list = []
        comments_troll_list = []
        troll_rate_list = []
        comments_votes_mean = []
        negative_votes_rate_list = []
        high_votes_rate_list = []
        high_votes_proportion_list = []
        high_votes_count_list = []
        thres = comments.ups.quantile(0.75)
        high_votes_total = 0
        for i in range(match.shape[0]):
            time = datetime.fromisoformat(match['time'][i])
            time_h = time + timedelta(hours=hour)
            comments_temp = comments[comments.datetime >= time]
            comments_temp = comments_temp[comments_temp.datetime <= time_h]
            high_votes_count = comments_temp[comments_temp.ups > thres].shape[0]
            high_votes_total += high_votes_count
        for i in range(match.shape[0]):
            time = datetime.fromisoformat(match['time'][i])
            time_h = time + timedelta(hours=hour)
            comments_temp = comments[comments.datetime >= time]
            comments_temp = comments_temp[comments_temp.datetime <= time_h]
            comments_count = comments_temp.shape[0]
            comments_troll_count = comments_temp[comments_temp.is_troll == 1].shape[0]
            negative_votes_count = comments_temp[comments_temp.ups<0].shape[0]
            high_votes_count = comments_temp[comments_temp.ups>thres].shape[0]
            if comments_count != 0:
                troll_rate = comments_troll_count / comments_count
                negative_votes_rate = negative_votes_count/comments_count
                high_votes_rate = high_votes_count/comments_count
                high_votes_proportion = high_votes_count/high_votes_total
            else:
                troll_rate = 0
                negative_votes_rate = 0
                high_votes_rate = 0
                high_votes_proportion = 0
            #scaler = preprocessing.MinMaxScaler()
            #votes_scale_param = scaler.fit(comments_temp['votes'])
            #df['votes_scaled'] = scaler.fit_transform(df['votes'],votes_scale_param)

            votes_mean = comments_temp.ups.mean()

            comments_count_list.append(comments_count)
            comments_troll_list.append(comments_troll_count)
            troll_rate_list.append(troll_rate)
            comments_votes_mean.append(votes_mean)
            negative_votes_rate_list.append(negative_votes_rate)
            high_votes_rate_list.append(high_votes_rate)
            high_votes_proportion_list.append(high_votes_proportion)
            high_votes_count_list.append(high_votes_count)
        match['comments_count'] = comments_count_list
        match['troll_count'] = comments_troll_list
        match['troll_rate'] = troll_rate_list
        match['comments_votes_mean'] = comments_votes_mean
        match['negative_votes_rate'] = negative_votes_rate_list
        match['high_votes_rate'] = high_votes_rate_list
        match['high_votes_proportion'] = high_votes_proportion_list
        match['high_votes_count'] = high_votes_count_list
        match = match.loc[match['comments_count']!=0]
        match.to_csv(f'../../data/match_troll/{hour}h/{team}_match_troll.csv',index=False)
        match = match.loc[match['comments_count']>=10]
        df = pd.concat([df, match])
        if match.is_big_six.iloc[0]==1:
            big_six_df = pd.concat([big_six_df,match])
        if match.top_team.iloc[0]==1:
            top_team_df = pd.concat([top_team_df,match])
        if match.bottom_team.iloc[0]==1:
            bottom_team_df = pd.concat([bottom_team_df,match])
    df.to_csv(f'../../data/match_troll/{hour}h/match_troll.csv',index=False)
    big_six_df.to_csv(f'../../data/match_troll/{hour}h/big_six_match_troll.csv',index=False)
    top_team_df.to_csv(f'../../data/match_troll/{hour}h/top_team_match_troll.csv', index=False)
    bottom_team_df.to_csv(f'../../data/match_troll/{hour}h/bottom_team_match_troll.csv', index=False)

def match_sentiment_analysis(hour):
    premier_abbr,_,_,_,_,_,_,_ = get_premier_info()
    df = pd.DataFrame()
    big_six_df = pd.DataFrame()
    top_team_df = pd.DataFrame()
    bottom_team_df = pd.DataFrame()
    for team in premier_abbr:
        match = pd.read_csv(f'../../data/match/{team}_match.csv')
        comments = pd.read_csv(f'../../data/comments/gameday/Sentiment/{team}_gameday_comments_sentiment.csv')
        comments = comments.loc[comments.sentiment_score!=0]
        comments['datetime'] = pd.to_datetime(comments.time)
        comments_count_list = []
        comments_votes_mean_list = []
        comments_votes_std_list = []
        negative_votes_rate_list = []
        high_votes_rate_list = []
        sentiment_score_list = []
        high_votes_sentiment_list = []
        negative_votes_sentiment_list = []
        positive_sentiment_rate_list = []
        negative_sentiment_rate_list = []
        positive_sentiment_votes_mean_list = []
        positive_sentiment_votes_std_list = []
        negative_sentiment_votes_mean_list = []
        negative_sentiment_votes_std_list = []
        thres = comments.ups.quantile(0.75)
        for i in range(match.shape[0]):
            time = datetime.fromisoformat(match['time'][i])
            time_h = time + timedelta(hours=hour)
            comments_temp = comments[comments.datetime >= time]
            comments_temp = comments_temp[comments_temp.datetime <= time_h]
            comments_count = comments_temp.shape[0]
            negative_votes = comments_temp[comments_temp.ups<0]
            negative_votes_count = negative_votes.shape[0]
            high_votes = comments_temp[comments_temp.ups>thres]
            high_votes_count = high_votes.shape[0]
            positive_sentiment = comments_temp[comments_temp.sentiment_score>=0.05]
            positive_sentiment_count = positive_sentiment.shape[0]
            negative_sentiment = comments_temp[comments_temp.sentiment_score<=-0.05]
            negative_sentiment_count = negative_sentiment.shape[0]
            if comments_count != 0:
                negative_votes_rate = negative_votes_count/comments_count
                high_votes_rate = high_votes_count/comments_count
                positive_sentiment_rate = positive_sentiment_count/comments_count
                negative_sentiment_rate = negative_sentiment_count/comments_count
            else:
                negative_votes_rate = 0
                high_votes_rate = 0
                positive_sentiment_rate = 0
                negative_sentiment_rate = 0

            votes_mean = comments_temp.ups.mean()
            votes_std = comments_temp.ups.std()
            sentiment_mean = comments_temp.sentiment_score.mean()
            high_votes_sentiment_mean = high_votes.sentiment_score.mean()
            negative_votes_sentiment_mean = negative_votes.sentiment_score.mean()
            positive_sentiment_votes_mean = positive_sentiment.ups.mean()
            positive_sentiment_votes_std = positive_sentiment.ups.std()
            negative_sentiment_votes_mean = negative_sentiment.ups.mean()
            negative_sentiment_votes_std = negative_sentiment.ups.std()
            comments_count_list.append(comments_count)
            comments_votes_mean_list.append(votes_mean)
            comments_votes_std_list.append(votes_std)
            negative_votes_rate_list.append(negative_votes_rate)
            high_votes_rate_list.append(high_votes_rate)
            sentiment_score_list.append(sentiment_mean)
            high_votes_sentiment_list.append(high_votes_sentiment_mean)
            negative_votes_sentiment_list.append(negative_votes_sentiment_mean)
            positive_sentiment_rate_list.append(positive_sentiment_rate)
            negative_sentiment_rate_list.append(negative_sentiment_rate)
            positive_sentiment_votes_mean_list.append(positive_sentiment_votes_mean)
            positive_sentiment_votes_std_list.append(positive_sentiment_votes_std)
            negative_sentiment_votes_mean_list.append(negative_sentiment_votes_mean)
            negative_sentiment_votes_std_list.append(negative_sentiment_votes_std)

        match['comments_count'] = comments_count_list
        match['comments_votes_mean'] = comments_votes_mean_list
        match['comments_votes_std'] = comments_votes_std_list
        match['negative_votes_rate'] = negative_votes_rate_list
        match['high_votes_rate'] = high_votes_rate_list
        match['sentiment_score'] = sentiment_score_list
        match['high_votes_sentiment_score'] = high_votes_sentiment_list
        match['negative_votes_sentiment_score'] = negative_votes_sentiment_list
        match['positive_sentiment_rate'] = positive_sentiment_rate_list
        match['negative_sentiment_rate'] = negative_sentiment_rate_list
        match['positive_sentiment_votes_mean'] = positive_sentiment_votes_mean_list
        match['positive_sentiment_votes_std'] = positive_sentiment_votes_std_list
        match['negative_sentiment_votes_mean'] = negative_sentiment_votes_mean_list
        match['negative_sentiment_votes_std'] = negative_sentiment_votes_std_list
        match = match.loc[match['comments_count']!=0]
        match.to_csv(f'../../data/match_sentiment/{hour}h/{team}_match_sentiment.csv',index=False)
        match = match.loc[match['comments_count']>=10]
        df = pd.concat([df, match])
        if match.is_big_six.iloc[0]==1:
            big_six_df = pd.concat([big_six_df,match])
        if match.top_team.iloc[0]==1:
            top_team_df = pd.concat([top_team_df,match])
        if match.bottom_team.iloc[0]==1:
            bottom_team_df = pd.concat([bottom_team_df,match])
    df.to_csv(f'../../data/match_sentiment/{hour}h/match_sentiment.csv',index=False)
    big_six_df.to_csv(f'../../data/match_sentiment/{hour}h/big_six_match_sentiment.csv',index=False)
    top_team_df.to_csv(f'../../data/match_sentiment/{hour}h/top_team_match_sentiment.csv', index=False)
    bottom_team_df.to_csv(f'../../data/match_sentiment/{hour}h/bottom_team_match_sentiment.csv', index=False)

if __name__ == "__main__":
    # create_table()
    match_troll_analysis(6)
    #match_sentiment_analysis(12)
