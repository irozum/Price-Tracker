from django import forms

class LinkForm(forms.Form):
    product = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Product name'}))
    link = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'Link'}))