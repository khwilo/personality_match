import os
import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

twitter_consumer_key = os.environ['PERSONALITY_MATCH_CONSUMER_KEY']
twitter_consumer_secret = os.environ['PERSONALITY_MATCH_CONSUMER_SECRET']
twitter_access_token = os.environ['PERSONALITY_MATCH_ACCESS_TOKEN']
twitter_access_secret = os.environ['PERSONALITY_MATCH_ACCESS_SECRET']
