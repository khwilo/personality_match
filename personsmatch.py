import os
import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def get_twitter_client():
  try:
    # Set the environment variables.
    twitter_consumer_key = os.environ['PERSONALITY_MATCH_CONSUMER_KEY']
    twitter_consumer_secret = os.environ['PERSONALITY_MATCH_CONSUMER_SECRET']
    twitter_access_token = os.environ['PERSONALITY_MATCH_ACCESS_TOKEN']
    twitter_access_secret = os.environ['PERSONALITY_MATCH_ACCESS_SECRET']
  except KeyError:
    sys.stderr.write("TWITTER_* environment variables not set\n")
    sys.exit(1)

  # Create an instance of the Twitter API.
  twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

  return twitter_api

def get_pi_client():
  try:
    # IBM Bluemix credentials for Personality Insights
    pi_username = os.environ['PI_USERNAME']
    pi_password = os.environ['PI_PASSWORD']
  except KeyError:
    sys.stderr.write("PI_* environment variables not set\n")
    sys.exit(1)

  # Create Personality Insights instance
  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

  return personality_insights


def analyze(handle):
  # Retrieve data from Twitter.
  statuses = get_twitter_client().GetUserTimeline(screen_name=handle, count=200, include_rts=False)

  # This variable saves tweets.
  # Convert to bytes first.
  text = b"" 
  #text = "".encode() -> method 2

  # View the results.
  for status in statuses:
    if (status.lang == 'en'):
      text += status.text.encode('utf-8')

  pi_result = get_pi_client().profile(text)
  
  return pi_result

def flatten(orig):
  data = {}
  
  for c in orig['tree']['children']:
    if 'children' in c:
      for c2 in c['children']:
        if 'children' in c2:
          for c3 in c2['children']:
            if 'children' in c3:
              for c4 in c3['children']:
                if (c4['category'] == 'personality'):
                  data[c4['id']] = c4['percentage']
                  if 'children' not in c3:
                    if (c3['category'] == 'personality'):
                      data[c3['id']] = c3['percentage']

  return data 


def compare(dict1, dict2):
  compared_data = {}
  for keys in dict1:
    if dict1[keys] != dict2[keys]:
      compared_data[keys] = abs(dict1[keys] - dict2[keys])
  
  return compared_data

user_handle = "@khwilo"
match_handle = "@jadytrix"


user_result = analyze(user_handle)
match_result = analyze(match_handle)


user = flatten(user_result)
match = flatten(match_result)

compared_results = compare(user, match)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
  print(keys),
  print(user[keys]),
  print('->'),
  print(match[keys]),
  print('->'),
  print(compared_results[keys])
