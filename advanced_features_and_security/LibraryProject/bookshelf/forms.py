

# advanced_features_and_security/forms.py

from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'published']


# LibraryProject/bookshelf/forms.py

from django import forms

class ExampleForm(forms.Form):
    # Define your form fields here
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
