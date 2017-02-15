import json
import os

import logging

import sys
import textwrap

import tweepy
import tweepy.error

from ..School import School
from .NotificationDispatcher import NotificationDispatcher


class TwitterDispatcher(NotificationDispatcher):

    def __init__(self):
        self.logger = logging.getLogger("TwitterDispatcher")
        self.logger.debug("Loading Twitter config info...")
        if os.path.isfile(os.path.join(os.getcwd(), "twitter_config.json")):
            with open(os.path.join(os.getcwd(), "twitter_config.json"), "r") as f:
                self.config = json.load(f)
        else:
            self.logger.error("twitter_config.json not found, creating...")
            self.config = {
                "CONSUMER_KEY": "",
                "CONSUMER_SECRET": "",
                "ACCESS_KEY": "",
                "ACCESS_SECRET": "",
                "TWEET_FORMAT": "Status for {twitter} updated. New status: {status}"
            }
            with open(os.path.join(os.getcwd(), "twitter_config.json"), "w") as f:
                json.dump(self.config, f, indent=4, sort_keys=True)

        try:
            self.logger.debug("Authenticating with Twitter...")
            self.auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"], self.config["CONSUMER_SECRET"])
            self.auth.set_access_token(self.config["ACCESS_KEY"], self.config["ACCESS_SECRET"])
            self.api = tweepy.API(self.auth)
            if self.api.verify_credentials():
                self.logger.debug("Authenticated with Twitter.")
        except tweepy.error.TweepError:
            self.logger.error("Failed to authenticate with Twitter. Please correct the settings in "
                              "twitter_config.json and restart.")
            sys.exit(1)

    def dispatch_notification(self, school: School, new_status: str):
        twitter = getattr(school, "twitter", school.name)
        tweet = self.config["TWEET_FORMAT"].format(twitter=twitter, status=new_status)
        truncated_tweet = textwrap.shorten(tweet, 140, placeholder="...")
        if not os.getenv("SCHOOLTRACKER_DEBUG", False):
            self.api.update_status(truncated_tweet)
        else:
            self.logger.debug(truncated_tweet)


