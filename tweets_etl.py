import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sqlite3
from getpass import getpass
import time

class PLDT_tweets:
    """
    A class object that contains methods to scrape tweets using the
    Twitter API.
    """
    def __init__(self, conn_path):
        print("Input Twitter API bearer key...")
        bearer_token = getpass()
        
        conn = sqlite3.connect(conn_path)
        self.conn = conn
        print(f"Connected to sqlite3 database {self.conn}")
        
        self.bearer_token = bearer_token
        self.account_info = None
    
    
    def get_username_account_info(self, username):
        """
        Accepts a username and searches for the Twitter account with the given
        username using the endpoin url "https://api.twitter.com/2/users/by/
        username/:username". Returns a dictionary of select user.fields
        of the Twitter account.
        """
        try:
            response = (requests
                        .get(f'https://api.twitter.com/2/users/by/username/{username}',
                             headers={'Authorization': f'Bearer {self.bearer_token}'},
                             params={"user.fields": "created_at,description,id,location,name,username,url,verified"})
                        .json()
                        )
        except:
            print("Invalid request: check username input or bearer_token")
        
        response_data = response.get('data')
        self.account_info = response_data
        return response_data
    
    
    def to_sql_table(self, df, tbl_name):
        with self.conn:
            df.to_sql(tbl_name, if_exists='replace', index=False, con=self.conn)
        print(f"Stored scraped tweets in sqlite database with table name '{tbl_name}'")


    def display_sql_tables(self):
        with self.conn:
            print(self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
    
    
    def search_tweets(self, query, sql_tbl_name):
        """
        Accepts a query and searches Twitter for tweets following the given
        query until the last page of results.
        """
        store_data = []
        params = {"query": query,
                  'max_results': 100,
                  'tweet.fields': 'author_id,conversation_id,created_at,' \
                                  'in_reply_to_user_id,public_metrics,' \
                                  'possibly_sensitive,text,lang',
                  'place.fields':'country,country_code,name,place_type,geo',
                  'expansions': 'author_id',
                  'user.fields': 'id,username,created_at,location,description'}
        headers = {'Authorization': f'Bearer {self.bearer_token}'}

        next_token = 0
        page = 1
        start_time = time.time()
        print(f"Scraping tweets...")
        while True:
            if page == 1:
                print(f"At page {page}")
            elif page % 2 == 0:
                print(f"At page {page}")

            search_tweets = (requests
                            .get(f'https://api.twitter.com/2/tweets/search/recent',
                                 headers=headers, params=params).json())
            next_token = search_tweets.get('meta').get('next_token')
            data_ = search_tweets.get('data')
            store_data.extend(data_)

            if next_token is None:
                print(f"Last page {page}")
                break
            else:
                params.update({"pagination_token": f"{next_token}"})
            page += 1
            time.sleep(0.5)

        end_time = time.time() - start_time
        print(f"Total scrape time is {end_time:.2f} seconds")
        
        
        df_tweets = pd.json_normalize(store_data).drop(columns='edit_history_tweet_ids')
        self.to_sql_table(df_tweets, sql_tbl_name)