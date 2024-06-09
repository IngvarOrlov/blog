from django.db import models
from PIL import Image

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.urls.base import reverse


class User(AbstractUser):
    email = models.EmailField("email address", blank=True, unique=True)
    bio = models.TextField("biography", blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name='Профиль пользователя'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 120 or img.width > 120:
            new_img = (120, 120)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def get_absolute_url(self):
        return reverse("profile_view", kwargs={'pk': self.pk})
