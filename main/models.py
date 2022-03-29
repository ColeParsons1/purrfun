from __future__ import division, unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
#from .forms import PostForm
#from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from warnings import warn
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Sum
#from django.utils.translation import ugettext as _


import uuid




class Meme_Template(models.Model):
    Image = models.ImageField(blank=True, null=True)

    #def __str__(self):
        #return self


class Topic(models.Model):
    Label = models.CharField(max_length=50)
    
    def __unicode__(self):
       return self.Label

       
class User_Groups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Label = models.CharField(max_length=50)
    Members = models.ManyToManyField(User, blank=True, related_name="members")
    
    def __unicode__(self):
       return self.Label     
       

class Post(models.Model):
    Author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Author_Profile = models.ForeignKey('main.Profile', on_delete=models.CASCADE, blank=True, null=True)
    Author_Profile_Picture = models.CharField(max_length=300, blank=True, null=True)
    Author_Display_Name = models.CharField(max_length=300, blank=True, null=True)
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True, related_name="Topic")
    Group = models.ForeignKey(User_Groups, on_delete=models.CASCADE, blank=True, null=True, related_name="User_Groups")
    Content = models.CharField(max_length=300, default=uuid.uuid1)
    Image = models.ImageField(blank=True, null=True)
    Image2 = models.ImageField(blank=True, null=True)
    Image3 = models.ImageField(blank=True, null=True)
    Image4 = models.ImageField(blank=True, null=True)
    ImageString = models.CharField(max_length=300, default="")
    Created = models.DateTimeField(auto_now_add=True)
    LikeCount = models.PositiveIntegerField(default=0)
    ReshareCount = models.PositiveIntegerField(default=0)
    CommentCount = models.PositiveIntegerField(default=0)
    Comments = models.ForeignKey('main.Comment', on_delete=models.CASCADE, blank=True, null=True, related_name="comment")
    PostComments = models.ForeignKey('main.Post', on_delete=models.CASCADE, blank=True, null=True, related_name="postcomment")
    IsOriginalpost = models.BooleanField(default=True)
    IsQuotepost = models.BooleanField(default=False)
    IsRepost = models.BooleanField(default=False)
    IsLike = models.BooleanField(default=False)
    IsComment = models.BooleanField(default=False)
    UserHasLiked = models.BooleanField(default=False)
    UserHasReposted = models.BooleanField(default=False)
    RepostAuthor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="repostAuthor")
    Reposted = models.DateTimeField(auto_now_add=True)
    Likes = models.ManyToManyField(User, blank=True, related_name="likes")
    Reposts = models.ManyToManyField(User, blank=True, related_name="reposts")
    Comment = models.ManyToManyField(User, blank=True, related_name="comments")
    Flags = models.ManyToManyField(User, blank=True, related_name="flags")
    ReplyingTo = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="repto")
    Caption = models.CharField(max_length=300, default=uuid.uuid1)
    PostItem = models.ForeignKey('main.Post', on_delete=models.CASCADE, blank=True, null=True, related_name="pos")
    Req_User_Follows_Author = models.BooleanField(default=False)
    InteractionID = models.PositiveIntegerField(default=0)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=75,
    )
    
    def __str__(self): 
        return self.Content


class Repost(models.Model):
    Reposter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    Post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name='reposted')
    Comments = models.ForeignKey('main.RepostComment', on_delete=models.CASCADE, blank=True, null=True, related_name="repost_comment")
    LikeCount = models.PositiveIntegerField(default=0)
    ReshareCount = models.PositiveIntegerField(default=0)
    CommentCount = models.PositiveIntegerField(default=0)
    Created = models.DateTimeField(auto_now_add=True)
    UserHasLiked = models.BooleanField(default=False)
    UserHasReposted = models.BooleanField(default=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=75,
    )
    
    def __str__(self): 
        return self.Post.Content         


class Liked_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    liked_post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name="posts_liked", blank=True, null=True)
    alreadyLiked = models.BooleanField(default=False)

    def __str__(self):
        return self.liked_post.Content
        
        
class Reshared_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reshare")
    reshared_post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name="posts_reshared", blank=True, null=True)
    alreadyReshared = models.BooleanField(default=False)

    def __str__(self):
        return self.reshared_post.Content
        
        
        
class Commented_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_commented")
    commented_post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name="posts_commented", blank=True, null=True)
    alreadyCommented = models.BooleanField(default=False)

    def __str__(self):
        return self.commented_post.Content         


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    alreadyLiked = models.BooleanField(default=False)

    def __str__(self):
        return 'Liked by {} on {}'.format(self.user) 


class Comment(models.Model): 
    post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name='comments')
    Author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return self.body
        

class Report(models.Model): 
    Offendor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering = ('created',)

        
class Flagged_Post(models.Model):
    post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name='flagged')
    created = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering = ('created',)
    
    def __unicode__(self):
       return self.post.Content    



class RepostComment(models.Model): 
    post = models.ForeignKey('main.RePost', on_delete=models.CASCADE, related_name='repost_comments')
    Author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 


    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return self.body          
  

