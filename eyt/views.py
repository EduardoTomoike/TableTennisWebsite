from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import logout
from .utils import send_email_via_api
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import ProfileForm
from .forms import VideoUploadForm
from .models import Video
from .forms import PlayerProfileForm
from .forms import CoachProfileForm
from .models import PlayerProfile
from .models import CoachProfile
from django.contrib import messages
from django.db.models import Q
from .models import VideoReview
from .forms import VideoReviewForm
from .forms import PlayerReplyForm
from .models import Notification

########################################################################################################
@login_required
def notifications_view(request):
    if request.user.role == 'coach':
        notifications = request.user.notifications.filter().order_by('-timestamp')
    else:
        notifications = []
    return render(request, 'eyt/notifications.html', {'notifications': notifications})


########################################################################################################
@login_required
def video_call_view(request, coach_id):
    from .models import CustomUser
    coach = CustomUser.objects.get(id=coach_id)
    player = request.user
    room_name = f"player_{player.id}_coach_{coach.id}"

    # Create an in-app notification for the coach
    Notification.objects.create(
        recipient=coach,
        sender=player,
        message=f"{player.username} has initiated a video call with you.",
        link=f"https://meet.jit.si/{room_name}",
    )

    
    return redirect(f"https://meet.jit.si/{room_name}")


########################################################################################################
@login_required
def send_email_view(request, recipient_id):
    recipient = CustomUser.objects.get(id=recipient_id)  # Fetch the recipient by ID

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender_email = request.user.email  

        
        status_code, response_data = send_email_via_api(subject, message, recipient.email, sender_email)

        if status_code == 201:  
            return redirect('base')  
        else:
            return render(request, 'eyt/send_email_form.html', {
                'error': response_data.get('message', 'An error occurred'),
                'recipient': recipient,
            })

    return render(request, 'eyt/send_email_form.html', {'recipient': recipient})


########################################################################################################
@login_required
def add_video_review(request, video_id):
   
    if request.user.role != 'coach':
        return HttpResponseForbidden("Only coaches can leave video reviews.")

    video = get_object_or_404(Video, id=video_id)

    
    existing_review = VideoReview.objects.filter(video=video, coach=request.user.coachprofile).first()

    if request.method == 'POST':
        form = VideoReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.video = video
            review.coach = request.user.coachprofile
            review.save()
            return redirect('player_videos_for_review', player_id=video.player.playerprofile.id)  # Redirect back to video list
    else:
        form = VideoReviewForm(instance=existing_review)

    return render(request, 'eyt/add_video_review.html', {'video': video, 'form': form})

########################################################################################################
@login_required
def player_videos_for_review(request, player_id):
    
    if request.user.role != 'coach':
        return HttpResponseForbidden("Only coaches can review player videos.")
    
    
    player = get_object_or_404(PlayerProfile, id=player_id)
    videos = Video.objects.filter(player=player.user)

    return render(request, 'eyt/player_videos_for_review.html', {'player': player, 'videos': videos})

########################################################################################################
@login_required
def edit_coach_profile(request):
    if request.user.role != 'coach':
        return HttpResponseForbidden("Only coaches can access this page.")
    
    try:
        coach_profile = request.user.coachprofile #
    except CoachProfile.DoesNotExist:
        coach_profile = CoachProfile(user=request.user) 
        

    if request.method == 'POST':
        form = CoachProfileForm(request.POST, request.FILES, instance=coach_profile) 
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('coach_profile')  
    else:
        form = CoachProfileForm(instance=coach_profile)

    return render(request, 'eyt/edit_coach_profile.html', {'form': form})

########################################################################################################
@login_required
def upload_video(request):
    if not hasattr(request.user, 'playerprofile'):
        return HttpResponseForbidden("Only players can upload videos.")
    if request.user.role != 'player':
        return redirect('player_profile')  
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.player = request.user  
            video.save()
            return redirect('video_list')  
    else:
        form = VideoUploadForm()
    return render(request, 'eyt/upload_video.html', {'form': form})

########################################################################################################
@login_required
def edit_player_profile(request):
    if request.user.role != 'player':
        return HttpResponseForbidden("Only players can access this page.")
    
    try:
        player_profile = request.user.playerprofile
    except PlayerProfile.DoesNotExist:
        player_profile = PlayerProfile(user=request.user)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=player_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('player_profile')  
    else:
        form = PlayerProfileForm(instance=player_profile)

    return render(request, 'eyt/edit_player_profile.html', {'form': form})

