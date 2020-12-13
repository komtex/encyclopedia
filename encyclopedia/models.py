from django.db import models
from django import forms

class Article(forms.Form):
    title = forms.CharField(max_length=30)
    content = forms.CharField(widget=forms.Textarea)
