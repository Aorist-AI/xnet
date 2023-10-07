from django import forms
from .models import Messages


class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 50,
        'rows': 2.5
    }))

    class Meta:
        model = Messages
        fields = ['message']