########################################################################################################
@login_required
def base(request):
    search_query = request.GET.get('q')  

    if request.user.role == 'player':
        if search_query:
            available_coaches = CoachProfile.objects.filter(
                Q(user__username__icontains=search_query) |
                Q(specialization__icontains=search_query) |
                Q(certifications__icontains=search_query) |
                Q(user__state__icontains=search_query)    |
                Q(user__city__icontains=search_query)     |
                Q(availability__icontains=search_query)
            ).order_by('user__state', 'user__city')  
        else:
            available_coaches = CoachProfile.objects.all().order_by('user__state', 'user__city')
        context = {'available_coaches': available_coaches, 'search_query': search_query}

    elif request.user.role == 'coach':
        if search_query:
            active_players = PlayerProfile.objects.filter(
                Q(user__username__icontains=search_query) |
                Q(specialization__icontains=search_query) |
                Q(rating__icontains=search_query)  |
                Q(user__state__icontains=search_query) |
                Q(user__city__icontains=search_query)
            ).order_by('user__state', 'user__city')  
        else:
            active_players = PlayerProfile.objects.all().order_by('user__state', 'user__city')
        context = {'active_players': active_players, 'search_query': search_query}

    else:
        context = {}

    return render(request, 'eyt/base.html', context)


########################################################################################################
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.role == 'coach':
                return redirect('coach_profile')
            else:
                return redirect('player_profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

########################################################################################################
def landing_page(request):
    coaches = CoachProfile.objects.all().order_by('user__state', 'user__city')
    return render(request, 'eyt/landing_page.html', {'coaches': coaches})

########################################################################################################

#check if this one is necessary
def home(request):
    players = PlayerProfile.objects.all().order_by('user__state', 'user__city')
    coaches = CoachProfile.objects.all().order_by('user__state', 'user__city')
    context = {
        'players': players,
        'coaches': coaches
    }
    return render(request, 'eyt/profiles_overview.html', context)
    
########################################################################################################    
#def register(request):
#    if request.method == 'POST':
#        form = CustomUserCreationForm(request.POST)
#        if form.is_valid():
#            user = form.save(commit=False)
#            user.usatt_number = form.cleaned_data.get('usatt_number')
#            user.rating = form.cleaned_data.get('rating')
#            user.city = form.cleaned_data.get('city')
#            user.state = form.cleaned_data.get('state')
#            user.birth_date = form.cleaned_data.get('birth_date')
#            user.specialization = form.cleaned_data.get('specialization')
#            user.role = form.cleaned_data.get('role')
#            user.email = form.cleaned_data.get('email')
#            user.about = form.cleaned_data.get('about')
#            user.save()
#            if user.role == 'player':
#                PlayerProfile.objects.create(user=user)
#            elif user.role == 'coach':
#                CoachProfile.objects.create(user=user)
#
#            login(request, user)
#            return redirect('base')  # Redirect to the new home page after login
#    else:
#        form = CustomUserCreationForm()
#    return render(request, 'eyt/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Save user instance
                user = form.save(commit=False)
                user.usatt_number = form.cleaned_data.get('usatt_number')
                user.rating = form.cleaned_data.get('rating')
                user.city = form.cleaned_data.get('city')
                user.state = form.cleaned_data.get('state')
                user.birth_date = form.cleaned_data.get('birth_date')
                user.specialization = form.cleaned_data.get('specialization')
                user.role = form.cleaned_data.get('role')
                user.email = form.cleaned_data.get('email')
                user.about = form.cleaned_data.get('about')
                user.save()

                # Create profile based on role, only if it doesn't already exist
                if user.role == 'player':
                    PlayerProfile.objects.get_or_create(user=user)  # Prevent duplicates
                elif user.role == 'coach':
                    CoachProfile.objects.get_or_create(user=user)  

                login(request, user)  
                return redirect('base')  
            except IntegrityError as e:
                # Handle duplicate entry errors or other integrity issues
                return render(request, 'eyt/register.html', {
                    'form': form,
                    'error': 'An account with this user ID already exists.',
                })
    else:
        form = CustomUserCreationForm()
    return render(request, 'eyt/register.html', {'form': form})
    
########################################################################################################
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')  # Redirect to the base page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'eyt/login.html')

########################################################################################################
# View for creating or updating a player profile
@login_required
def player_profile_view(request):
    if not request.user.is_authenticated or request.user.role != 'player':
        return HttpResponseForbidden("You do not have access to this page.")
    try:
        player_profile = request.user.playerprofile
    except PlayerProfile.DoesNotExist:
        player_profile = PlayerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=player_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player profile updated successfully!')
            return redirect('player_profile')
    else:
        form = PlayerProfileForm(instance=player_profile)
    return render(request, 'eyt/player_profile.html', {'player': request.user.playerprofile})

########################################################################################################
# View for creating or updating a coach profile
def coach_profile_view(request):
    if not request.user.is_authenticated or request.user.role != 'coach':
        return HttpResponseForbidden("You do not have access to this page.")
    try:
        coach_profile = request.user.coachprofile
    except CoachProfile.DoesNotExist:
        coach_profile = CoachProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = CoachProfileForm(request.POST, request.FILES, instance=coach_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coach profile updated successfully!')
            return redirect('coach_profile')
    else:
        form = CoachProfileForm(instance=coach_profile)
    return render(request, 'eyt/coach_profile.html', {'coach': request.user.coachprofile})


########################################################################################################
@login_required
def my_uploaded_videos(request):
    # Ensure only players can access this view
    if request.user.role != 'player':
        return HttpResponseForbidden("Only players can access this page.")
    
    # Get the videos uploaded by the logged-in player, including their reviews
    videos = Video.objects.filter(player=request.user).prefetch_related('videoreview_set')

    # Handle reply form submission
    if request.method == 'POST':
        # Get the review being replied to
        review_id = request.POST.get('review_id')
        review = get_object_or_404(VideoReview, id=review_id, video__player=request.user)
        
        # Bind the form to the POST data and the specific review instance
        reply_form = PlayerReplyForm(request.POST, instance=review)
        if reply_form.is_valid():
            reply_form.save()  # Save the player's reply to the review
            return redirect('my_uploaded_videos')  # Reload the page to show the new reply

    # Create a reply form for each review to be rendered in the template
    reply_forms = {review.id: PlayerReplyForm(instance=review) for video in videos for review in video.videoreview_set.all()}
    
    return render(request, 'eyt/my_uploaded_videos.html', {'videos': videos, 'reply_forms': reply_forms})

########################################################################################################
def video_list(request):
    videos = Video.objects.filter(player=request.user)
    return render(request, 'video_list.html', {'videos': videos})

########################################################################################################
def player_profile(request):
    return render(request, 'player_profile.html')

########################################################################################################
def coach_profile(request):
    return render(request, 'coach_profile.html')

########################################################################################################
def manage_videos(request):
    return render(request, 'manage_videos.html')

########################################################################################################
def playback_video(request, video_id):
    return render(request, 'playback_video.html')

########################################################################################################
def search_coaches(request):
    return render(request, 'search_coaches.html')

########################################################################################################
def select_coach(request):
    return render(request, 'select_coach.html')

########################################################################################################
def video_call(request):
    return render(request, 'video_call.html')

########################################################################################################
def payment(request):
    return render(request, 'payment.html')

########################################################################################################
# View to display all player profiles
@login_required
def all_player_profiles(request):
    players = PlayerProfile.objects.all()
    return render(request, 'eyt/player_profiles_list.html', {'players': players})

########################################################################################################
# View to display all coach profiles
@login_required
def all_coach_profiles(request):
    coaches = CoachProfile.objects.all()
    return render(request, 'eyt/coach_profiles_list.html', {'coaches': coaches})

########################################################################################################
def player_profile_detail(request, user_id):
    player_profile = get_object_or_404(PlayerProfile, user__id=user_id)
    return render(request, 'eyt/player_profile_detail.html', {'player_profile': player_profile})

########################################################################################################
def coach_profile_detail(request, user_id):
    coach_profile = get_object_or_404(CoachProfile, user__id=user_id)
    return render(request, 'eyt/coach_profile_detail.html', {'coach_profile': coach_profile})

########################################################################################################
def video_reviews(request):
    if not request.user.is_authenticated or request.user.role != 'coach':
        return HttpResponseForbidden("Only coaches can access this page.")
    
    # Logic to get the videos that need reviewing, e.g., all uploaded player videos
    videos = Video.objects.all()
    return render(request, 'eyt/video_reviews.html', {'videos': videos})

########################################################################################################
from django.shortcuts import render, get_object_or_404
from .models import Video

########################################################################################################
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'eyt/video_detail.html', {'video': video})

########################################################################################################
def custom_logout(request):
    logout(request)
    return redirect('landing_page')

