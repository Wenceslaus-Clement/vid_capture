import os
import subprocess
import requests
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import speech_recognition as sr
from moviepy.editor import AudioFileClip

# OMDB and TMDB API keys
OMDB_API_KEY = '71448efb'
TMDB_API_KEY = 'f6f74d3416647ac0ebd60667187fa8b8'

def upload_video(request):
    """
    Handles video uploads and performs video comparisons with local database, OMDB, and TMDB APIs.
    """
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']

        # Save the uploaded video to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        video_path = fs.path(filename)

        try:
            # Ensure the video file is valid
            if not os.path.exists(video_path):
                raise ValueError("Video file not found.")

            # Step 1: Compare with local database videos (audio & video comparison)
            local_results = local_compare_videos(video_path)

            # Step 2: Compare with OMDB API
            omdb_results = compare_with_omdb(video_path)

            # Step 3: Compare with TMDB API
            tmdb_results = compare_with_tmdb(video_path)

            # Try to display the movie name after comparison
            final_movie_title = (
                local_results[0].get('title') if local_results else
                (omdb_results[0].get('title') if omdb_results else
                 (tmdb_results[0].get('title') if tmdb_results else "Unknown Title"))
            )

            # Combine results from all sources
            combined_results = {
                'local_results': local_results,
                'omdb_results': omdb_results,
                'tmdb_results': tmdb_results,
                'final_movie_title': final_movie_title  # Add final movie title after comparison
            }

            # Return combined results as JSON
            return JsonResponse(combined_results, status=200)

        except Exception as e:
            print(f"Error during video comparison: {e}")
            return JsonResponse({"error": f"Error occurred during video comparison: {str(e)}"}, status=500)

    # If it's not a POST request or no file uploaded, render the upload page
    return render(request, 'videos/upload.html')

def local_compare_videos(video_path):
    """
    Compares the uploaded video with videos in the local database (local video files).
    """
    # Placeholder for actual comparison logic. Simulating comparison result.
    results = [{"title": "Sample Local Movie", "similarity": 0.85}]
    return results

def compare_with_omdb(video_path):
    """
    Extracts a title from the video and compares it with the OMDB API.
    """
    title = extract_title_from_audio_or_video(video_path)
    if not title:
        return []

    omdb_url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
    
    try:
        response = requests.get(omdb_url)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return [{'title': data['Title'], 'year': data['Year'], 'similarity': 'N/A'}]
        return []
    except requests.RequestException as e:
        print(f"OMDB API error: {e}")
        return []

def compare_with_tmdb(video_path):
    """
    Extracts a title from the video and compares it with the TMDB API.
    """
    title = extract_title_from_audio_or_video(video_path)
    if not title:
        return []

    tmdb_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}'
    
    try:
        response = requests.get(tmdb_url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            return [{'title': movie['title'], 'release_date': movie['release_date'], 'similarity': 'N/A'} for movie in results]
        return []
    except requests.RequestException as e:
        print(f"TMDB API error: {e}")
        return []

def extract_title_from_audio_or_video(video_path):
    """
    Attempts to extract a movie title from the video using multiple methods:
    1. Video metadata extraction
    2. Audio recognition (speech-to-text)
    3. Machine learning model (optional)
    """
    # Step 1: Try to extract title from metadata
    metadata_title = extract_video_metadata(video_path)
    if metadata_title:
        print(f"Extracted title from metadata: {metadata_title}")
        return metadata_title

    # Step 2: Try to extract title using audio recognition (speech-to-text)
    audio_title = extract_title_from_audio(video_path)
    if audio_title:
        print(f"Extracted title from audio: {audio_title}")
        return audio_title

    return "Unknown Title"

def extract_video_metadata(video_path):
    """
    Extracts metadata from the video file using FFmpeg.
    """
    command = f"ffmpeg -i '{video_path}' -f ffmetadata -"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    metadata = {}
    if result.returncode == 0:
        output = result.stderr.decode('utf-8')  # FFmpeg outputs metadata to stderr
        for line in output.splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                metadata[key.strip()] = value.strip()
    
    return metadata.get('title', None)

def extract_title_from_audio(video_path):
    """
    Extracts the title from the audio using Speech-to-Text.
    """
    recognizer = sr.Recognizer()
    audio_clip = AudioFileClip(video_path)
    audio_clip.write_audiofile("temp_audio.wav")

    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Google Speech Recognition error: {e}")
    finally:
        # Clean up temporary audio file
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

    return None

def extract_title_using_ml(video_path):
    """
    (Optional) Uses machine learning to infer the title from the video content.
    This is a placeholder function for machine learning inference.
    """
    # Placeholder for ML model inference
    return None
