# forms.py

from django import forms
from django_summernote.widgets import SummernoteWidget
from django import forms  # 댓글 작성 양식



from .models import Post, Comment




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','hook_text','content','head_image','file_upload','category']
        widgets = {
            'content': SummernoteWidget(),
        }


# 댓글 작성 양식
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)