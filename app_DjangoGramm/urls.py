from django.urls import path, include

from app_DjangoGramm.views import MainView, RegisterView, MyLoginView, ProfileView, MyLogoutView, EditProfileView, \
    FollowersView, FollowingView, PostView, follow, like, SearchView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('like/', like, name='like'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('follow/<username>/', follow, name='follow'),
    path('profile/<username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<username>/followers/', FollowersView.as_view(), name='followers'),
    path('profile/<username>/following/', FollowingView.as_view(), name='following'),
    path('new_post/', PostView.as_view(), name='new_post'),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('search/', SearchView.as_view(), name='search'),
]
