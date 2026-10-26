from django import forms
from .models import Bookmark

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'category']

    def clean_title(self):
        # cleaned_data bata title nikalne
        title = self.cleaned_data.get('title')
        
        # yadi title 3 character vanda chhoto chha bhane error falne
        if title and len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        
        return title

    def clean_url(self):
        # cleaned_data bata url nikalne
        url = self.cleaned_data.get('url')
        
        # database ma yo url paila nai chha ki nai check garne 
        # (exclude le chai update garda aafnai url lai ignore garna help garcha)
        if Bookmark.objects.filter(url=url).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This URL is already bookmarked!")
        
        return url
    