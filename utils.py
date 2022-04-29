import praw
import os

def get_auth_instance():
    # Establish authorized Reddit instance
    reddit = praw.Reddit(
        client_id = os.environ.get("REDIT_CLIENT_ID", None),
        client_secret = os.environ.get("REDDIT_SECRET_TOKEN", None),
        user_agent = os.environ.get("REDDIT_USER_AGENT", None),
        username = os.environ.get("REDDIT_USERNAME", None),
        password = os.environ.get("REDDIT_PASSWORD", None)    
    )
    return reddit

def printy(thing):
    print('\ndir():\n' , dir(thing))
    print('\n')
    print('-'*40)
    print('\nvars():\n', vars(thing))
    print('\n')

# Migrate timer to utils?
    # t1_start = process_time()
    # # Timer and teardown
    # t1_stop = process_time()
    # # print(f'\nDone!\nTotal time (seconds): {t1_stop-t1_start}\nPress any key to close the program.')
    # # input()
    # # sys.exit('Exit.')