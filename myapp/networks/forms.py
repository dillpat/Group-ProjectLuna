from .models import NetworkComment
from django import forms


class NetworkCommentForm(forms.ModelForm):
    class Meta:
        model = NetworkComment
        fields = ("content",)
