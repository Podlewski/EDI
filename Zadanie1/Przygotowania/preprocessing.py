import arff
from datetime import timedelta
import pandas as pd
import sys


file_name = sys.argv[1]

# CONSTANS
popular_site_percent = 0.5
fixed_session_duration = 10 * 60 


df = pd.read_csv(file_name, sep=' ', header=None, na_values='-',
    error_bad_lines=False, nrows=5000, usecols=[0,3,5,6,7],
    names=['host', 'timestamp', 'request', 'status', 'bytes'])

## PART 1
df = df.iloc[:50000]

## PART 2
df['timestamp'] = pd.to_datetime(df['timestamp'], format='[%d/%b/%Y:%H:%M:%S')
df['date'] = [d.date() for d in df['timestamp']]
df['time'] = [d.time() for d in df['timestamp']]
df['date'] = df['date'].astype('str')
df['time'] = df['time'].astype('str')

request_pack = df['request'].str.split(' ').str
df['method'] = request_pack[0]
df['url'] = request_pack[1]
df['protocol'] = request_pack[2]
df.drop('request', axis=1, inplace=True)

df['bytes'] = pd.to_numeric(df['bytes'], errors='coerce')
df['bytes'].fillna(0, inplace=True)
df['bytes'] = df['bytes'].astype('int64')

df = df[df['method'] == 'GET']
df = df[df['status'] == 200]
df = df[~df['url'].str.contains('.jpg|.gif|.bmp|.xbm|.png|.jpeg')]

users = df['host'].unique() 

sites_counts = df['url'].value_counts().rename('count')
sites_percents = (df['url'].value_counts(normalize=True) * 100).rename('percent')

sites = pd.concat([sites_counts, sites_percents], axis=1)
sites = sites.reset_index().rename({'index': 'url'}, axis=1)

## PART 3
popular_sites = sites[sites['percent'] > popular_site_percent]

sessions = []
clear_popular_sites_dict = {b : False for b in popular_sites['url']}

for user in users:
    requests = pd.DataFrame(df[df['host'] == user])

    session_start = requests.iloc[0]['timestamp']
    session_end = session_start
    popular_sites_dict = clear_popular_sites_dict
    requests_count = 0

    for index, request in requests.iterrows():
        if request['timestamp'] - session_end > timedelta(seconds=fixed_session_duration):
            session_duration = (session_end - session_start).total_seconds()
            avg_request_duration = session_duration / requests_count 

            sessions.append({**{'user': user, 'duration': session_duration,
                                'requests_count': requests_count,
                                'avg_request_duration': avg_request_duration},
                             **popular_sites_dict})

            session_start = request['timestamp']
            popular_sites_dict = clear_popular_sites_dict
            requests_count = 0

        if request['url'] in popular_sites_dict:
            popular_sites_dict[request['url']] = True
        requests_count += 1 
        session_end = request['timestamp']

sessions_df = pd.DataFrame(sessions)
sessions_df.to_csv(file_name + '_sessions.csv', index=False)

arff.dump(file_name + '_sessions.arff',
          sessions_df.values,
          relation=file_name,
          names=sessions_df.columns)