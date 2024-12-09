from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('player/<int:user_id>/', views.player_profile_detail, name='player_profile_detail'),
    path('coach/<int:user_id>/', views.coach_profile_detail, name='coach_profile_detail'),
    path('coach/video-reviews/', views.video_reviews, name='video_reviews'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/player/', views.player_profile, name='player_profile'),
    path('profile/coach/', views.coach_profile, name='coach_profile'),
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/', views.video_list, name='video_list'),
    path('playback/<int:video_id>/', views.playback_video, name='playback_video'),
    #path('search/', views.search_coaches, name='search_coaches'),
    #path('select/', views.select_coach, name='select_coach'),
    path('payment/', views.payment, name='payment'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-videos/', views.my_uploaded_videos, name='my_uploaded_videos'),
    path('player/profile/', views.player_profile_view, name='player_profile'),
    path('coach/profile/', views.coach_profile_view, name='coach_profile'),
    path('players/', views.all_player_profiles, name='all_player_profiles'),
    path('coaches/', views.all_coach_profiles, name='all_coach_profiles'),
    path('base/', views.base, name='base'),  
    path('logout/', views.custom_logout, name='logout'),
    path('player/edit-profile/', views.edit_player_profile, name='edit_player_profile'),
    path('coach/edit-profile/', views.edit_coach_profile, name='edit_coach_profile'),
    path('player/<int:player_id>/videos/', views.player_videos_for_review, name='player_videos_for_review'),
    path('video/<int:video_id>/review/', views.add_video_review, name='add_video_review'),
    path('send-email/<int:recipient_id>/', views.send_email_view, name='send_email'),
    path('video_call/<int:coach_id>/', views.video_call_view, name='video_call'),
    path('notifications/', views.notifications_view, name='notifications'),

]














#from django.urls import path
#from .views import register, user_login, user_logout

#urlpatterns = [
#    path('register/', register, name='register'),
#    path('login/', user_login, name='login'),
#    path('logout/', user_logout, name='logout'),
#]



#from django.urls import path
#from . import views





#urlpatterns = [
#    path('', views.homepage, name=""),

#    path('register', views.register, name="register"),

#    path('login', views.login, name="login"),

#    path('coach_profile', views.coach_profile, name="coach_profile"),

#    path('player_profile', views.coach_profile, name="coach_profile")
#]
