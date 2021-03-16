from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.db.models import Q
from django.template import loader
from django.conf.urls import url
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import render, redirect
from .forms import sign
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from main.tokens import account_activation_token
from django.db.models import Q
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
from operator import and_, or_
import operator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from functools import reduce
#from friendship.models import Follow, Block
#from .models import FollowingManager
from .models import Topic, User_Groups
from .models import Post, Comment, Repost, Like, Liked_Post, Reshared_Post, Profile, default_profile_pic, Message, Notification, Flagged_Post, User_Groups
from .forms import CommentForm
from .forms import PostForm
from .forms import ProfileForm, ImageForm, MessageForm, DMPostForm, GroupForm
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, ListView
#from star_ratings import app_settings, get_star_ratings_rating_model
#from star_ratings.forms import CreateUserRatingForm
#from star_ratings.compat import is_authenticated
#from . import app_settings, get_star_ratings_rating_model
import json

# Create your views here.
#def homepage(request):
	#return HttpResponse("Wow this is an <strong>awesome</strong> tutorial")

def index(request):
    User = get_user_model()
    users = User.objects.all()
    all_posts = Post.objects.all().order_by('Created').reverse()
    all_reposts = Repost.objects.all().order_by('Created').reverse()
    all_liked = Liked_Post.objects.all()
    com = Comment.objects.filter().count
    #following = Follow.objects.following(request.user)
    default_pic = default_profile_pic.objects.all()
    post_list = zip(all_posts, all_reposts)
    form = PostForm(request.POST or None, request.FILES or None)
    dmForm = MessageForm(request.POST or None)
    group_form = GroupForm(request.POST or None)
    Author = request.user
    
    if request.method == 'POST':
        if 'postFeed' in request.POST:
            Content = form.save(commit=False)
            Content.Author = request.user
            files = request.FILES.getlist('Image')
            fs = FileSystemStorage()
            Content.save()
            form = PostForm(request.POST or None, request.FILES or None, instance=Content)
            return HttpResponse('<script>history.back();</script>')
            
        elif 'like' in request.POST:
            user = User.objects.get(request.user.username)
            post = Post.objects.get(Post, pk=post_id)
            post.LikeCount += 1
            post.save()
            return redirect('<script>history.back();</script>')
            
        #if 'group' in request.POST:
            #if group_form.is_valid():
                #group = group_form.save(commit=False)
                #group.user = request.user
                #group.Label = request.POST['Label']
                #group.Members = request.POST['Members']
                #group.save()
                #User_Groups.objects.create(user=request.user, Label=group.Label, Members=group.Members)
                #return HttpResponse('<script>history.back();</script>')
            
        #if 'DM' in request.POST:
            #post_id = int(request.GET.get("id"))
            #post = get_object_or_404(Post, pk=post_id)
            #msg_content = dmForm.save(commit=False)
            #msg_content.post = post
            #msg_content.sender = request.user
            #msg_content.save(request.POST['msg_content'])
            #return redirect('<script>history.back();</script>')   
            
        
            
    else:
        form = PostForm()    
        dmForm = MessageForm()
        group_form = GroupForm()
        
    context = {
        'User': users,
        'all_posts': all_posts,
        #'following': following,
        'form': form,
        'Author': Author,
        'all_reposts': all_reposts,
        'all_liked': all_liked,
        'post_list': post_list,
        'default_pic': default_pic,
        'dmForm': dmForm,
        'group_form': group_form,
    }
    template = loader.get_template('main/index.html')
    
    return HttpResponse(template.render(context, request))


