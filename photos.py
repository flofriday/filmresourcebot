import random

import praw
import requests

reddit = None
unsplash_access_key = None


def __init__(config):
    global reddit
    reddit = praw.Reddit(
        client_id=config["reddit_client_id"],
        client_secret=config["reddit_client_secret"],
        password=config["reddit_password"],
        user_agent="Photobot",
        username=config["reddit_username"],
    )

    global unsplash_access_key
    unsplash_access_key = config["usplash_access_key"]


class Photo:
    """A simple class for storring, URLs of photos and where they came from"""

    def __init__(self, url, name, source_url, creator="", creator_url=""):
        self.url = url
        self.name = name
        self.source_url = source_url
        self.creator = creator
        self.creator_url = creator_url

    def __repr__(self):
        return "<Photo url:%s name:%s source_url:%s>" % (
            self.url,
            self.name,
            self.source_url,
        )


def get_subreddits_photos(number=3):
    # All interesting subreddits
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

    # Combine all subreddits to one string
    subreddits_combined = "+".join(subreddits)
    posts = reddit.subreddit(subreddits_combined).hot(limit=64)

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
        photo = Photo(
            post.url,
            post.subreddit.display_name.capitalize(),
            "https://reddit.com" + post.permalink,
            post.author.name.replace("\\", "").lower(),
            "https://reddit.com/u/" + post.author.name + "/posts",
        )
        photos.append(photo)

    # Shorten the list if it is longer than expected
    if len(photos) > number:
        random.shuffle(photos)
        photos = photos[:number]

    return photos


def get_random_unsplash_photos(number=3):
    response = requests.get(
        "https://api.unsplash.com/photos",
        params={
            "client_id": unsplash_access_key,
            "page": random.randint(1, 15),
            "per_page": number,
        },
    )

    data = response.json()

    # Convert the data to photos
    photos = []
    for result in data:
        photo = Photo(
            url=result["urls"]["regular"],
            name=result["description"],
            source_url=result["links"]["html"],
            creator=result["user"]["name"],
            creator_url=result["user"]["links"]["html"],
        )

        # Set to empty text if there is no description
        if photo.name is None:
            photo.name = "Photo"

        if len(photo.name) > 25:
            photo.name = photo.name[:22] + "..."

        photos.append(photo)

    return photos


def get_inspiration_photos(number=6):
    print("Load inspiration images ...")

    # Calculate how many images of each kind
    reddit_number = int(number / 2)
    unsplash_number = number - reddit_number

    # Load the images
    photos = get_subreddits_photos(reddit_number)
    print(f"Got {len(photos)} reddit images")
    photos += get_random_unsplash_photos(unsplash_number)
    print(f"Got {len(photos)} unsplash images")

    # Shuffle the images and return them
    random.shuffle(photos)
    return photos


def get_search_photos(query):
    response = requests.get(
        "https://api.unsplash.com/search/photos",
        params={
            "query": query,
            "client_id": unsplash_access_key,
            "per_page": "5",
        },
    )

    data = response.json()
    photos = []
    for result in data["results"]:
        photo = Photo(
            url=result["urls"]["regular"],
            name=result["description"],
            source_url=result["links"]["html"],
            creator=result["user"]["name"],
            creator_url=result["user"]["links"]["html"],
        )

        # Set to empty text if there is no description
        if photo.name is None:
            photo.name = "Photo"

        if len(photo.name) > 25:
            photo.name = photo.name[:22] + "..."

        photos.append(photo)

    return photos
