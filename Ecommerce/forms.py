from django import forms

class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True)