class FollowingManager(models.Model):

    def followers(self, user):
        key = cache_key("followers", user.pk)
        followers = cache.get(key)

        if followers is None:
            qs = Follow.objects.filter(followee=user).all()
            followers = [u.follower for u in qs]
            cache.set(key, followers)

        return followers

    def following(self, user):
        key = cache_key("following", user.pk)
        following = cache.get(key)
        

        if following is None:
            qs = Follow.objects.filter(follower=user).all()
            following = [u.followee for u in qs]
            cache.set(key, following)

        return following

    def add_follower(self, follower, followee):
        if follower == followee:
            raise ValidationError("Users cannot follow themselves")

        relation, created = Follow.objects.get_or_create(
            follower=follower, followee=followee
        )

        if created is False:
            raise AlreadyExistsError(
                "User '%s' already follows '%s'" % (follower, followee)
            )

        follower_created.send(sender=self, follower=follower)
        followee_created.send(sender=self, followee=followee)
        following_created.send(sender=self, following=relation)

        bust_cache("followers", followee.pk)
        bust_cache("following", follower.pk)

        return relation

    def remove_follower(self, follower, followee):
        try:
            rel = Follow.objects.get(follower=follower, followee=followee)
            follower_removed.send(sender=self, follower=follower)
            followee_removed.send(sender=self, followee=followee)
            following_removed.send(sender=self, following=rel)
            rel.delete()
            bust_cache("followers", followee.pk)
            bust_cache("following", follower.pk)
            return True
        except Follow.DoesNotExist:
            return False

    def follows(self, follower, followee):
        followers = cache.get(cache_key("following", follower.pk))
        following = cache.get(cache_key("followers", followee.pk))

        if followers and followee in followers:
            return True
        elif following and follower in following:
            return True
        else:
            return Follow.objects.filter(follower=follower, followee=followee).exists()


class Follow(models.Model):

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="follower"
    )
    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="followee"
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FollowingManager()

    class Meta:
        verbose_name = _("Following Relationship")
        verbose_name_plural = _("Following Relationships")
        unique_together = ("follower", "followee")

    def __str__(self):
        return "User #%s follows #%s" % (self.follower_id, self.followee_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.follower == self.followee:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)


def _clean_user(user):
    if not app_settings.STAR_RATINGS_ANONYMOUS:
        if not user:
            raise ValueError(_("User is mandatory. Enable 'STAR_RATINGS_ANONYMOUS' for anonymous ratings."))
        return user
    return None
    

class Muted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="muted")






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    Display_Name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    Profile_Picture = models.ImageField(blank=True, null=True)
    Cover_Picture = models.ImageField(blank=True, null=True)
    Liked_posts = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name='liked', blank=True, null=True)
    Reshared_posts = models.ForeignKey('main.Reshared_Post', on_delete=models.CASCADE, related_name='reshared', blank=True, null=True)
    Commented_posts = models.ForeignKey('main.Commented_Post', on_delete=models.CASCADE, related_name='comments_post', blank=True, null=True)
    Flagged_posts = models.ForeignKey('main.Flagged_Post', on_delete=models.CASCADE, related_name='flagged', blank=True, null=True)
    MessagesCount = models.PositiveIntegerField(default=0)
    Notifications = models.PositiveIntegerField(default=0)
    Follower_Count = models.PositiveIntegerField(default=0)
    Following_Count = models.PositiveIntegerField(default=0)
    User_Following = models.ManyToManyField(User, blank=True, null=True, related_name='folwing')
    User_Followers = models.ManyToManyField(User, blank=True, null=True, related_name='folwers')
    isPrivate = models.BooleanField(default=False)
    Groups = models.ForeignKey('main.User_Groups', on_delete=models.CASCADE, related_name='groups', blank=True, null=True)
    Posts = models.ManyToManyField('main.Post', blank=True, null=True, related_name='psts')

    def __str__(User):
        return User.username

    def __str__(User_Following):
        return User_Following.User.username

    def __str__(User_Followers):
        return User_Followers.User.username      
   
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
class user_pics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    Image = models.ImageField(blank=True, null=True)


class default_profile_pic(models.Model):
      image = models.FileField(blank=True, null=True)
      
      
class Message(models.Model):
      sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
      sender_profile_picture = models.CharField(max_length=300, blank=True, null=True)
      receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
      msg_content = models.TextField(max_length=500, blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      is_shared_post = models.BooleanField(default=False)
      post_id = models.PositiveIntegerField(default=0)  

class Notification(models.Model):
      post = models.ForeignKey('main.Post', on_delete=models.CASCADE, related_name='NotificationPost', blank=True, null=True)
      sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_sender")
      sender_profile_picture = models.CharField(max_length=300, blank=True, null=True)
      receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_receiver", blank=True, null=True)
      is_comment_notification = models.BooleanField(default=False)
      is_like_notification = models.BooleanField(default=False)
      is_repost_notification = models.BooleanField(default=False)
      is_follow_notification = models.BooleanField(default=False)
      msg = models.TextField(max_length=100, blank=True)
      created_at = models.DateTimeField(auto_now_add=True)


class Follow_obj(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follower')

    def __str__(self):
        return self.user.username      
    
class Block_obj(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blocker')

    def __str__(self):
        return self.user.username
        
class Mute_obj(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_muter')

    def __str__(self):
        return self.user.username             
