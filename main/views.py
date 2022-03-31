from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import update_last_login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
import json
from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q
from django.template import loader
#from django.conf.urls import url
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import render, redirect
from .forms import sign
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
#from django.utils.encoding import force_text
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
import logging
import pprint
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from .serializers import PostSerializer
from .serializers import LikePostSerializer
from .serializers import MessageSerializer
from .serializers import NotificationSerializer
from .serializers import GroupSerializer
from .serializers import TopicSerializer
from .serializers import LoginSerializers
from .serializers import TemplateSerializer
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from functools import reduce
from .models import Meme_Template, Topic, User_Groups
from .models import Post, Comment, Repost, Like, Liked_Post, Reshared_Post, Profile, default_profile_pic, Message, Notification, Flagged_Post, User_Groups
from .forms import CommentForm
from .forms import PostForm
from .forms import ProfileForm, ImageForm, MessageForm, DMPostForm, GroupForm
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


import json

# Create your views here.
#def homepage(request):
	#return HttpResponse("Wow this is an <strong>awesome</strong> tutorial")

def index(request):
	User = get_user_model()
	users = User.objects.all()
	all_posts = Post.objects.filter(Q(Author__profile__User_Followers__username__icontains=request.user)).order_by('Created').reverse()
	all_reposts = Repost.objects.all().order_by('Created').reverse()
	all_liked = Liked_Post.objects.all()
	com = Comment.objects.filter().count
	following = request.user.profile.User_Following
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
			Content.Author_Profile = request.user.profile
			files = request.FILES.getlist('Image')
			fs = FileSystemStorage()
			Content.save()
			form = PostForm(request.POST or None, request.FILES or None, instance=Content)
			return HttpResponse('<script>history.back();</script>')
			
		#elif 'like' in request.POST:
			#user = User.objects.get(request.user.username)
			#post = Post.objects.get(Post, pk=post_id)
			#post.LikeCount += 1
		#post.save()
			#return redirect('index')
			
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
		'following': following,
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
			#Follow.objects.add_follower(follower, followee)
			#Follow_obj.objects.create(user=user, user_follower=request.user)
			if user.profile.isPrivate == True:
				sendFollowRequest(request, user)
				
			else:
				request.user.profile.User_Following.add(user)
				request.user.profile.Following_Count += 1
				request.user.profile.save()
				user.profile.User_Followers.add(request.user)
				user.profile.Notifications += 1
				user.profile.Follower_Count += 1
				user.profile.save()
				Notification.objects.create(sender=request.user, receiver=user, is_follow_notification=True, msg="")
				
			
			return HttpResponse('<script>history.back();</script>')
			

		elif 'unfollow' in request.POST:
		   # Follow.objects.remove_follower(follower, followee)
			request.user.profile.User_Following.remove(user)
			request.user.profile.Following_Count -= 1
			request.user.profile.save()
			user.profile.User_Followers.remove(request.user)
			user.profile.Follower_Count -= 1
			user.profile.save()
			return HttpResponse('<script>history.back();</script>')
			
		elif 'block' in request.POST:
			request.user.profile.User_Following.remove(user)
			user.profile.User_Followers.remove(request.user)
			user.profile.save()
			request.user.profile.Blocked_Users.add(user)
			request.user.profile.save()
			return HttpResponse('<script>history.back();</script>')
			
		elif 'unblock' in request.POST:
			request.user.profile.Blocked_Users.remove(user)
			return HttpResponse('<script>history.back();</script>')
			
		elif 'mute' in request.POST:
			request.user.profile.Muted_Users.add(user)
			request.user.profile.save()
			return HttpResponse('<script>history.back();</script>')
			
		elif 'unmute' in request.POST:
			request.user.profile.Muted_Users.remove(user)
			request.user.profile.save()
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



def repost(post_id, user):
	
	post = get_object_or_404(Post, pk=post_id)
	user = User.objects.get(pk=user.id)
	post.Reposts.add(user)
	Post.objects.create(Author=post.Author, RepostAuthor=user, Content=post.Content, Topic=post.Topic, Image=post.Image, Image2=post.Image2, Image3=post.Image3, Image4=post.Image4, Created=post.Created, IsRepost=True)
	post.ReshareCount += 1
	user.profile.Notifications += 1
	Notification.objects.create(post=post, sender=user, receiver=user, is_repost_notification=True, msg="")
	user.profile.save()
	post.IsRepost = False
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


