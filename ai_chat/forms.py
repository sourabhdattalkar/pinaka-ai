from django import forms

class APIKeyForm(forms.Form):
    api_key = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your API key'}))

class ChatForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ask a question...'}))
