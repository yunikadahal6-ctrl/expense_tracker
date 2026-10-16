from django import forms
from .models import Expense
class ItemForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount  # Always return the cleaned value!

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError("Title is shorter than 3 character")

        # Rule 2: Check if this title is already in the database
        if Expense.objects.filter(title=title).exists():
            raise forms.ValidationError("This expense already exists!")

        return title
        

            