def inbox(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    DMs = Message.objects.filter(receiver=request.user)
    default_pic = default_profile_pic.objects.all()
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        if 'msg' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.save(request.POST['msg_content'])
                #Message.objects.create(sender=request.user, receiver=message.receiver)
                #return redirect('Purefun/inbox.html')
        else:
            form = MessageForm()
    template = loader.get_template('main/inbox.html')
    context = {
        'DMs': DMs,
        'user': user,
        'form': form,
    }
    return HttpResponse(template.render(context, request)) 


def about(request):
    
    return render(request, 'main/about.html')    


def login(request):
    
    return render(request, 'main/login.html')    

    
def signup(request):
    if request.method == 'POST':
        form = sign(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.is_staff = False
            user.is_superuser = False
            user.is_admin = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Purefun Account'
            message = render_to_string('main/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            login(request, user)
            user.email_user(subject, message)
            return render(request, 'main/account_activation_sent.html')
    else:
        form = sign()
    return render(request, 'main/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.Profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'main/account_activation_invalid.html')

        
def account_activation_sent(request):
    return render(request, 'activate')


def account_activation_email(request):
    return render(request, 'activate')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'main/login.html', {'albums': albums})
            else:
                return render(request, 'main/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Invalid login'})
    return render(request, 'main/login.html')


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    template = loader.get_template('main/user_profile.html')
    context = {
        'User': user,
    }
    return HttpResponse(template.render(context, request))


def get_user_profile(request, username):
    
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(Author=user).order_by('Created').reverse()
    all_reposts = Repost.objects.filter(Reposter=user).order_by('Created').reverse()
    #following = Follow.objects.following(user)
    #followers = Follow.objects.followers(user)
    DMs = Message.objects.filter(receiver=request.user)
    default_pic = default_profile_pic.objects.all()
    template = loader.get_template('main/user_profile.html')
    context = {
        'user': user,
        "user_posts":user_posts,
        'all_reposts': all_reposts,
        'DMs': DMs,
        'default pic': default_pic,
    }
    followee = user
    follower = request.user
    if request.method == "POST":   
        if 'follow' in request.POST:
            Follow.objects.add_follower(follower, followee)
            return HttpResponse('<script>history.back();</script>')

        elif 'unfollow' in request.POST:
            Follow.objects.remove_follower(follower, followee)
            return HttpResponse('<script>history.back();</script>')
            
        elif 'block' in request.POST:
            Follow.objects.remove_follower(follower, followee)
            Block.objects.add_block(follower, followee)
            return HttpResponse('<script>history.back();</script>')
            
        elif 'unblock' in request.POST:
            Block.objects.remove_block(follower, followee)
            return HttpResponse('<script>history.back();</script>')
 
    editable = False

    return HttpResponse(template.render(context, request))


def go_private(request, username):
    
    user = User.objects.get(username=username)
    user.profile.isPrivate = True
    user.profile.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'user': user,
    }
    return HttpResponse('<script>history.back();</script>')
    
    return HttpResponse(template.render(context, request))
    

def go_public(request, username):
    
    user = User.objects.get(username=username)
    user.profile.isPrivate = False
    user.profile.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'user': user,
    }
    return HttpResponse('<script>history.back();</script>')
    
    return HttpResponse(template.render(context, request))     


def followers(request, username, template_name="main/user_profile.html"):
   
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)
    return render(
        request,
        template_name,
        {
            get_friendship_context_object_name(): user,
            "friendship_context_object_name": get_friendship_context_object_name(),
            "followers": followers,
        },
    )


def following(request, username, template_name="main/user_profile.html"):
   
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)
    return render(
        request,
        template_name,
        {
            get_friendship_context_object_name(): user,
            "friendship_context_object_name": get_friendship_context_object_name(),
            "following": following,
        },
    )