def like(post_id, user):
	post = get_object_or_404(Post, pk=post_id)
	u = User.objects.get(pk=user.id)
	post.Likes.add(user)
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(user.id)
	post.LikeCount += 1
	post.IsLike = False
	user.profile.Notifications += 1
	Notification.objects.create(post=post, sender=user, receiver=post.Author, is_like_notification=True, msg="")
	#Flagged_Post.objects.create(post=post)
	user.profile.save()
	post.save()
	return HttpResponse('<script>history.back();</script>')
	#return redirect('index')
		
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
				group.Members.set()
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
	group.Members = Members.set()
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


SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'
LANGUAGE_SESSION_KEY = '_language'
permission_classes = [permissions.AllowAny]
def loginn(request, user, backend=None):
	"""
	Persist a user id and a backend in the request. This way a user doesn't
	have to reauthenticate on every request. Note that data set during
	the anonymous session is retained when the user logs in.
	"""
	session_auth_hash = ''
	if user is None:
		user = request.user
	if hasattr(user, 'get_session_auth_hash'):
		session_auth_hash = user.get_session_auth_hash()

	if SESSION_KEY in request.session:
		if _get_user_session_key(request) != user.pk or (
				session_auth_hash and
				not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
			# To avoid reusing another user's session, create a new, empty
			# session if the existing session corresponds to a different
			# authenticated user.
			request.session.flush()
	else:
		request.session.cycle_key()

	try:
		backend = backend or user.backend
	except AttributeError:
		backends = _get_backends(return_tuples=True)
		if len(backends) == 1:
			_, backend = backends[0]
		else:
			raise ValueError(
				'You have multiple authentication backends configured and '
				'therefore must provide the `backend` argument or set the '
				'`backend` attribute on the user.'
			)

	request.session[SESSION_KEY] = user.pk
	request.session[BACKEND_SESSION_KEY] = backend
	request.session[HASH_SESSION_KEY] = session_auth_hash
	if hasattr(request, 'user'):
		request.user = user
	rotate_token(request)
	user_logged_in.send(sender=user.__class__, request=request, user=user)



def createComment(request, post_id, data):

	old_post = get_object_or_404(Post, pk=post_id)
	user = request.user
	OP = old_post.Author
	OP.profile.Notifications += 1
	OP.profile.save()
	reply = request.data.get('Content')
	Post.objects.create(Author=user, Content=reply, IsOriginalpost = False, IsComment = True, PostItem = old_post)
	OP.profile.save()
	old_post.Comment.add(user)
	old_post.CommentCount += 1
	old_post.save()
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(old_post.Content)
	pp.pprint("CommentCount")
	pp.pprint(old_post.CommentCount)
	#Notification.objects.create(post=old_post, sender=user, receiver=OP, is_comment_notification=True, msg="")

	return HttpResponse('<script>history.back();</script>') 


@method_decorator(csrf_exempt, name='post')
class LoginViewSet(APIView):
	permission_classes = [permissions.AllowAny]
	@csrf_exempt
	def post(self, request):
		#permission_classes = [permissions.IsAuthenticated]
		serializer = LoginSerializers(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.validate(data=request.data)
		username = request.data.get('username')
		password = request.data.get('password')	
		user = authenticate(username=username, password=password)
		pp = pprint.PrettyPrinter(indent=4)
		login(request)
		update_last_login(None, user)
		pp.pprint("logged in")
		pp.pprint(user.pk)
		pp.pprint(username)
		pp.pprint(password)
		token = account_activation_token.make_token(user)
		pp.pprint(token)
		user.is_active = True
		request.user = user
		pp.pprint(request.user)
		return Response({"status": status.HTTP_200_OK, "Token": token})

	def get(self, request):
		permission_classes = [permissions.AllowAny]
		info = Profile.objects.all()
		serializer = LoginSerializers(info, many=True)
		return Response(serializer.data)

class ProfileViewSet(APIView):
	queryset = Profile.objects.all()#permission_classes = (permissions.AllowAny,)
	serializer = ProfileSerializer(queryset, many=True)
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		permission_classes = [permissions.AllowAny]
		profiles = Profile.objects.filter(user=request.user)
		serializer = ProfileSerializer(profiles, many=True)
		return Response(serializer.data)


class ProfileOtherUserViewSet(APIView):
	queryset = Profile.objects.all()#permission_classes = (permissions.AllowAny,)
	serializer = ProfileSerializer(queryset, many=True)
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		permission_classes = [permissions.AllowAny]
		profile = Profile.objects.all()
		serializer = ProfileSerializer(profile, many=True)
		return Response(serializer.data)		

class PostDetailViewSet(APIView):
	queryset = Post.objects.all()#permission_classes = (permissions.AllowAny,)
	serializer = PostSerializer(queryset, many=True)
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		#queryset = Profile.objects.all()
		data = request.data
		post_id = request.data.get('id')
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(post_id)
		posts = Post.objects.filter(Q(id=post_id))
		#posts = Post.objects.all()
		serializer = PostSerializer(posts, many=True)
		prepared_data_variable = request.user
		return Response(serializer.data)		

#@method_decorator(csrf_exempt, name='dispatch')
class PostViewSet(APIView):
	queryset = Post.objects.all()#permission_classes = (permissions.AllowAny,)
	serializer = PostSerializer(queryset, many=True)
	#permission_classes = [permissions.AllowAny]
	permission_classes = [HasAPIKey]
	def get(self, request):
		#queryset = Profile.objects.all()
		#Author__contains=request.user.profile.User_Following
 
		viewer = request.user
			#return i
		#d = .aut                         
		posts = Post.objects.filter(Q(Author__profile__User_Followers__username__icontains=viewer, IsComment=False)).order_by('id').reverse()

		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)

	@csrf_exempt
	def post(self, request):
		#form = PostForm(request.POST or None, request.FILES or None)
		prepared_data_variable = request.user  #and serializer.validated_data['IsRepost'] == False
		serializer = PostSerializer(data=request.data)
		pp = pprint.PrettyPrinter(indent=4)
		username = request.user.username
		user = request.user
		data = request.data
		#post_to_feed(request, data)
		Content = data.get('Content')
		checked = "My vibe has been checked :("

		if "enate" in Content:
			Content = checked
		if "olitic" in Content:
			Content = checked	
		if "limate" in Content:
			Content = checked
		if "rump" in Content:
			Content = checked
		if "police" in Content:
			Content = checked
		if "elect" in Content:
			Content = checked
		if "epublican" in Content:
			Content = checked
		if "emocrat" in Content:
			Content = checked
		if "Biden" in Content:
			Content = checked
		if "acist" in Content:
			Content = checked
		if "acism" in Content:
			Content = checked
		if "ropaganda" in Content:
			Content = checked
		if "emocracy" in Content:
			Content = checked
		if "racial" in Content:
			Content = checked
		if "acial" in Content:
			Content = checked    
		if "rivelage" in Content:
			Content = checked
		if "hite" in Content:
			Content = checked
		if "lave" in Content:
			Content = checked
		if "BLM" in Content:
			Content = checked
		if "blm" in Content:
			Content = checked
		if "lack lives matter" in Content:
			Content = checked
		if "president" in Content:
			Content = checked
		if "vote" in Content:
			Content = checked
		if "GOP" in Content:
			Content = checked
		if "upreme court" in Content:
			Content = checked
		if "KKK" in Content:
			Content = checked
		if "ongress" in Content:
			Content = checked
		if "apitol" in Content:
			Content = checked
		if "law" in Content:
			Content = checked
		if "tax" in Content:
			Content = checked
		if "DNC" in Content:
			Content = checked
		if "RNC" in Content:
			Content = checked
		if "andidate" in Content:
			Content = checked
		if "CNN" in Content:
			Content = checked
		if "olice" in Content:
			Content = checked
		if "fficer" in Content:
			Content = checked
		if "enator" in Content:
			Content = checked
		if "overn" in Content:
			Content = checked
		if "onstitution" in Content:
			Content = checked
		if "NRA" in Content:
			Content = checked
		if "nra" in Content:
			Content = checked
		if "kkk" in Content:
			Content = checked
		if "ealthcare" in Content:
			Content = checked
		if "mendmant" in Content:
			Content = checked
		if "gun" in Content:
			Content = checked
		if "ilibuster" in Content:
			Content = checked
		if "hite house" in Content:
			Content = checked
		if "hite House" in Content:
			Content = checked
		if "ederal" in Content:
			Content = checked
		if "QAnon" in Content:
			Content = checked
		if "ovid" in Content:
			Content = checked
		if "accin" in Content:
			Content = checked
		if "ommunis" in Content:
			Content = checked
		if "Asian" in Content:
			Content = checked
		if "union" in Content:
			Content = checked
		if "tudent debt" in Content:
			Content = checked
		if "tudent Debt" in Content:
			Content = checked
		if "rotest" in Content:
			Content = checked
		if "orporation" in Content:
			Content = checked
		if "ight wing" in Content:
			Content = checked
		if "eft wing" in Content:
			Content = checked
		if "ight-wing" in Content:
			Content = checked
		if "eft-wing" in Content:
			Content = checked 
		if "mmigrant" in Content:
			Content = checked
		if "edicare" in Content:
			Content = checked
		if "edicaid" in Content:
			Content = checked
		if "ecretary" in Content:
			Content = checked
		if "ilitary" in Content:
			Content = checked
		if "Obama" in Content:
			Content = checked
		if "obama" in Content:
			Content = checked
		if "un control" in Content:
			Content = checked
		if "azi" in Content:
			Content = checked
		if "iot" in Content:
			Content = checked
		if "USDA" in Content:
			Content = checked
		if "usda" in Content:
			Content = checked
		if "FDA" in Content:
			Content = checked
		if "fda" in Content:
			Content = checked
		if "ascis" in Content:
			Content = checked
		if "harma" in Content:
			Content = checked
		if "FBI" in Content:
			Content = checked
		if "Tax" in Content:
			Content = checked
		if "uthoritarian" in Content:
			Content = checked
		if "olitician" in Content:
			Content = checked
		if "onservative" in Content:
			Content = checked
		if "uslim" in Content:
			Content = checked
		if "lection" in Content:
			Content = checked
		if "hristian" in Content:
			Content = checked
		if "arxis" in Content:
			Content = checked
		if "narch" in Content:
			Content = checked
		if "OVID" in Content:
			Content = checked
		if "oronavirus" in Content:
			Content = checked
		if "elhi" in Content:
			Content = checked
		if "media" in Content:
			Content = checked
		if "Media" in Content:
			Content = checked
		if "United States" in Content:
			Content = checked
		if "hreat" in Content:
			Content = checked
		if "AOC" in Content:
			Content = checked
		if "aoc" in Content:
			Content = checked
		if "God " in Content:
			Content = checked
		if "ibertarian" in Content:
			Content = checked
		if "iberal" in Content:
			Content = checked
		if "1A" in Content:
			Content = checked
		if "2A" in Content:
			Content = checked
		if "saki" in Content:
			Content = checked
		if "order" in Content:
			Content = checked
		if "un control" in Content:
			Content = checked
		if "eftist" in Content:
			Content = checked
		if "mpeach" in Content:
			Content = checked
		if "ountry" in Content:
			Content = checked
		if "ountries" in Content:
			Content = checked
		if "partisan" in Content:
			Content = checked
		if "Partisan" in Content:
			Content = checked
		if "lobal" in Content:
			Content = checked
		if "auci" in Content:
			Content = checked
		if "Cox" in Content:
			Content = checked
		if "reen party" in Content:
			Content = checked
		if "reen Party" in Content:
			Content = checked
		if "ncap" in Content:
			Content = checked
		if "rexit" in Content:
			Content = checked
		if "onfederate" in Content:
			Content = checked
		if "flag" in Content:
			Content = checked
		if "IRS" in Content:
			Content = checked
		if "ardon" in Content:
			Content = checked
		if "Build Back Better" in Content:
			Content = checked
		if "uild back better" in Content:
			Content = checked
		if "nigge" in Content:
			Content = checked
		if "Nigge" in Content:
			Content = checked    
		if "range man" in Content:
			Content = checked
		if "range Man" in Content:
			Content = checked
		if "hristian" in Content:
			Content = checked
		if "ewish" in Content:
			Content = checked
		if "Jew" in Content:
			Content = checked
		if "jew" in Content:
			Content = checked
		if "Jesus do" in Content:
			Content = checked
		if "Jesus said" in Content:
			Content = checked
		if "ace theory" in Content:
			Content = checked
		if "ace Theory" in Content:
			Content = checked
		if "ar on Drugs" in Content:
			Content = checked
		if "ar on drugs" in Content:
			Content = checked
		if "leepy Joe" in Content:
			Content = checked
		if "leepy joe" in Content:
			Content = checked
		if "aetz" in Content:
			Content = checked
		if "allot" in Content:
			Content = checked
		if "stablish" in Content:
			Content = checked
		if "he news" in Content:
			Content = checked
		if "ox news" in Content:
			Content = checked
		if "ox News" in Content:
			Content = checked
		if "ransphob" in Content:
			Content = checked
		if " rights" in Content:
			Content = checked
		if "Rights" in Content:
			Content = checked
		if "egulat" in Content:
			Content = checked
		if "ender" in Content:
			Content = checked
		if "olocaust" in Content:
			Content = checked
		if "eminis" in Content:
			Content = checked
		if "elfare" in Content:
			Content = checked
		if "hapiro" in Content:
			Content = checked
		if "ucker Carlson" in Content:
			Content = checked
		if "ucker carlson" in Content:
			Content = checked
		if "itch Mcconnel" in Content:
			Content = checked
		if "itler" in Content:
			Content = checked
		if "anon" in Content:
			Content = checked
		if "eagan" in Content:
			Content = checked
		if " war" in Content:
			Content = checked
		if "War " in Content:
			Content = checked
		if "ussia" in Content:
			Content = checked
		if "nvade" in Content:
			Content = checked
		if "roops" in Content:
			Content = checked
		if "WW3" in Content:
			Content = checked
		if "ar 3" in Content:
			Content = checked
		if "ar III" in Content:
			Content = checked
		if "WWIII" in Content:
			Content = checked
		if "JB" in Content:
			Content = checked
		if "jb" in Content:
			Content = checked											
		else:
			Content = Content
		if serializer.is_valid():
			if serializer.validated_data['IsRepost'] != True and serializer.validated_data['IsLike'] == False and serializer.validated_data['IsComment'] == False:
				serializer.validated_data['Author'] = prepared_data_variable
				serializer.validated_data['Author_Profile'] = request.user.profile
				serializer.validated_data['Content'] = Content
				serializer.validated_data['Image'] = serializer.validated_data['ImageString']
				serializer.save()
			elif serializer.validated_data['IsRepost'] != False and serializer.validated_data['IsLike'] == False and serializer.validated_data['IsComment'] == False:
				post_id = request.data.get('id')
				pp.pprint('Reposted')
				repost(post_id, user)
				return Response()
			elif serializer.validated_data['IsLike'] != False and serializer.validated_data['IsComment'] == False:
				post_id = request.data.get('id')
				pp.pprint(user.id)
				like(post_id, user)
				return Response()
			elif serializer.validated_data['IsComment'] != False and serializer.validated_data['IsLike'] != True:
				post_id = request.data.get('id')
				pp.pprint('comment')
				pp.pprint(post_id)
				createComment(request, post_id, data)
				return Response()					    
		return Response(serializer.data)
   
	def put(self, request):
		username = request.user.username
		pp = pprint.PrettyPrinter(indent=4)
		form = PostForm(request.POST or None, request.FILES or None)
		serializer = PostSerializer(data=request.data)
		post_id = request.data.get('id')
		like(request, post_id, username)
		pp.pprint('putt')
		#serializer.data.LikeCount = 15
		#post.Likes.add(request.user)
		#post.LikeCount += 1
		if serializer.is_valid():
			post_id = request.data.get('id')
			like(request, post_id, username)
			pp.pprint('putt')
			return Response()
		return Response(serializer.data)

#@csrf_exempt					
class ImageViewSet(APIView):
	queryset = Meme_Template.objects.all()
	permission_classes = [permissions.AllowAny]
	serializer = TemplateSerializer(queryset, many=True)
	@csrf_exempt
	def post(self, request):
		#post = Meme.objects.all()
		#prepared_data_variable = request.user
		serializer = TemplateSerializer(data=request.data)
		#messages = Message.objects.filter(Q(receiver__username=request.user.username) | Q(sender__username=request.user.username))
		#receiver = serializer.receiver
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data)  



