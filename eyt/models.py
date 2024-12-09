from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

#For the video features
from django.conf import settings


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('coach', 'Coach'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    usatt_number = models.CharField(max_length=20)
    rating = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    birth_date = models.DateField()
    specialization = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(max_length=100)
    about = models.CharField(max_length=1000)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)


class Video(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Use the CustomUser model
User = get_user_model()

# PlayerProfile Model
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Default value
    specialization = models.CharField(max_length=100, default='Unknown')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Player"

# CoachProfile Model
class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default='General')
    experience_years = models.IntegerField(default=0)  # Default value
    certifications = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True, default='Unknown')
    rating = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Coach"

# VideoReview Model
class VideoReview(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review for {self.video.title} by {self.coach.user.username}"

# VirtualCoachingSession Model
class VirtualCoachingSession(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')])
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session between {self.player.user.username} and {self.coach.user.username}"

# Payment Model
class Payment(models.Model):
    session = models.OneToOneField(VirtualCoachingSession, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending')])

    def __str__(self):
        return f"Payment for session {self.session.id} - {self.status}"

# CoachReview Model
class CoachReview(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()

    def __str__(self):
        return f"Review by {self.player.user.username} for {self.coach.user.username}"
    
# Notification Model
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} from {self.sender.username}"

    



