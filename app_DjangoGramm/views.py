import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from app_DjangoGramm.forms import RegisterForm, LoginForm, ProfileForm, PostForm
from app_DjangoGramm.models import Post, Profile, User, Follower, Like


@login_required
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        liking = Like.objects.filter(profile_id=request.user.profile, post=post)
        count_likes = len(Like.objects.filter(post=post))
        if liking:
            Like.unlike(request.user.profile, post)
            is_liking = False
            count_likes -= 1
        else:
            Like.like(request.user.profile, post)
            is_liking = True
            count_likes += 1
        data = {
            'value': is_liking,
            'count_likes': count_likes,
        }
        return JsonResponse(data, safe=False)
    return HttpResponseRedirect(reverse('main'))


class MainView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        my_following = Follower.objects.filter(user_id=request.user).values('following_user_id')
        posts = Post.objects.filter(Q(user__in=my_following) | Q(user=request.user)).order_by('-id').\
            annotate(amount_likes=Count('liked_post'))
        likes = Like.objects.filter(profile_id=request.user.profile).select_related('post')
        liked_posts = [like.post for like in likes]
        context = {
            'posts': posts,
            'liked_posts': liked_posts,
            'title': 'Main'
        }
        return render(request, 'main.html', context=context)


@login_required
def follow(request, username):
    if request.method == 'POST':
        following_user = User.objects.get(username=username)
        following = Follower.objects.filter(user_id=request.user, following_user_id=following_user)
        if following:
            Follower.unfollow(request.user, following_user)
            is_following = False
        else:
            Follower.follow(request.user, following_user)
            is_following = True
        resp = {'following': is_following}
        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json")
    return HttpResponseRedirect(reverse('profile', args=(username,)))


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, username):

        if username == request.user.username:
            profile, created = Profile.objects.get_or_create(user=request.user)
        else:
            profile = get_object_or_404(Profile, user__username=username)
        following_user = User.objects.get(username=username)
        is_following = Follower.objects.filter(user_id=request.user, following_user_id=following_user)
        posts = Post.objects.filter(user__username=username).order_by('-id').annotate(amount_likes=Count('liked_post'))
        likes = Like.objects.filter(profile_id=profile).select_related('post')
        liked_posts = [like.post for like in likes]
        context = {
            'profile': profile,
            'posts': posts,
            'following': is_following,
            'liked_posts': liked_posts,
            'title': 'My profile',
        }
        return render(request, 'profile.html', context=context)


class EditProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, username):
        if username == request.user.username:
            profile = Profile.objects.get(user=request.user)
        else:
            return HttpResponseRedirect(reverse('profile', args=(username,)))
        profile_form = ProfileForm(instance=profile)
        context = {
            'form': profile_form,
            'title': 'Edit Profile',
        }
        return render(request, 'edit_profile.html', context=context)

    def post(self, request, username):
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            edit_profile = profile_form.save(commit=False)
            edit_profile.user = request.user
            edit_profile.save()
            return HttpResponseRedirect(reverse('profile', args=(username,)))
        return render(request, 'edit_profile.html', {'form': profile_form})


class FollowersView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, username):
        followers = Follower.objects.filter(following_user_id__username=username)
        context = {
            'followers': followers,
            'title': 'Followers'
        }
        return render(request, 'followers.html', context=context)


class FollowingView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, username):
        following = Follower.objects.filter(user_id__username=username)
        context = {
            'following': following,
            'title': 'Followers'
        }
        return render(request, 'following.html', context=context)


class PostView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        post_form = PostForm()
        context = {
            'form': post_form,
            'title': 'New Post',
        }
        return render(request, 'new_post.html', context=context)

    def post(self, request):
        post = Post.objects.create(user=request.user)
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'new_post.html', {'form': post_form})


class MyLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_success_url(self):
        return reverse('profile', args=(self.request.POST.get('username'),))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('main'))


class MyLogoutView(LogoutView):
    next_page = '/'
