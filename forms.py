from django import forms
from .models import *

class NewPost(forms.Form):
    new_title = forms.CharField(label='Title', max_length=100)
    new_body = forms.CharField(label='Body')
    tags = forms.CharField(label='Tags')


class NewComment(forms.Form):
	new_comment_body = forms.CharField(label='CommentBody')
	

class Search(forms.Form):
	search = forms.CharField()
# Needed to save the user input when creating posts.
