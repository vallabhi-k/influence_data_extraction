from datetime import datetime, date
import time
from itertools import dropwhile, takewhile
import csv
import instaloader
import random
from argparse import ArgumentParser
import os
import pickle

import csv
import pandas as pd

import json
import boto3
from random import shuffle

access_key = 'AKIA244KK3IEPDBO6XWU'
secret_access_key = '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'

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key
    )

bucket = 'influencer-file-set'
bucket_file_path = 's3://influencer-file-set/'
comments_file_path = 's3://influencer-file-set/comments.csv'
users_file_path = 's3://influencer-file-set/Users.csv'
post_information_file_path = 's3://influencer-file-set/PostsInformation.csv'


def getData(entered_name):
    bot = instaloader.Instaloader(max_connection_attempts=1, download_videos=False, save_metadata=False,
                                  post_metadata_txt_pattern='')
    bot.load_session_from_file('influencerabc2', 'session-influencerabc2')

    while True:
        try:
            profile = instaloader.Profile.from_username(bot.context, entered_name)
            # print(profile)
            print("Username: ", profile.username)
            # print("Number of Posts: ", profile.mediacount)
            posts = profile.get_posts()
            # print("retireved posts:")
            today = date.today()
            year = int(today.strftime("%Y"))
            month = int(today.strftime("%m"))
            day = int(today.strftime("%d"))

            sinceyear = year

            sincemonth = month - 6
            if (sincemonth <= 0):
                # reducing the year if the month is in prev year
                sinceyear = year - 1
                # changing the month to be of the years month.
                sincemonth += 12

            # dd/mm/YY
            SINCE = datetime(sinceyear, sincemonth, day)
            UNTIL = datetime(year, month, day)
            top_50_posts = 50
            counter = 0

            with open('Users.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Posts Count", "Followees", "Followers", "Verified status", "Bio"])
                # likes = set()
                print("Fetching likes of all posts of profile {}.".format(profile.username))

                verified_status = "Verified" if profile.is_verified == True else "Not Verified"
                writer.writerow(
                    [entered_name, profile.mediacount, profile.followees, profile.followers, verified_status,
                     profile.biography])

            comments_list = []

            print("data entered in abv csv, now adding to influencername.csv")
            with open('PostsInformation.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Username", "Caption", "Caption Mentions", "Hashtags", "Is sponsored", "Sponsor users", "Location",
                     "Likes"])
                for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
                    if counter <= top_50_posts:
                        comments_user = post.get_comments()
                        ctr = 0
                        for itr in comments_user:
                            if ctr <= 10:
                                comments_list.append(itr.text)
                                ctr += 1
                            else:
                                break
                        located_at = post.location.name if post.location is not None else "None"
                        writer.writerow([entered_name, post.caption, post.caption_mentions, post.caption_hashtags,
                                         post.is_sponsored, post.sponsor_users, located_at, post.likes])
                        counter += 1
                    else:
                        break

            with open('comments.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Comments"])
                for itr in comments_list:
                    writer.writerow([entered_name, itr])

            break


        except Exception as e:
            print("Oops!  That was no valid username.  Try again...")
            print(e)
            break


def create_local_files():
    # read from s3 and create local file
    obj = s3.get_object(Bucket=bucket, Key='Users.csv')
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.reader(data)

    with open('Users.csv', 'w') as file:
        writer_obj = csv.writer(file)
        for row in records:
            writer_obj.writerow(row)

    obj = s3.get_object(Bucket=bucket, Key='PostsInformation.csv')
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.reader(data)

    with open('PostsInformation.csv', 'w') as file:
        writer_obj = csv.writer(file)
        for row in records:
            writer_obj.writerow(row)

    obj = s3.get_object(Bucket=bucket, Key='comments.csv')
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.reader(data)

    with open('comments.csv', 'w') as file:
        writer_obj = csv.writer(file)
        for row in records:
            writer_obj.writerow(row)


def write_local_files():
    # write back to s3
    users_df = pd.read_csv('Users.csv')
    users_df.to_csv(users_file_path, index=False)

    postsInfo_df = pd.read_csv('PostsInformation.csv')
    postsInfo_df.to_csv(post_information_file_path, index=False)

    comments_df = pd.read_csv('comments.csv')
    comments_df.to_csv(comments_file_path, index=False)

users_list = []
with open('Brands.csv', 'r') as file:
    reader_obj = csv.reader(file)
    for row in reader_obj:
        if row[0] != 'Username':
            users_list.append(row[0])

shuffle(users_list)

while True:
    create_local_files()
    for i in range(5):
        getData(users_list[0])
        users_list.append(users_list[0])
        users_list.pop(0)

    write_local_files()
    time.sleep(86400)

