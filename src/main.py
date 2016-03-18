import praw
import OAuth2Util
import pprint
import random

user_agent = ("JokerPractice v0.1 by DukeCarge")

r = praw.Reddit(user_agent = user_agent)
o = OAuth2Util.OAuth2Util(r, server_mode=True)
r.login("BotWhoJokes", "RobotHumor42????", disable_warning=True)
o.refresh(force = True)
thing_limit = 10
botname = ["BotWhoJokes"]
CallWords = ["joke"]
fgj = open("goodjokes.txt", "w+")
fbj = open("badjokes.txt", "w+")
GoodJoke = [line.rstrip('\n') for line in fgj]
fgj.close()
BadJoke = [line.rstrip('\n') for line in fbj]
fbj.close()
fo = open("nouns.txt")
JokeWords = [line.rstrip('\n') for line in fo]
phrases = [" is as likely as ", " would totally destroy ", " can't really stand up to ", " is building a wall to keep out "]
fo.close()
JokeRand1 = 0
JokeRand2 = 0
JokeSent = 0
GoodRand = 0
JCount = 0
mycomment = 0

already_done = []
have_i_posted = False
print_outdone = False

while True:
    
    o.refresh()
    subreddit = r.get_subreddit("botwhojokes")
    for submission in subreddit.get_hot(limit=thing_limit):
        random.seed() 
        JokeRand1 = random.randint(0,len(JokeWords)-1)
        JokeRand2 = random.randint(0,len(JokeWords)-1)
        JokeSent = random.randint(0,len(phrases)-1)
        while JokeRand1 == JokeRand2:
            JokeRand2 = random.randint(0,len(JokeWords)-1)
        
        op_text = submission.selftext.lower()
        op_title = submission.title.lower()
        has_joke_text = any(string in op_text for string in CallWords)
        has_joke_title = any(string in op_title for string in CallWords)
        if submission.comments:
            for i, elem in enumerate(submission.comments):
                comment = submission.comments[i]
                author = str(comment.author)
                have_i_posted = any(string in author for string in botname)
                if have_i_posted:
                    mycomment = i
                if have_i_posted and submission.id not in already_done:
                    already_done.append(submission.id)
                    print_outdone = False
        if submission.id not in already_done and has_joke_text:
            
            telljoke = JokeWords[JokeRand1] + phrases[JokeSent] + JokeWords[JokeRand2]
            tellbad = any(string in telljoke for string in BadJoke)
            if tellbad:
                continue
            if JCount >= 50:
                GoodRand = random.randint(0,len(GoodJoke)-1)
                telljoke = GoodJoke[GoodRand]
            submission.add_comment(telljoke + "\n \n Was the joke I told good? Upvote me. Bad? Downvote me. More info at https://github.com/AlexFroio/BotWhoJokes")
            submission.upvote()
            already_done.append(submission.id)
            JCount = JCount + 1
        if have_i_posted:
            comment = submission.comments[mycomment]
            if comment.ups >= 10:
                GoodJoke.append(comment.selftext.strip("\n \n Was the joke I told good? Upvote me. Bad? Downvote me. More info at https://github.com/AlexFroio/BotWhoJokes") + "\n")
            if comment.ups == 0:
                BadJoke.append(comment.selftext.strip("\n \n Was the joke I told good? Upvote me. Bad? Downvote me. More info at https://github.com/AlexFroio/BotWhoJokes") + "\n")
                if comment.selftext in GoodJoke:
                    GoodJoke.remove(comment.selftext + "\n")
            fgj = open("goodjokes.txt", "w")
            for line in GoodJoke:
                fgj.write(line)
            fgj.close()
            fbj = open("badjokes.txt", "w")
            for line in BadJoke:
                fbj.write(line)
            fbj.close()       
    
        have_i_posted = False
    if not print_outdone:
        pprint.pprint(already_done)
        print_outdone = True