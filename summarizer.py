import os
import re
import time
import shutil
import requests
import nltk
import pickle
import yt_dlp
from textblob import TextBlob
from langdetect import detect
from newspaper import Article

from dotenv import load_dotenv
load_dotenv()


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

with open('output/punkt_hindi_tokenizer.pkl', 'rb') as f:
    hindi_tokenizer = pickle.load(f)
with open('output/punkt_news_tokenizer.pkl', 'rb') as f:
    english_tokenizer = pickle.load(f)

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
def summarize_article(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        raise RuntimeError(f"Error processing article: {e}")

    lang = detect(article.text)
    tokenizer = hindi_tokenizer if lang == 'hi' else english_tokenizer
    lang_name = "Hindi" if lang == 'hi' else "English"

    try:
        sentences = tokenizer.tokenize(article.text)
    except Exception:
        sentences = []

    sentiment = TextBlob(article.text).sentiment

    return {
        "title": article.title,
        "authors": ', '.join(article.authors),
        "date": str(article.publish_date) if article.publish_date else "",
        "language": lang_name,
        "summary": article.summary,
        "polarity": sentiment.polarity,
        "sentiment": "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral",
        "sentences": sentences
    }

def download_audio(youtube_url, output_path="audio"):
    import shutil
    print("Checking for ffmpeg...")
    print("ffmpeg found at:", shutil.which("ffmpeg"))

    try:
        print("Downloading audio from YouTube...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path + '.%(ext)s',
            'quiet': False,
            'cookies': 'static/cookies.txt',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        final_path = output_path + ".mp3"
        print(f"Download complete. Checking if file exists: {final_path}")
        if not os.path.exists(final_path):
            raise FileNotFoundError(f"yt-dlp did not produce the file: {final_path}")
        return final_path
    except Exception as e:
        print("Download failed:", e)
        raise


def upload_to_assemblyai(filename):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    with open(filename, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=f)
    response.raise_for_status()
    return response.json()['upload_url']

def request_transcription(audio_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    json = {
        "audio_url": audio_url,
        "auto_chapters": True
    }
    response = requests.post(endpoint, json=json, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def poll_transcription(transcript_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    while True:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'completed':
            return data
        elif data['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {data['error']}")
        time.sleep(5)

def summarize_youtube_video(youtube_url):
    audio_path = download_audio(youtube_url)
    try:
        upload_url = upload_to_assemblyai(audio_path)
        transcript_id = request_transcription(upload_url)
        result = poll_transcription(transcript_id)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    transcript = result.get("text", "")
    summary = result.get("chapters", [])
    summarized_text = " ".join([c["summary"] for c in summary]) if summary else transcript

    if not transcript.strip():
        raise RuntimeError("Transcription failed or was empty.")

    lang = detect(transcript)
    lang_name = "Hindi" if lang == 'hi' else "English"
    sentiment = TextBlob(transcript).sentiment
    sentences = nltk.sent_tokenize(transcript)

    return {
        "title": "YouTube Video",
        "authors": "",
        "date": "",
        "language": lang_name,
        "summary": summarized_text.strip(),
        "polarity": sentiment.polarity,
        "sentiment": "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral",
        "sentences": sentences
    }
