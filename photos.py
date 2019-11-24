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

    def __init__(self, url, name, source_url):
        self.name = name
        self.url = url
        self.source_url = source_url

    def __repr__(self):
        return "<Photo url:%s name:%s source_url:%s>" % (self.url, self.name,
        self.source_url)

def get_subreddits_photos(subreddits):
    # Combine all subreddits to one string 
    subreddits_combined = "+".join(subreddits)
    posts = reddit.subreddit(subreddits_combined).hot(limit=128)

    # Filter the posts
    photos = []
    for post in posts:
        # Ignore if they are:
        # - text only
        # - under 10 upvotes
        # - not ok for under 18
        # - sticked to a subreddit
        if post.is_self or post.score < 10 or post.over_18 or post.stickied:
            continue

        # Add the photo to the list
        photo = Photo(post.url, post.subreddit.display_name, "https://reddit.com" + post.permalink)
        photos.append(photo)

    return photos

def get_inspiration_photos(number=5):
    subreddits = [
        "analog",
        "architecture",
        "earthporn",
        "itookapicture",
        "natureporn",
        "photographs",
        "portraisphotos",
        "portraits",
        "portraitsporn",
    ]
    
    print("Load inspiration images ...")
    photos = get_subreddits_photos(subreddits)
    print(f"Got {len(photos)} images")

    # If there are more images found than requested, shorten that list
    if (len(photos) > number):
        random.shuffle(photos)
        photos = photos[0:number]

    return photos

