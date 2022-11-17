from django.db import models
from django.contrib.auth import get_user_model
from django.core.files import File

from io import BytesIO
from PIL import Image

User = get_user_model()

class Profile(models.Model):

    id_user = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_img_raw = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    profile_img_thumbnail = models.ImageField(upload_to='profile_images', default='blank_profile_picture_thumbnail.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    def process_thumbnail(self):
        # Process image to make thumbnail
        if not self.profile_img_thumbnail or self.profile_img_thumbnail.name == 'profile_images/blank_profile_picture_thumbnail.png':
            self.profile_img_thumbnail = self.make_thumbnail(self.profile_img_raw)
            self.save()
            

        return 'http://127.0.0.1:8000' + self.profile_img_thumbnail.url

    def make_thumbnail(self, image, size=(176,176)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=100)

        names = image.name.split(".")
        name = names[0] + "_thumbnail." + names[1]

        thumbnail = File(thumb_io, name=name)
        return thumbnail

    
    