from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm
from .models import Expense
from django.db.models import Sum

# Create your views here.

def expense_list(request):
    category = request.GET.get('category')  # Read ?category=food from URL
    items = Expense.objects.all().order_by('-created_at')
    
    if category:
        items = items.filter(category = category)
    
    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains=query)
    total = items.aggregate(total=Sum('amount'))['total']

    return render(request, 'tracker/expense_list.html', {'items': items, 'total': total})

def expense_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ItemForm()

    return render(request, 'tracker/expense_form.html', {'form': form})

def expense_update(request, pk):
    item = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ItemForm(instance=item)

    return render(request, 'tracker/expense_form.html', {'form': form, 'item': item})

def expense_delete(request, pk):
    item = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('expense_list')

    return render(request, 'tracker/expense_confirm_delete.html', {'item': item})  
