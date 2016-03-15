import praw
import OAuth2Util
import pprint

user_agent = ("JokerPractice v0.1 by DukeCarge")

r = praw.Reddit(user_agent = user_agent)
o = OAuth2Util.OAuth2Util(r, server_mode=True)
r.login("BotWhoJokes", "RobotHumor42????", disable_warning=True)
o.refresh(force = True)
thing_limit = 10
botname = ["BotWhoJokes"]
jokeWords = ["joke"]
already_done = []

while True:
    
    subreddit = r.get_subreddit("botwhojokes")
    for submission in subreddit.get_hot(limit=thing_limit):
        op_text = submission.selftext.lower()
        has_joke = any(string in op_text for string in jokeWords)
        comment = submission.comments[0]
        author = comment.author
        have_i_posted = any(string in author for string in botname)
        
        if submission.id not in already_done and has_joke and not have_i_posted:
            submission.add_comment("Reading you clear!")
            already_done.append(submission.id)
    
    
