from django import forms
from .models import ProjectComment, Rating
from my_aplication.models import Application

class createCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['author', 'content', 'project', 'content_type', 'object_id', 'comment']


class createRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value', 'project', 'content_type', 'object_id']

class createApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['freelancer', 'accepted', 'project', 'requirement']