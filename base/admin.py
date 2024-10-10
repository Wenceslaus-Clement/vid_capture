from django.contrib import admin
from .models import Video
import os

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file')  # Show the title and file in the admin panel
    # search_fields = ('title',)
    def save_model(self, request, obj, form, change):
        # Check if the title field is empty
        if not obj.title and obj.video_file:
            # Set the title as the name of the uploaded file (without extension)
            obj.title = obj.video_file.name.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        super().save_model(request, obj, form, change)

admin.site.register(Video, VideoAdmin)
# from django.contrib import admin
# from .models import Video
# import os

# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'video_file', 'is_temporary', 'created_at')
    
#     def save_model(self, request, obj, form, change):
#         if not obj.title and obj.video_file:
#             # Extract file name (without extension) as title
#             obj.title = os.path.splitext(obj.video_file.name)[0]
#         super().save_model(request, obj, form, change)

# admin.site.register(Video, VideoAdmin)
