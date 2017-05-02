import praw
import time
from datetime import datetime
import smtplib

r = praw.Reddit('WPBot', user_agent = 'Writing_Prompt Aggregator');
FMT = '%H:%M:%S'
iteration = 0;
   
def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("successfully sent the mail");
    except:
        print("failed to send mail");

def run_bot():
    subreddit = r.subreddit("writingprompts");
    
    trending = open("trendingPrompts.txt", "w+");
        
    for submission in subreddit.hot(limit=50):
        curTime = datetime.utcnow();
        curTime_ts = time.mktime(curTime.timetuple());
        postTime = datetime.utcfromtimestamp(submission.created_utc);
        postTime_ts = time.mktime(postTime.timetuple());
        age = (int(curTime_ts - postTime_ts) / 60);
        if  age < 120 and submission.score > 25:
            if not submission.id in open("trendingPrompts.txt").read():
                trending.write(submission.id + "\n");
                msg = "{" + str(submission.score) + "} " + submission.title;
                msg += "\nAge: " + str(time.strftime("%H:%M:%S", time.gmtime(age)));
                print(msg);
                send_email('redditwpbot', 'beepboop!2', 'wang3806@umn.edu', 'WP Alert', msg); 
                
run_bot();
