from django.shortcuts import render, redirect, get_object_or_404
import json
from .forms import ItemForm
from .models import Expense
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Naya user database ma save huncha
            return redirect('login')  # Banisake pachi Login page ma pathaune
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Create your views here.
@login_required
def expense_list(request):
    items = Expense.objects.filter(user=request.user).order_by('-id')

    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains=query)

    total = items.aggregate(Sum('amount'))['amount__sum'] or 0

    # Category-wise totals for chart
    user_expenses = Expense.objects.filter(user=request.user)
    food_total = float(user_expenses.filter(category='food').aggregate(Sum('amount'))['amount__sum'] or 0)
    transport_total = float(user_expenses.filter(category='transport').aggregate(Sum('amount'))['amount__sum'] or 0)
    bills_total = float(user_expenses.filter(category='bills').aggregate(Sum('amount'))['amount__sum'] or 0)
    other_total = float(user_expenses.filter(category='other').aggregate(Sum('amount'))['amount__sum'] or 0)

    # json.dumps() le python list lai safe JS array banaucha
    chart_data = json.dumps([food_total, transport_total, bills_total, other_total])

    context = {
        'items': items,
        'total': total,
        'chart_data': chart_data,
    }
    return render(request, 'tracker/expense_list.html', context)

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
        # Login vako user lai yo bookmark ko malik banaune
            expense.user = request.user
            # Ani balla final save garne
            expense.save()
            return redirect('expense_list')
    else:
        form = ItemForm()

    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def expense_update(request, pk):
    item = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ItemForm(instance=item)

    return render(request, 'tracker/expense_form.html', {'form': form, 'item': item})

@login_required
def expense_delete(request, pk):
    item = get_object_or_404(Expense, pk=pk,user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('expense_list')

    return render(request, 'tracker/expense_confirm_delete.html', {'item': item})  
