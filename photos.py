import random
import praw

reddit = None

def __init__(config):
    global reddit
    reddit = praw.Reddit(client_id=config["reddit_client_id"], 
    client_secret=config["reddit_client_secret"],
    password=config["reddit_password"],
    user_agent='Photobot',
    username=config["reddit_username"])

class Photo:
    """A simple class for storring, URLs of photos and where they came from"""

    def __init__(self, url, source_url):
        self.url = url
        self.source_url = source_url

    def __repr__(self):
        return "<Photo url:%s source_url:%s>" % (self.url, self.source_url)

def get_subreddits_photos(subreddits):
    # Combine all subreddits to one string 
    subreddits_combined = "+".join(subreddits)
    posts = reddit.subreddit(subreddits_combined).hot(limit=128)

    # Filter the posts
    photos = []
    for post in posts:
        # Ignore NSFW posts
        if post.over_18:
            continue
        
        # Ignore sticked posts
        if post.stickied: 
            continue

        # Ignore text only posts
        if post.is_self:
            continue

        photo = Photo(post.url, "https://reddit.com" + post.permalink)
        photos.append(photo)

    return photos

def get_inspiration_photos(number=5):
    subreddits = [
        "earthporn",
        "portraitsporn",
        "portraisphotos",
        "portraits",
        "architecture",
        "photographs",
        "analog",
        "itookapicture",
        "natureporn",
    ]
    
    print("Load inspiration images ...")
    photos = get_subreddits_photos(subreddits)

    # If there are more images found than requested, shorten that list
    if (len(photos) > number):
        random.shuffle(photos)
        photos = photos[0:number]

    return photos

