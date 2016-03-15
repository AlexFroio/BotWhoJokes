import praw
import OAuth2Util
import pprint

user_agent = ("JokerPractice v0.1 by DukeCarge")

r = praw.Reddit(user_agent = user_agent)
o = OAuth2Util.OAuth2Util(r, server_mode=True)
r.login("BotWhoJokes", "RobotHumor42????")
o.refresh(force = True)
thing_limit = 10
jokeWords = ["joke"]
already_done = []

while True:
    
    subreddit = r.get_subreddit("botwhojokes")
    for submission in subreddit.get_hot(limit=thing_limit):
        op_text = submission.selftext.lower()
        has_joke = any(string in op_text for string in jokeWords)
        if submission.id not in already_done and has_joke:
            r.reply("Reading you clear!")
    
    
