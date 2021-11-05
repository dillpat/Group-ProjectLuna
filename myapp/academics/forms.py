from .models import ModuleComment
from django import forms


class ModuleCommentForm(forms.ModelForm):
    class Meta:
        model = ModuleComment
        fields = ("content",)
