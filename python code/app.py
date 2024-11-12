import requests

# Set your API key here
API_KEY = 'ENTER_YOUR_API_KEY'  # Replace with your API key



from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



# YouTube Video ID (this is part of the URL after "v=")
video_id = 'Xj0Jtjg3lHQ'  # Replace with your target video ID

# API URL to get comments
url = f'https://www.googleapis.com/youtube/v3/commentThreads'

# Parameters to send with the request
params = {
    'part': 'snippet',
    'videoId': video_id,
    'key': API_KEY,
    'maxResults': 100  # The maximum number of comments to fetch per request
}

# Function to get comments from the video with pagination support
def get_youtube_comments(max_comments=200):
    comments = []
    while True:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Loop through the response and extract comment text
            for item in data.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
                
                # Stop if we've reached the maximum number of comments
                if len(comments) >= max_comments:
                    return comments
            
            # Check if there's a next page (pagination)
            next_page_token = data.get('nextPageToken')
            if next_page_token:
                # If there's a next page, set the pageToken for the next request
                params['pageToken'] = next_page_token
            else:
                break  # No more pages, exit the loop
        else:
            print(f"Error: {response.status_code}")
            break
    
    return comments

# Fetch comments from multiple pages, limited to a maximum of 1000 comments
comments = get_youtube_comments(max_comments=1000)

# Initialize the VADER SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Variables to count sentiment categories
positive = 0
negative = 0
neutral = 0

# Perform sentiment analysis on each comment
for comment in comments:
    # Get sentiment scores
    sentiment = analyzer.polarity_scores(comment)

    # Determine overall sentiment
    if sentiment['compound'] >= 0.05:
        positive += 1
    elif sentiment['compound'] <= -0.05:
        negative += 1
    else:
        neutral += 1

# Print the results
print("Positive: ", positive)
print("Negative: ", negative)
print("Neutral: ", neutral)
