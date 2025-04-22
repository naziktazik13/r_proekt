from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Profile,Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category','video', 'media', 'content', 'status']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',  # Это превратит обычное текстовое поле в поле выбора даты
                'class': 'form-control',
                'placeholder': 'Выберите дату рождения'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image', 'parent']
        widgets = {
            'parent': forms.HiddenInput()
        }

