import os
import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

# Set the environment variables.
twitter_consumer_key = os.environ['PERSONALITY_MATCH_CONSUMER_KEY']
twitter_consumer_secret = os.environ['PERSONALITY_MATCH_CONSUMER_SECRET']
twitter_access_token = os.environ['PERSONALITY_MATCH_ACCESS_TOKEN']
twitter_access_secret = os.environ['PERSONALITY_MATCH_ACCESS_SECRET']

# Create an instance of the Twitter API
twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)


# Retrieve data from Twitter
handle = "@khwilo"
statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
