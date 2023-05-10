import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



api_key = "AIzaSyBObxVtZoOSwyihqmBAb5rTVoeznTcWmBE"





def extract_video_id(url):
    video_id = None
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^\?&"\'#<>]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break

    return video_id


def get_video_details(url):
    video_id = extract_video_id(url)
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]
        else:
            print("No video found with the provided video_id.")
            return None

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None


def get_comments(url, max_results=10):
    comments = []
    video_id = extract_video_id(url)
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,  # Maximum results to return
            textFormat="plainText",
            order="relevance"
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            likes = comment["snippet"]["likeCount"]
            one_comment = {
                "author": comment["snippet"]["authorDisplayName"],
                "text": comment["snippet"]["textDisplay"],
                "likes": comment["snippet"]["likeCount"],
            }
            comments.append(one_comment)
            print(f"Comment by {author}: {text} with {likes} likes")
        
        # Sort comments by number of likes, in descending order
        comments.sort(key=lambda c: c["likes"], reverse=True)
        return comments

    except HttpError as e:
        print(f"An error occurred: {e}")

def process_url(url):
    print("hello there")