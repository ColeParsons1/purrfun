from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post
from .models import Comment
from .models import Profile
from .models import Report, Message, user_pics, Topic, User_Groups
#from friendship.models import Follow, Block
#from .models import FollowingManager
import ast
#from .models import UserRating
#from django.db.models.loading import get_model

#Libro = get_model('Post')


class MyForm (forms.Form):
    def __init__ (self, Topic, Content, *args, **kwargs):
        self.Content = Topic
        self.desc = Content
        super (MyForm, self).__init__ (*args, **kwargs)



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('reason',)

        
class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(label="Send to:",queryset=User.objects.order_by('username'))
    msg_content = forms.CharField(label='Text', max_length=100, required=False)
    #post = forms.ModelChoiceField(queryset=Post.objects.order_by('Created').reverse())

    class Meta:
        model = Message
        fields = ('receiver', 'msg_content',)
        
    #def __init__(self, *args, **kwargs):
        #super(MessageForm, self).__init__(*args, **kwargs)
        #self.fields['post'].required = False     
        
        
class DMPostForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = Message
        fields = ('receiver',)          


YEARS = [x for x in range(1940,2021)]    
class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(label="When's your birthday?", widget=forms.SelectDateWidget(years=YEARS))
    bio = forms.CharField(label='Bio',widget=forms.Textarea, max_length=260, required=False)
    location = forms.CharField(label='Location',max_length=30, required=False)
    profile_pic = forms.ImageField(widget = forms.FileInput())

    class Meta:
        model = User
        fields = ('birth_date', 'location', 'bio', 'profile_pic', )
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False
        
        
class ImageForm(forms.ModelForm):
    Image = forms.ImageField(widget = forms.FileInput())

    class Meta:
        model = user_pics
        fields = ('Image', )
        
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['Image'].required = False          
        

YEARS = [x for x in range(1940,2021)]        
class Profile(forms.ModelForm):

    birth_date = forms.DateField(label="Birth date", widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'location', 'Profile_Picture',)        

my_default_errors = {
    'invalid': 'Vibe Check'
}

Invalid = "politics, political"        
class PostForm(forms.ModelForm):

    Content = forms.CharField(label='Text', widget=forms.TextInput(attrs={'rows':4, 'cols':15}), error_messages=my_default_errors)
    Image = forms.ImageField(widget = forms.FileInput())
    Topic = forms.ModelChoiceField(queryset=Topic.objects.order_by('Label'))
    Group = forms.ModelChoiceField(queryset=User_Groups.objects.order_by('Label'))

    class Meta:
        model = Post
        fields = ('Group', 'Topic', 'Image', 'Content',)
        
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['Group'].required = False 
        self.fields['Image'].required = False
        self.fields['Content'].required = False 
        self.fields['Topic'].required = False

    def clean_Content(self):
        Content = self.cleaned_data.get('Content')
        
        if Content:
            if "politics" not in Content: 
                Content = Content
            else:
                Content = "My vibe has been checked :("
                
        return Content    

        
YEARS = [x for x in range(1940,2021)]
class sign(UserCreationForm):
    email = forms.EmailField(label='Email',max_length=54, required=True, help_text='')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    birth_date = forms.DateField(label="When's your birthday?", widget=forms.SelectDateWidget(years=YEARS))
    bio = forms.CharField(label='Bio',widget=forms.Textarea, max_length=260, required=False)
    location = forms.CharField(label='Location',max_length=30, required=False)
    profile_pic = forms.FileField(label='Profile Picture',required=False)
    class Meta:
        model = User
        fields = ('username', 'birth_date', 'location', 'bio', 'profile_pic',)

        
YEARS = [x for x in range(1940,2021)]        
class user_edit_profile(forms.ModelForm):
    
    birth_date = forms.DateField(label="When's your birthday?", widget=forms.SelectDateWidget(years=YEARS))
    bio = forms.CharField(label='Bio',widget=forms.Textarea, max_length=260, required=False)
    location = forms.CharField(label='Location',max_length=30, required=False)
    profile_pic = forms.FileField(label='Profile Picture',required=False)

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'location', 'bio', 'profile_pic',)  


class report(forms.ModelForm):
    message = forms.CharField(label='Location',max_length=30, required=False)
    #'email','password1', 'password2',
    class Meta:
        model = User
        fields = ('message',)

        
class GroupForm(forms.ModelForm):

    Label = forms.CharField(label='Group Label', widget=forms.TextInput(attrs={'rows':1, 'cols':7}), required=False)
    Members = forms.ModelMultipleChoiceField(label='Group Members', widget=forms.SelectMultiple(attrs={'rows':1, 'cols':1}), queryset=User.objects.distinct().order_by('username'), required=False)


    class Meta:
        model = User_Groups
        fields = ('Members', 'Label',)
        
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['Members'].required = False
        self.fields['Label'].required = False
        #self.fields['Members'] = self.instance.Members.split(',')
    
    #def clean_groups(self):
        #Members = self.cleaned_data['Members']
        #if Members:
            #assert isinstance(Members, (list, tuple))
            #return str(','.join(Members))
        #else:
            #return '' 
        