from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from . models import CustomUser
from .models import Video
from .models import PlayerProfile 
from .models import CoachProfile
from .models import VideoReview

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('coach', 'Coach'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    
    usatt_number = forms.CharField(max_length=20, required=True, label='USATT Number')
    rating = forms.IntegerField(required=True, label='Table Tennis Rating')
    city = forms.CharField(max_length=100, required=True, label='City')
    state = forms.CharField(max_length=100, required=True, label='State')
    birth_date = forms.DateField(required=True, label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    specialization = forms.CharField(max_length=100, required=True, label='Specialization')
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Role')
    email = forms.EmailField(max_length=100, required=True, label='Email')
    about = forms.CharField(max_length=1000, required=True, label='About Me')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label='Gender')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'usatt_number', 'rating', 'city', 'state', 'birth_date', 'specialization', 'role', 'email', 'about', 'gender')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['usatt_number', 'rating', 'city', 'state', 'birth_date', 'specialization', 'role', 'email', 'about', 'gender']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            # Only allow .mp4 files
            if not video.name.endswith('.mp4'):
                raise forms.ValidationError('Only .mp4 video files are allowed.')
        return video       

# Form for Player Profile
class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ['rating', 'specialization', 'profile_picture']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Form for Coach Profile
class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = CoachProfile
        fields = ['specialization', 'experience_years', 'certifications', 'availability', 'rating', 'profile_picture']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'certifications': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Form for video reviews from coaches
class VideoReviewForm(forms.ModelForm):
    class Meta:
        model = VideoReview
        fields = ['review_text', 'rating', 'reply']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'reply': forms.Textarea(attrs={'rows': 2}),
        }


# Form for reply from players to coach's reviews
class PlayerReplyForm(forms.ModelForm):
    class Meta:
        model = VideoReview
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your reply here...'}),
        }







