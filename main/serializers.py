from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, get_user_model
from .models import Profile
from .models import Post
from .models import Message
from .models import Notification
from .models import User_Groups
from .models import Topic
from .models import Meme_Template
from rest_framework import serializers
from django.core.files import File
from django.utils.translation import gettext_lazy as _
import base64






class TemplateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Meme_Template
		fields = (
		'id',
		'Image',
		) 


class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	Profile_Picture = serializers.SerializerMethodField()
	Display_Name = serializers.SerializerMethodField()
	def get_user(self, Profile):
		if Profile.user.username:
			return Profile.user.username
		return default
	def get_likes(self, Profile):
		if Profile.Liked_posts:
			return Profile.Liked_posts.Content
		return ""
	def get_Profile_Picture(self, Profile):
		if Profile.Profile_Picture:
			return Profile.Profile_Picture.url
		return ""
	def get_Display_Name(self, Profile):
		if Profile.Display_Name:
			return Profile.Display_Name
		return ""

	
	class Meta:
		model = Profile
		fields = (
		'id',	
		'user',
		'Display_Name',
		'bio',
		'location',
		'birth_date',
		'User_Following',
		'User_Followers',
		'Profile_Picture',
		'Cover_Picture',
		'likes',	
		)           


class PostSerializer(serializers.ModelSerializer):
	Author = serializers.SerializerMethodField()
	Author_Profile_Picture = serializers.SerializerMethodField()
	Author_Display_Name = serializers.SerializerMethodField()
	Image = serializers.SerializerMethodField()
	Image2 = serializers.SerializerMethodField()
	Image3 = serializers.SerializerMethodField()
	Image4 = serializers.SerializerMethodField()
	RepostAuthor = serializers.SerializerMethodField()
	def get_Author(self, Post):
		if Post.Author:
			return Post.Author.username
		return ""
	def get_Author_Profile_Picture(self, Post):
		if Post.Author.profile.Profile_Picture:
			return Post.Author.profile.Profile_Picture.url
		return ""
	def get_Author_Display_Name(self, Post):
		if Post.Author.profile.Display_Name:
			return Post.Author.profile.Display_Name
		return ""
	def get_Image(self, Post):
		if Post.Image:
			return Post.Image.url
		return ""
	def get_Image2(self, Post):
		if Post.Image2:
			return Post.Image2.url
		return ""
	def get_Image3(self, Post):
		if Post.Image3:
			return Post.Image3.url
		return ""
	def get_Image4(self, Post):
		if Post.Image4:
			return Post.Image4.url
		return ""			
	def get_RepostAuthor(self, Post):
		if Post.RepostAuthor:
			return Post.RepostAuthor.profile.Display_Name
		return ""                                 
   

	class Meta:
		model = Post
		fields = (
			'id',
			'Topic',
			'Author',
			'Author_Profile',
			'Author_Profile_Picture',
			'Author_Display_Name',
			'Content',
			'LikeCount',
			'ReshareCount',
			'Image',
			'Image2',
			'Image3',
			'Image4',
			'ImageString',
			'CommentCount',
			'IsRepost',
			'IsLike',
			'IsComment',
			'UserHasLiked',
			'UserHasReposted',
			'Reposted',
			'RepostAuthor',
			'Likes',
			'Reposts',
			'Comment',
			'Flags',
			'Created',
			'Req_User_Follows_Author',
		)

   


class LikePostSerializer(serializers.ModelSerializer):
		  
	class Meta:
		model = Post
		fields = (
			'id',
			'Topic',
			'Author',
			'Author_Profile',
			'Author_Profile_Picture',
			'Author_Display_Name',
			'Content',
			'LikeCount',
			'ReshareCount',
			'Image',
			'ImageString',
			'CommentCount',
			'IsRepost',
			'UserHasLiked',
			'UserHasReposted',
			'Reposted',
			'RepostAuthor',
			'Likes',
			'Reposts',
			'Comment',
			'Flags',
			'Created',
			'Req_User_Follows_Author',
		)

	#def to_representation(self, data):
		#data = super(LikePostSerializer, self).to_representation(data)
		#data['LikeCount'] = 5
		#return data

		

class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.SerializerMethodField()
	sender_profile_picture = serializers.SerializerMethodField()
	receiver = serializers.SerializerMethodField()
	def get_sender(self, Message):
		if Message.sender.username:
			return Message.sender.username
		return default
	def get_sender_profile_picture(self, Message):
		if Message.sender.username:
			return Message.sender.profile.Profile_Picture.url
		return default	
	def get_receiver(self, Message):
		if Message.receiver.username:
			return Message.receiver.username
		return default	
	
		
	class Meta:
		model = Message
		fields = (
		'id',
		'post_id',
		'sender',
		'sender_profile_picture',
		'receiver',
		'msg_content',
		'created_at',
		'is_shared_post',	
		)


class NotificationSerializer(serializers.ModelSerializer):
	post = serializers.SerializerMethodField()
	sender = serializers.SerializerMethodField()
	sender_profile_picture = serializers.SerializerMethodField()
	receiver = serializers.SerializerMethodField()
	def get_receiver(self, Notification):
		if Notification:
			return Notification.receiver.username
		return default
	def get_sender(self, Notification):
		if Notification.sender:
			return Notification.sender.username
		return default
	def get_sender_profile_picture(self, Notification):
		if Notification.sender.username:
			return Notification.sender.profile.Profile_Picture.url
		return default	
	def get_post(self, Notification):
		if Notification.post:
			return Notification.post.Content
		return default		

		
	class Meta:
		model = Notification
		fields = (
		'id',
		'post',
		'sender',
		'sender_profile_picture',
		'receiver',
		'is_comment_notification',
		'is_like_notification',
		'is_repost_notification',
		'is_follow_notification',
		'msg',
		'created_at',	
		)



class GroupSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	def get_user(self, User_Groups):
		if User_Groups.user.username:
			return User_Groups.user.username
		return default
		
	class Meta:
		model = User_Groups
		fields = (
		'id',
		'user',
		'Label',
		'Members',	
		)


class TopicSerializer(serializers.ModelSerializer):
		
	class Meta:
		model = Topic
		fields = (
		'id',
		'Label',	
		)


class LoginSerializers(serializers.Serializer):
	class Meta:
		model = User
		username = serializers.CharField(max_length=255)
		password = serializers.CharField(max_length=128, write_only=True)

	def validate(self, data):
		username = data.get('username')
		password = data.get('password')
		if username and password:

			user = authenticate(request=self.context.get('request'),
								username=username, password=password)
			if user:
				data['user'] = user

			data['user'] = user
		return data        	


#def get_Image(self, Post):
		#f = open(Post.Author.Profile.Profile_Picture, 'rb')
		#image = File(f)
		#data = base64.b64encode(image.read())
		#f.close()
		#return data				        