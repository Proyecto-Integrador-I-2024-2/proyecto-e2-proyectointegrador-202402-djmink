from django import forms
from my_aplication.models import Application, ProjectComment, ProjectRating

class createCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['author', 'content', 'project', 'content_type', 'object_id', 'comment']


class createRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['value', 'project', 'content_type', 'object_id']

class createApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['freelancer', 'project', 'milestone']   

