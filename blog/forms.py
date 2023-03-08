from django import forms

from .models import Post

from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    def clean(self):
        clean_data = super().clean()
        if Post.objects.filter(title = clean_data.get("title", "")).exists():
            raise ValidationError ("Post Title Exists!")
        return clean_data
      
    class Meta:
        model = Post
        fields = ('title', 'text')