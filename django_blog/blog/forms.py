from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('instance', None)
        super().__init__(*args, instance=self.user_instance, **kwargs)

        # Pre-fill profile_picture field from related Profile
        if self.user_instance and hasattr(self.user_instance, 'profile'):
            self.fields['profile_picture'].initial = self.user_instance.profile.profile_picture

    def save(self, commit=True):
        # Save the User fields
        user = super().save(commit=commit)

        # Save the profile picture to the related Profile
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            profile = getattr(user, 'profile', None)
            if profile:
                profile.profile_picture = profile_picture
                if commit:
                    profile.save()

        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of your post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter the content of your post'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter your comment...',
                'rows': 4,
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;'
            })
        }
