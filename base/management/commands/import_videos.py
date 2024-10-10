# yourapp/management/commands/upload_videos.py

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from base.models import Video  # Replace with your actual model

class Command(BaseCommand):
    help = 'Upload videos from a directory to the database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing the videos')

    def handle(self, *args, **options):
        directory = options['directory']
        
        for filename in os.listdir(directory):
            if filename.endswith(('.mp4', '.avi', '.mov')):  # Add or remove video extensions as needed
                file_path = os.path.join(directory, filename)
                with open(file_path, 'rb') as file:
                    video = Video(
                        title=os.path.splitext(filename)[0],  # Use filename without extension as title
                        video_file=File(file, name=filename)
                    )
                    video.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {filename}'))

        self.stdout.write(self.style.SUCCESS('Video upload completed'))