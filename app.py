#-*- coding:utf8
from secret import *
from tweepy import API, OAuthHandler, TweepError
from time import *

import pip

# If there is no tweepy, it will install the package auto
pip.main(["install","tweepy"])

print("[+] Prepare to start")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = API(auth)

me = api.me()
last_tweet = {}

print(f"[+] Start Bot - {me.name}")

followers = me.followers_ids()

while True:
    print(f"[+] Check {len(followers)} followers")

    for follower in followers:
        # to response to "Rate Limit exceeded"
        sleep(2)

        try:
            if last_tweet.get(follower) is not None:
                tweets = api.user_timeline(follower, since_id=last_tweet[follower], count=5)
            else:
                tweets = api.user_timeline(follower, count=5)

        except TweepError as e:
            print(f"[!] Occured TweepError : {e.reason}")
            if e.reason is "Not Authorized":
                followers.pop(follower)
            break

        print(f"[+] Checking follower - {api.get_user(follower).name}, tweet cnt = {len(tweets)}")

        if len(tweets) > 0:
            last_tweet[follower] = tweets[0].id

        for tweet in tweets:
            if "추춰" in tweet.text and not tweet.favorited:
                tweet.favorite()
                api.update_status(f"@{tweet.author.screen_name} 당신은 추춰를 말했습니다!!", in_reply_to_status_id=tweet.id)

    print(f"[+] Checked {len(followers)} followers")