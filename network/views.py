from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Post, UserRelation

class NewPostForm(forms.Form):
    content = forms.CharField(max_length=200, label='', widget=forms.Textarea(attrs={'class': 'create-field', 'placeholder': "What's Happening?"}))

@login_required(login_url="login")
def edit(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data=json.loads(request.body)
    edit_post = Post.objects.get(pk=id)
    if edit_post.content == data['content']:
        return JsonResponse({"message": "No change detected ", "data": data['content']})
    edit_post.content = data['content']
    edit_post.save()
    return JsonResponse({"message": "Post Edited Successfully.", "data": data['content']})

@login_required(login_url="login")
def addlike(request, id):
    post = Post.objects.get(pk=id)
    currentUser = request.user
    post.likes.add(currentUser)
    count = post.likes.count()
    return JsonResponse({"message": "Post Liked!", "data": count })

@login_required(login_url="login")
def removelike(request, id):
    post = Post.objects.get(pk=id)
    currentUser = request.user
    post.likes.remove(currentUser)
    count = post.likes.count()
    return JsonResponse({"message": "Post Unliked!", "data": count })


def index(request):
    allPosts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(allPosts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    whoYouLiked = []

    try:
        for post in page_obj:
            if request.user in post.likes.all():
                whoYouLiked.append(post.id)
    except:
        whoYouLiked=[]
    
    return render(request, "network/index.html", {
        'allPosts': allPosts,
        'newPostForm': NewPostForm(),
        'page_obj': page_obj,
        'allposts': True,
        'whoYouLiked': whoYouLiked,
    })

@login_required(login_url="login")
def newPost(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            currentUser = request.user
            newPost = Post(content=content, author=currentUser)
            newPost.save()
            return HttpResponseRedirect(reverse('index'))
        
def Profile(request, id):
    profile = User.objects.get(pk=id)
    userPosts = profile.writer.all().order_by('id').reverse()
    
    followers = UserRelation.objects.filter(userf=profile)
    following = UserRelation.objects.filter(follower=profile)

    try:
        checkFollow = followers.filter(follower=User.objects.get(pk=request.user.id))
        if (len(checkFollow) != 0):
            isFollowing = True
        else: 
            isFollowing = False
    except:
        isFollowing = False

    paginator = Paginator(userPosts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    whoYouLiked = []
    likes = {}
    try:
        for post in page_obj:
            if request.user in post.likes.all():
                whoYouLiked.append(post.id)
    except:
        whoYouLiked=[]
    return render(request, "network/profile.html", {
        'profile': profile,
        'userPosts': userPosts,
        'page_obj': page_obj,
        'followers': followers,
        'following': following,
        'isFollowing': isFollowing,
        'whoYouLiked': whoYouLiked,
        'likes': likes

    })

@login_required(login_url="login")
def unfollow(request):
    if request.method == 'POST':
        profile_name = request.POST['follow']
        profile = User.objects.get(username=profile_name)
        UserRelation.objects.get(userf=profile, follower=request.user).delete()
        return HttpResponseRedirect(reverse('profile', args=(profile.id, )))

@login_required(login_url="login")
def follow(request):
    if request.method == 'POST':
        profile_name = request.POST['follow']
        profile = User.objects.get(username=profile_name)  
        newFollow= UserRelation(userf=profile, follower=request.user)
        newFollow.save()
        return HttpResponseRedirect(reverse('profile', args=(profile.id, )))
    
@login_required(login_url="login")
def following(request):
    following = UserRelation.objects.filter(follower=request.user)
    allPosts = Post.objects.all().order_by('id').reverse()
    followingPosts = []

    for post in allPosts:
        for person in following:
            if person.userf == post.author:
                followingPosts.append(post) 

    paginator = Paginator(followingPosts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'newPostForm': NewPostForm(),
        'page_obj': page_obj,
        'allposts': False
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
