from django import forms
from .models import Website

class LinkForm(forms.Form):
    website = forms.ModelChoiceField(queryset=Website.objects.all(), label='', empty_label=None)
    product = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Product name'}))
    link = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'Link'}))