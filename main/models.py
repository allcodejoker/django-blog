from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    blog_image = models.ImageField(upload_to=('blog_images/'))
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog_post.title} - {self.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    image = models.ImageField(upload_to=('profile_p/'), default='profile_p/default.png')

    def __str__(self):
        return self.user.username
    
    def total_followers(self):
        return self.followers.count()
    
    def save(self, *args, **kwargs):
        if not self.bio and self.user:
            self.bio = f"I am {self.user.username}"
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # If user JUST registered, create his Profile
        Profile.objects.create(user=instance)
    else:
        # If User is just updating, update his Profile also
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # If Profile does not exist, create him (not really important)
            Profile.objects.create(user=instance)
