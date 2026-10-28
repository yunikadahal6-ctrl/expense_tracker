from .models import Task
from django import forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','priority']
    def clean_title(self):
        title = self.cleaned_data.get('title','').strip()

        if len(title) < 3:
            raise forms.ValidationError("Task title must be at least 3")

        #case 2:
        # Check if this title is already in the database
        if Task.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Task already exist")
        return title
    
        