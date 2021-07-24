from django import forms
from .models import Post, Category, Comment


choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)


POST_CHOICES = ["Normal", "HighlySuggested"]


class PostForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'category',
                  'body', 'snippet', 'header_image', )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'elder', 'type': 'hidden'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Messages'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),


        }


class EditForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'category', 'isSuggested',
                  'body', 'snippet', 'header_image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'isSuggested': forms.Select(choices=POST_CHOICES, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),

        }


class AddCommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'user')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 10}),
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'elder', 'type': 'hidden'}),
        }
