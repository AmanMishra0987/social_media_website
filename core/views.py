from django.forms import ImageField
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain


# Create your views here.
@login_required(login_url='signin')
def index (request):
    user_profile = Profile.objects.get_or_create(user=request.user,id_user=request.user.id)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_lists = list(chain(*feed))
    
    posts = Post.objects.all()
    return render(request,"index.html",{'user_profile': user_profile,'posts':posts})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken') 
                return redirect('signup')
            else:
                user =User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login = auth.authenticate(username=username,email=email,password=password)
                auth.login(request,user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup')
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
    return render(request,'signin.html')

def login(request):
    return render(request,"index.html")

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return render(request,"signin.html")

@login_required(login_url='signin')
def setting(request):
    user_profile,created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('setting')


    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else: 
        return redirect('/')

def profile(request,username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=request.user.username)
    user_post_length = len(user_post)

  


    follower = request.user.username
    user = request.user.username 
    
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=request.user.username))
    user_following = len(FollowersCount.objects.filter(follower=request.user.username))



    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post': user_post ,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    }

    return render(request,'profile.html',context)

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    from django.shortcuts import redirect
from .models import FollowersCount

def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if FollowersCount.objects.filter(follower=follower, user=user).exists():
            # If already following, unfollow
            FollowersCount.objects.filter(follower=follower, user=user).delete()
        else:
            # If not following, follow
            FollowersCount.objects.create(follower=follower, user=user)

    # Redirect to the profile page of the user being followed/unfollowed
    return redirect('profile', username=user)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'post':
        username = request.post['username']
        username_object = User.objects.filter(username__icontain=username)
        username_profile = []
        username_profile_list =[]
        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids) 
            username_profile_list.append(profile_lists)

        username_profile_lists = list(chain(*username_profile_list))
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})