class MessageViewSet(APIView):
	queryset = Message.objects.all()
	serializer = MessageSerializer(queryset, many=True)
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		#queryset = Profile.objects.all()
		permission_classes = [permissions.IsAuthenticated]
		messages = Message.objects.filter(Q(receiver__username=request.user.username)).order_by('created_at').reverse()
		serializer = MessageSerializer(messages, many=True)
		prepared_data_variable = request.user
		return Response(serializer.data)

	def post(self, request):
		permission_classes = [permissions.IsAuthenticated]
		prepared_data_variable = request.user
		form = MessageForm(request.POST or None)
		serializer = MessageSerializer(data=request.data)
		#messages = Message.objects.filter(Q(receiver__username=request.user.username) | Q(sender__username=request.user.username))
		#receiver = serializer.receiver
		data = request.data
		if serializer.is_valid():
			if serializer.validated_data['is_shared_post'] == True:
				post_id = data.get('post_id')
				msg(request, post_id)
			serializer.validated_data['sender'] = prepared_data_variable
			serializer.validated_data['receiver'] = data.get('receiver')
			serializer.validated_data['msg_content'] = data.get('msg_content')
			Message.objects.create(sender=request.user, msg_content=data.get('msg_content'), receiver=data.get('receiver'))
		return Response(serializer.data)
  

