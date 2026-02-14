from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
            User, 
            on_delete=models.CASCADE,
            related_name = "posts"
            )
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete = models.CASCADE,
        )
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to = 'profile_pics/', blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"

# signals go here
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
    post = models.ForeignKey(
            Post, 
            on_delete=models.CASCADE,
            )
    author = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            )
    content = models.TextField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
