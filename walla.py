import requests
from bs4 import BeautifulSoup
import re
import youtube_dl
# Function to extract media_id from the iframe in the webpage HTML
def extract_media_id(original_url):
    # Make a GET request to fetch the raw HTML content
    response = requests.get(original_url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the iframe in the HTML that contains the media_id
        iframe = soup.find('iframe', class_='article-video-iframe')
        
        if iframe:
            iframe_src = iframe.get('src')
            print(f"Found iframe src: {iframe_src}")
            
            # Extract the media_id from the iframe URL using regex
            media_id_match = re.search(r'media=(\d+)', iframe_src)
            
            if media_id_match:
                return media_id_match.group(1)  # Return the media_id
    return None

# Function to fetch JSON and extract the video URL
def fetch_video_url(media_id):
    player = ""
    base_url = f"https://dal.walla.co.il/media/{media_id}?origin=player.{player}"#TODO add source dynamically
    response = requests.get(base_url)
    
    if response.status_code == 200:
        json_data = response.json()
        
        # Extract the stream URL from the JSON structure
        try:
            stream_url = json_data['data']['video']['stream_urls'][0]['stream_url']
            return stream_url
        except (KeyError, IndexError) as e:
            print(f"Error extracting stream_url: {e}")
            return None
    return None

# Function to download the video using ffmpeg
def download_video(video_url, output_file):
    ydl_opts = {
    'outtmpl': 'downloaded_video.mp4',  # Set the output filename
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Video downloaded as {output_file}")

# Main function to automate extraction and downloading
def automate_video_download(original_url, output_file):
    # Step 1: Extract the media_id from the page
    media_id = extract_media_id(original_url)
    
    if media_id:
        print(f"Found media ID: {media_id}")
        # Step 2: Fetch the video URL from the media_id
        video_url = fetch_video_url(media_id)
        
        if video_url:
            print(f"Found video URL: {video_url}")
            # Step 3: Download the video using ffmpeg
            download_video(video_url, output_file)
        else:
            print("Failed to extract video URL.")
    else:
        print("Failed to extract media ID.")

# Example usage
if __name__ == "__main__":
    original_url = ""  # Original webpage URL
    output_file = "downloaded_video.mp4"  # Output filename
    automate_video_download(original_url, output_file)
