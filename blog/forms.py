from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BlogPost

# Reader Registration Form
class ReaderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reader = True  # Set the user as a reader
        if commit:
            user.save()
        return user

# Publisher Registration Form
class PublisherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_publisher = True  # Set the user as a publisher
        if commit:
            user.save()
        return user

# Blog Creation
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']