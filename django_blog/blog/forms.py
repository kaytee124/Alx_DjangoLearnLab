from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag

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
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tags separated by commas (e.g., python, django, web)',
            'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
        }),
        help_text='Enter tags separated by commas. New tags will be created automatically.'
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of your post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter the content of your post'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill tags_input with existing tags if editing
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in tags])

    def clean_tags_input(self):
        """Clean and normalize tag names"""
        # Get the raw input value
        tags_input = self.cleaned_data.get('tags_input', '')
        if not tags_input:
            return []
        
        # Split by comma, strip whitespace, and filter out empty strings
        tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        # Normalize: lowercase and remove duplicates
        normalized_tags = []
        seen = set()
        for tag in tag_names:
            # Limit tag length to 50 characters (matching model max_length)
            tag = tag[:50].lower()
            if tag and tag not in seen:
                normalized_tags.append(tag)
                seen.add(tag)
        
        return normalized_tags

    def save(self, commit=True):
        """Save the post and handle tag creation/association"""
        post = super().save(commit=commit)
        
        # Get cleaned tag names (from clean_tags_input method)
        tag_names = self.cleaned_data.get('tags_input', [])
        
        if commit:
            # Clear existing tags
            post.tags.clear()
            
            # Create or get tags and associate with post
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        else:
            # If commit=False, store tag names for later processing
            # This allows the post to be saved first, then tags can be added
            post._pending_tags = tag_names
        
        return post
    
    def save_m2m(self):
        """Handle many-to-many relationships when commit=False is used"""
        # This method is called automatically by Django when commit=False
        if hasattr(self.instance, '_pending_tags'):
            # Clear existing tags
            self.instance.tags.clear()
            
            # Create or get tags and associate with post
            for tag_name in self.instance._pending_tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.instance.tags.add(tag)
            
            # Clean up
            delattr(self.instance, '_pending_tags')

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
