from django.contrib import admin
#from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import auth
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.sites import AdminSite
#from .models import Profile
from .models import Topic
from .models import Meme_Template
from API.models import API_Test
from .models import Post, Comment, Repost, Liked_Post, Profile, default_profile_pic, Report, Flagged_Post, Message, Notification, User_Groups
#from friendship.admin import 

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Liked_Post)
admin.site.register(default_profile_pic)
admin.site.unregister(default_profile_pic)
admin.site.register(Report)
admin.site.register(Flagged_Post)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(User_Groups)
admin.site.register(API_Test)
admin.site.register(Meme_Template)
admin.site.site_header = 'Purrfun administration'
@admin.register(Comment)




class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created')
    list_filter = ('created', 'updated')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'
    

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('get_user', 'is_staff', 'get_location','get_birth_date', 'get_bio', 'get_profile_pic', )
    list_select_related = ('profile', )
    
    def get_user(self, instance):
        return instance.profile.user.username
    get_user.short_description = 'User'
    
    def get_bio(self, instance):
        return instance.profile.bio
    get_bio.short_description = 'Bio'

    def get_birth_date(self, instance):
        return instance.profile.birth_date
    get_birth_date.short_description = 'Birth date'
    
    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'
    
    def get_profile_pic(self, instance):
        return instance.profile.Profile_Picture
    get_profile_pic.short_description = 'Profile Picture'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

     
        
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)   
    


