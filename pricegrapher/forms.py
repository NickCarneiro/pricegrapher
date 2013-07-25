from django import forms

class UrlForm(forms.Form):
    productUrl = forms.URLField()