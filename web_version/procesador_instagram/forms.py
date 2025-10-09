from django import forms

class UploadForm(forms.Form):
    followers_file = forms.FileField(label='followers_1.json')
    following_file = forms.FileField(label='following.json')