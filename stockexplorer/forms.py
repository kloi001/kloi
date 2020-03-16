from django import forms
from django.db import models

class userprofileform(forms.Form):
    user_name = forms.CharField(max_length=100, label='Name')
    user_age = forms.CharField(max_length=2, label='Age')
    user_job = forms.CharField(max_length=2, label='What is your occupation?')
    user_education = forms.CharField(max_length=2, label='What is your field of study?')
    user_hobby = forms.CharField(max_length=2, label='What are your hobbies?')
