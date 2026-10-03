import pytube
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse
import os

# --- 1. Core Utility Function ---

def extract_video_id(url: str) -> str:
    """
    Extracts the unique video ID from a YouTube URL.
    Raises a ValueError if the URL is not valid.
    """
    try:
        # 1. Parse the URL
        parsed_url = urllib.parse.urlparse(url)
        
        # 2. Check if it's a standard watch link
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com') and parsed_url.path == '/watch':
            query = urllib.parse.parse_qs(parsed_url.query)
            if 'v' in query:
                return query['v'][0]
        
        # 3. Check for short-form shared links (e.g., youtu.be/ID)
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path.strip('/')
        
        # If neither, it's likely an invalid format
        raise ValueError("Invalid YouTube URL format.")
    
    except Exception as e:
        # Re-raise as ValueError for consistent error handling outside
        raise ValueError(f"Could not parse URL: {e}")

# --- 2. Feature: Video Downloader ---

def download_video(video_id: str, output_path: str = "downloads") -> None:
    """
    Downloads the highest resolution stream of the given YouTube video ID.
    """
    full_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        # Create the YouTube object
        yt = pytube.YouTube(full_url)
        
        # Select the highest resolution stream that contains both audio and video (progressive)
        # Note: For resolutions above 720p, streams are often separated (audio/video).
        stream = yt.streams.get_highest_resolution()

        if not stream:
            # Fallback to the first available stream if no progressive stream is found
            stream = yt.streams.first()
            if not stream:
                 raise Exception("No video streams found.")

        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        print(f"📥 Downloading: {yt.title}...")
        print(f"   Resolution: {stream.resolution}")
        
        # Start download
        file_path = stream.download(output_path=output_path)
        print(f"✅ Download complete! File saved to: {file_path}")

    except pytube.exceptions.VideoUnavailable:
        print(f"❌ Error: Video ID '{video_id}' is unavailable.")
    except Exception as e:
        print(f"❌ An error occurred during download: {e}")

# --- 3. Feature: Transcript/Summary Generator ---

def summarize_transcript(transcript_text: str, sentence_count: int = 5) -> str:
    """
    Performs a simple summarization by taking the first N sentences of the transcript.
    (This function can be upgraded with NLTK or Gensim for true summarization)
    """
    # Simple split on periods/exclamation/question marks
    sentences = []
    # Using a split and replace approach for basic sentence separation
    temp_text = transcript_text.replace('\n', ' ').replace('!', '.').replace('?', '.')
    potential_sentences = temp_text.split('.')
    
    for sentence in potential_sentences:
        clean_sentence = sentence.strip()
        if clean_sentence:
            sentences.append(clean_sentence)

    if not sentences:
        return "Could not find any sentences to summarize."

    # Join the first N sentences for the summary
    summary = ". ".join(sentences[:sentence_count]) + "..."
    return summary


def get_and_summarize(video_id: str) -> None:
    """
    Fetches the transcript and prints a summary.
    """
    try:
        # 1. Get the transcript list
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # 2. Concatenate the text from the list of dictionaries
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        print("\n📝 Transcript successfully fetched.")
        
        # 3. Generate and print the summary
        summary = summarize_transcript(full_transcript)
        
        print("--- SUMMARY (First 5 Sentences) ---")
        print(summary)
        print("-----------------------------------")
        
    except Exception as e:
        # Handles cases where transcript is disabled or non-existent
        print(f" Error fetching transcript for video ID '{video_id}': {e}")
        print("   This usually means the creator disabled subtitles or they are not available.")

# --- 4. Main Execution Logic ---

def main():
    """
    Main function to handle user interaction and control flow.
    """
    print(" YouTube Video Downloader/Summarizer ")
    print("------------------------------------------")

    url = input(" Enter the YouTube video URL: ")
    
    try:
        video_id = extract_video_id(url)
        print(f"Video ID extracted: {video_id}")
    except ValueError as e:
        print(f" Invalid URL: {e}")
        return

    # User choice
    while True:
        choice = input("\nWhat would you like to do? (D)ownload or (S)ummarize? (Type 'D' or 'S'): ").upper()
        
        if choice == 'D':
            download_video(video_id)
            break
        elif choice == 'S':
            get_and_summarize(video_id)
            break
        else:
            print("Invalid choice. Please enter 'D' or 'S'.")

if __name__ == "__main__":
    main()