class LikeViewSet(APIView):
	queryset = Post.objects.all()
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		serializer = LikePostSerializer(data=request.data)
		return Response(serializer.data)

	def post(self, request):
		permission_classes = [permissions.IsAuthenticated]
		post = Post.objects.all()
		prepared_data_variable = request.user
		serializer = PostSerializer(data=request.data)
		#messages = Message.objects.filter(Q(receiver__username=request.user.username) | Q(sender__username=request.user.username))
		#receiver = serializer.receiver
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data)        	


class NotificationViewSet(APIView):
	queryset = Notification.objects.all()
	serializer = NotificationSerializer(queryset, many=True)
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		#queryset = Profile.objects.all()
		permission_classes = [permissions.IsAuthenticated]
		notifications = Notification.objects.filter(receiver=request.user).order_by('created_at').reverse()
		serializer = NotificationSerializer(notifications, many=True)
		prepared_data_variable = request.user
		return Response(serializer.data)
  
	def post(self, request):
		permission_classes = [permissions.IsAuthenticated]
		prepared_data_variable = request.user
		serializer = NotificationSerializer(data=request.data)
		notifications = Message.objects.filter(receiver=request.user)
		if serializer.is_valid():
			serializer.validated_data['sender'] = prepared_data_variable
			serializer.save()
		return Response(serializer.data)			

							
class GroupViewSet(APIView):

	def get(self, request):
		#queryset = Profile.objects.all()
		groups = User_Groups.objects.filter(user=request.user)
		serializer = GroupSerializer(groups, many=True)
		prepared_data_variable = request.user
		return Response(serializer.data)


class TopicViewSet(APIView):

	def get(self, request):
		#queryset = Profile.objects.all()
		topics = Topic.objects.all()
		serializer = TopicSerializer(topics, many=True)
		return Response(serializer.data)		

#Content = form.save(commit=False)
		#Content.Author = request.user
		#files = request.FILES.getlist('Image')
		#fs = FileSystemStorage()
		#Content.save()
		#form = PostForm(request.POST or None, request.FILES or None, instance=Content)








