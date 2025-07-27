

# advanced_features_and_security/forms.py

from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'published']



from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(required=False, max_length=100)