def report(request, username):
    
    user = User.objects.get(username=username)
    template = loader.get_template('main/report.html')
    context = {
        'user': user,
    }
    if request.method == 'POST':
        form = report(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() 
            user.save()
            current_site = get_current_site(request)
            return render(request, 'main/edit_profile.html')
    else:
        form = report()  
    editable = False
    if request.user.is_authenticated() and request.user == user:
        editable = True
    return HttpResponse(template.render(context, request))    


def post_detail(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    com = Comment.objects.filter(post_id=post_id).count
    all_comments = Comment.objects.filter(post_id=post_id).order_by('created').reverse()
    user = User.objects.get(username=request.user)
    
    try:
        comments = post.comments
    except:
        comments = None
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if 'comment' in request.POST:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.Author = request.user
                comment.post = post
                post.CommentCount += 1
                post.Comment.add(user)
                post.save()
                comment.save(request.POST['body'])
                user.profile.Notifications += 1
                Notification.objects.create(post=post, sender=request.user, receiver=user, is_comment_notification=True, msg="")
                user.profile.save()
                return redirect('post_detail', post_id=post_id)

    else:
        comment_form = CommentForm()                   
    return render(request,
                  'main/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'com': com,
                   'all_comments': all_comments,
                   'comment_form': comment_form,
                   })
                   

def repost_detail(request, Repost_id):
    
    repost = get_object_or_404(Repost, pk=Repost_id)
    all_comments = Comment.objects.filter(post_id=repost.id).order_by('created').reverse()
    
    try:
        comments = repost.comments
    except:
        comments = None
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if 'comment' in request.POST:
            if form.is_valid():
                repostcomment = form.save(commit=False)
                repostcomment.Author = request.user
                repostcomment.repost = repost
                repostcomment.save(request.POST['body'])
                return redirect('repost_detail', Repost_id=Repost_id)

    else:
        comment_form = CommentForm()                   
    return render(request,
                  'main/repost_detail.html',
                  {'repost': repost,
                   'comments': comments,
                   'all_comments': all_comments,
                   'comment_form': comment_form,
                   })



def repost(request, post_id, username):
    
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(username=username)
    post.Reposts.add(request.user)
    Post.objects.create(Author=post.Author, RepostAuthor=request.user, Content=post.Content, Topic=post.Topic, Image=post.Image, Created=post.Created, IsRepost=True)
    post.ReshareCount += 1
    user.profile.Notifications += 1
    Notification.objects.create(post=post, sender=request.user, receiver=user, is_repost_notification=True, msg="")
    user.profile.save()
    post.IsRepost = True
    post.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return redirect('index')
    
    return HttpResponse(template.render(context, request))
    
    
def DMPost(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(username=request.user)
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        if 'dm' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.receiver = (request.POST['receiver'])
                message.post = post
                message.save(request.POST['msg_content'])
                Message.objects.create(sender=request.user, receiver=message.receiver)
                return redirect('main/inbox.html')
        
    else:
        form = MessageForm()
        
    template = loader.get_template('main/inbox.html')
    context = {
        'post': post,
        'like': like,
        'form': form,
        #'liked': liked,
    }
    #return redirect('index')
    
    return HttpResponse(template.render(context, request))    


def flag(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    Flagged_Post.objects.create(post=post)
    post.Flags.add(request.user)
    post.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
    }
    return redirect('index')
    
    return HttpResponse(template.render(context, request)) 

    
def unrepost(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(username=request.user)
    post.Reposts.remove(user)
    post.ReshareCount -= 1
    #post.objects.filter(id=id).delete()
    #post.IsRepost = False
    post.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return redirect('index')
    
    return HttpResponse(template.render(context, request))    


def like(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(username=username)
    post.Likes.add(request.user)
    post.LikeCount += 1
    user.profile.Notifications += 1
    Notification.objects.create(post=post, sender=request.user, receiver=user, is_like_notification=True, msg="")
    #Flagged_Post.objects.create(post=post)
    user.profile.save()
    post.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return HttpResponse(template.render(context, request))
    
    
def unlike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = User.objects.get(username=request.user)
    post.Likes.remove(user)
    post.LikeCount -= 1
    post.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return HttpResponse(template.render(context, request))  
 
    
def comment(request, post_id):
    User = get_user_model()
    users = User.objects.all()
    com = Comment.objects.filter().count
    following = Follow.objects.following(request.user)
    default_pic = default_profile_pic.objects.all()
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if 'post' in request.POST:
            if form.is_valid():
                Content = form.save(commit=False)
                Content.Author = request.user
                Content.save(request.POST['Content'])
                post = get_object_or_404(Post, pk=post_id)
                post.Comment.add(user)
                post.CommentCount += 1
                post.save()
                return redirect('index')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
    }
    return redirect('index')
    
    return HttpResponse(template.render(context, request))

    
def message(request, post_id):
    User = get_user_model()
    users = User.objects.all()
    post = get_object_or_404(Post, pk=post_id)
    com = Comment.objects.filter().count
    default_pic = default_profile_pic.objects.all()
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        if 'msg' in request.POST:
            if form.is_valid():
                msg_content = form.save(commit=False)
                msg_content.sender = request.user
                msg_content.post = post
                msg_content.save(request.POST['msg_content'])
                return redirect('index')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return redirect('inbox', request.user.username)
    
    return HttpResponse(template.render(context, request))

    
def msg(request, post_id):
    User = get_user_model()
    users = User.objects.all()
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    com = Comment.objects.filter().count
    default_pic = default_profile_pic.objects.all()
    dmForm = MessageForm(request.POST or None)
    #user.profile.MessagesCount += 1
    if request.method == 'POST':
        if 'dm' in request.POST:
            if dmForm.is_valid():
                post = get_object_or_404(Post, pk=post_id)
                msg_content = dmForm.save(commit=False)
                msg_content.post = post
                msg_content.sender = request.user
                user.profile.MessagesCount += 1
                user.save()
                msg_content.save(request.POST['msg_content'])
                return HttpResponse('<script>history.back();</script>')
    else:
        dmForm = MessageForm()
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return redirect('inbox', request.user.username)
    
    return HttpResponse(template.render(context, request))
    

def group(request):
    #user = User.objects.get(request.user)
    users = User.objects.all()
    groups = User_Groups.objects.all()
    group_form = GroupForm(request.POST or None)
    if request.method == 'POST':
        if 'group' in request.POST:
            if group_form.is_valid():
                group = group_form.save(commit=False)
                group.save()
                group.user = request.user
                group.Label = request.POST['Label']
                group.Members = group_form.cleaned_data['Members']
                group.save()
                return HttpResponse('<script>history.back();</script>')
    else:
        group_form = GroupForm()
        
    template = loader.get_template('main/index.html')
    context = {
        'group_form': group_form,
    }
    return HttpResponse('<script>history.back();</script>')
    
    return HttpResponse(template.render(context, request))   


def edit_profile(request):
    
    form = ProfileForm(request.POST or None)
    template = loader.get_template('main/index.html')
    if request.method == 'POST':
        if form.is_valid():
            form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
            user = form.save()
            user.birth_date = form.cleaned_data.get('birth_date')
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.Profile_Picture = form.cleaned_data['profile_pic']
            files = request.FILES.getlist('Profile_Picture')
            fs = FileSystemStorage()
            #if self.request.FILES:
                #for afile in self.request.FILES.getlist('Profile_Picture'):
                    #img = Profile.objects.create(Profile_picture=afile)
            user.save()
            return redirect('index')
    else:
        form = ProfileForm()                   
    return render(request,'main/edit_profile.html',{'form': form,})


def add_post(request):
    
    form = PostForm(request.POST or None)
    template = loader.get_template('main/index.html')
    if request.method == 'POST':
        if form.is_valid():
            form = PostForm(request.POST or None, request.FILES or None, instance=request.user.profile)
            user = form.save()
            user.Image = form.cleaned_data['Image']
            files = request.FILES.getlist('Image')
            fs = FileSystemStorage()
            user.save()
            return redirect('index')
    else:
        form = ProfileForm()                   
    return render(request,'main/edit_profile.html',{'form': form,})


def SearchView(request):
  
  query = request.GET.get('q','')
   
  if query:
    post_queryset = (Q(Content__icontains=query))
    user_queryset = (Q(username__icontains=query))
    #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
    post_results = Post.objects.filter(post_queryset).distinct()
    user_results = User.objects.filter(user_queryset).distinct()
    #topic_results = Topic.objects.filter(queryset).distinct()
  else:
       post_results = []
  return render(request, 'main/search.html', {'post_results':post_results,
  'user_results':user_results,
  'query':query,
  })


def addNotification(request, username, post_id):
    user = User.objects.get(username=request.user)
    user.profile.Notifications += 1
    user.save()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return HttpResponse(template.render(context, request))

    
def viewNotifications(request):
    Notifications = Notification.objects.all()
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'Notifications': Notifications,
    }
    return HttpResponse(template.render(context, request))    
    
    
def removeNotifications(request):
    user = request.user
    all_Notifications = Notification.objects.all()
    user.profile.Notifications = 0
    user.profile.save()
    #user.save()
        
    template = loader.get_template('main/notifications.html')
    context = {
        'all_Notifications': all_Notifications,
    }
    return HttpResponse(template.render(context, request))

    
def topics(request, label):
    #topic = Topic.objects.filter(Topic__Label__icontains=label) 
    topic = Topic.objects.filter(Topic__Label__icontains=label)
    all_topics = Topic.objects.all() 
    template = loader.get_template('Purefun/topics.html')
    context = {
        'topic': topic,
        'all_topics': all_topics,
    }
    return HttpResponse(template.render(context, request))     

    
def create_group(request):
    group = group_form.save(commit=False)
    group.user = request.user
    group.save()
    group.Members = (request.POST['Members'])
    group.save()
    group_form = GroupForm(request.POST or None, request.FILES or None, instance=group)
    return HttpResponse('<script>history.back();</script>')
        
    template = loader.get_template('main/index.html')
    context = {
        'post': post,
        'like': like,
        #'liked': liked,
    }
    return HttpResponse(template.render(context, request))    

  
def get_client_ip(request):
    remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
            if len(proxies) > 0:
                ip = proxies[0]
                #print"IP Address",ip
        return ip


class ProfileList(APIView):

	def get(self, request):
		profiles = Profile.objects.all()
		serializer = ProfileSerializer(profiles, many=True)
		return Response(serializer.data)           	
